# -*- coding: utf-8 -*-
"""
Sidebar Widget — Dynamic LLM-Powered Preset Tree

Builds a 3-level genre hierarchy from ``genre_registry.GENRE_TREE``:
  Presets → Root Genre → Sub-genre → [LLM-generated prompts]

Prompts are generated lazily when a user expands a sub-genre node.
Falls back to curated seed presets when the LLM is unavailable.

Fault-tolerance features (Plan-TUI):
  - Inline status label above the tree for progress / error display
  - Up to 2 retries with 2 s cooldown on LLM failures
  - Sidebar-level duplicate detection with automatic retry
  - Concurrency guard (prevents double-loading the same genre)
  - Rate limiter (≥ 2 s between any two sidebar LLM calls)
  - All event handlers and callbacks hardened with try/except

See SPEC-005-DYNAMIC-PRESETS for full specification.
"""

from __future__ import annotations

import logging
import time
from threading import Thread
from typing import Optional

from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import Label, Static, Tree
from textual.widgets.tree import TreeNode

from src.services.preset_service import PresetService, get_preset_service
from src.tui.history import HistoryManager

logger = logging.getLogger(__name__)

# Sentinel data markers (not user-visible prompts)
_MARKER_LOADING = "__loading__"
_MARKER_MORE = "__more__"

# Retry / rate-limit constants
_MAX_RETRIES = 2          # 1 initial + 2 retries = 3 total attempts
_RETRY_COOLDOWN = 2.0     # seconds between retries
_MIN_CALL_GAP = 2.0       # minimum seconds between any two LLM sidebar calls
_ERROR_DISMISS_SECS = 5.0 # auto-clear error status after this many seconds


class Sidebar(Static):
    """Left sidebar with dynamic genre preset tree and generation history."""

    class PresetSelected(Message):
        """A preset prompt was clicked."""
        def __init__(self, prompt: str) -> None:
            super().__init__()
            self.prompt = prompt

    class HistorySelected(Message):
        """A history entry was clicked."""
        def __init__(self, prompt: str) -> None:
            super().__init__()
            self.prompt = prompt

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._svc: PresetService = get_preset_service()
        # Track which genre nodes have been populated
        self._populated: set[str] = set()
        # Map tree node IDs to genre IDs for expansion handling
        self._node_genre_map: dict[int, str] = {}
        # Reference to presets root node
        self._presets_node: Optional[TreeNode] = None
        self._history_node: Optional[TreeNode] = None

        # ── Fault-tolerance state ───────────────────────────────
        # Sidebar-level duplicate detection: genre_id → set of normalised prompts
        self._generated_prompts: dict[str, set[str]] = {}
        # Genres currently being loaded (concurrency guard)
        self._loading_genres: set[str] = set()
        # Timestamp of last LLM call (rate limiter)
        self._last_llm_call: float = 0.0

    # ------------------------------------------------------------------ #
    # Compose & mount
    # ------------------------------------------------------------------ #

    def compose(self) -> ComposeResult:
        yield Label("", id="sidebar-status")
        tree: Tree[str] = Tree("🎵 Presets", id="sidebar-tree")
        tree.root.expand()
        yield tree

    def on_mount(self) -> None:
        self._build_tree()

    # ------------------------------------------------------------------ #
    # Status label helpers
    # ------------------------------------------------------------------ #

    def _set_status(self, text: str, *, error: bool = False) -> None:
        """Show a message in the sidebar status label."""
        try:
            lbl = self.query_one("#sidebar-status", Label)
            lbl.update(text)
            lbl.add_class("visible")
            if error:
                lbl.add_class("sidebar-error")
            else:
                lbl.remove_class("sidebar-error")
        except Exception:
            pass  # widget may not exist yet during early init

    def _clear_status(self) -> None:
        """Hide the sidebar status label."""
        try:
            lbl = self.query_one("#sidebar-status", Label)
            lbl.update("")
            lbl.remove_class("visible")
            lbl.remove_class("sidebar-error")
        except Exception:
            pass

    # ------------------------------------------------------------------ #
    # Tree construction
    # ------------------------------------------------------------------ #

    def _build_tree(self) -> None:
        """Build the full sidebar tree: Presets (root) + History."""
        tree = self.query_one("#sidebar-tree", Tree)
        tree.clear()
        self._node_genre_map.clear()
        self._populated.clear()

        # ── Presets section (Level 1: root genres) ──────────────
        self._presets_node = tree.root
        roots = self._svc.get_root_categories()
        for root_genre in roots:
            display = self._svc.get_display_name(root_genre)
            root_node = tree.root.add(display)
            self._node_genre_map[root_node.id] = root_genre.id

            # Level 2: sub-genres (all collapsed)
            subs = self._svc.get_sub_genres(root_genre.id)
            if subs:
                for sub in subs:
                    sub_node = root_node.add(sub.name)
                    self._node_genre_map[sub_node.id] = sub.id
                    # Add a placeholder so the node shows as expandable
                    sub_node.add_leaf("⏳ Expand to load prompts…", data=_MARKER_LOADING)
            else:
                # Root genre with no children — add placeholder for direct prompts
                root_node.add_leaf("⏳ Expand to load prompts…", data=_MARKER_LOADING)

        # ── History section ─────────────────────────────────────
        self._history_node = tree.root.add("📂 History")
        self._history_node.expand()
        self._populate_history()

    def _populate_history(self) -> None:
        """Populate (or repopulate) the history subtree."""
        if self._history_node is None:
            return
        # Clear existing history children
        self._history_node.remove_children()
        entries = HistoryManager.get_entries(limit=20)
        if not entries:
            self._history_node.add_leaf("(no history yet)")
        else:
            for entry in entries:
                label = entry.get("prompt", "")[:40]
                if len(entry.get("prompt", "")) > 40:
                    label += "…"
                genre_tag = entry.get("genre", "")
                quality = entry.get("quality", 0)
                display = f"{label}  [{genre_tag} {quality:.0%}]" if genre_tag else label
                self._history_node.add_leaf(display, data=entry.get("prompt", ""))

    # ------------------------------------------------------------------ #
    # Retry / rate-limit helper (runs in background thread)
    # ------------------------------------------------------------------ #

    def _generate_with_retries(
        self, genre_id: str, *, bypass_cache: bool = False
    ) -> list[str]:
        """Call PresetService with retries, cooldown, dedup, and rate-limit.

        Returns a list of *unique* (not previously shown) prompts, or ``[]``
        when all avenues are exhausted.  Never raises.

        Short-circuits immediately to seed fallback when the first attempt
        returns an empty list (typically means auth failure / 401 — no point
        retrying the same broken credentials multiple times).
        """
        known = self._generated_prompts.get(genre_id, set())
        had_hard_failure = False

        for attempt in range(1 + _MAX_RETRIES):
            # ── Short-circuit: if the LLM is clearly broken, skip to seeds ──
            if had_hard_failure:
                break

            # ── Rate-limit: ensure ≥ _MIN_CALL_GAP since last call ──
            elapsed = time.time() - self._last_llm_call
            if elapsed < _MIN_CALL_GAP:
                time.sleep(_MIN_CALL_GAP - elapsed)
            self._last_llm_call = time.time()

            try:
                prompts = self._svc.generate_presets(
                    genre_id, count=1, bypass_cache=bypass_cache,
                )
            except Exception:
                # Hard error (network, auth, etc.) — don't retry, go to seeds
                had_hard_failure = True
                prompts = []

            # If generate_presets returned empty (LLM returned None for all
            # providers, e.g. 401), don't retry — go straight to seeds.
            if not prompts and attempt == 0:
                had_hard_failure = True
                continue

            # ── Filter sidebar-level duplicates ──────────────────
            if prompts:
                unique = [
                    p for p in prompts
                    if self._svc._normalize(p) not in known  # noqa: SLF001
                ]
                if unique:
                    return unique
                # All duplicates — worth retrying with fresh generation

            # ── Cooldown before retry ────────────────────────────
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_COOLDOWN)

        # ── Final fallback: seed presets (also deduped) ──────────
        try:
            seeds = self._svc.get_seed_presets(genre_id)
            unique_seeds = [
                s for s in seeds
                if self._svc._normalize(s) not in known  # noqa: SLF001
            ][:1]
            if unique_seeds:
                return unique_seeds
        except Exception:
            pass  # truly nothing works — return empty

        return []

    def _register_prompts(self, genre_id: str, prompts: list[str]) -> None:
        """Record prompts in the sidebar-level dedup set."""
        if genre_id not in self._generated_prompts:
            self._generated_prompts[genre_id] = set()
        for p in prompts:
            self._generated_prompts[genre_id].add(self._svc._normalize(p))  # noqa: SLF001

    # ------------------------------------------------------------------ #
    # Lazy loading on expand
    # ------------------------------------------------------------------ #

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """When a genre/sub-genre node is expanded, load prompts via LLM."""
        try:
            node: TreeNode = event.node
            genre_id = self._node_genre_map.get(node.id)
            if genre_id is None:
                return  # Not a genre node (e.g., history, root)

            if genre_id in self._populated:
                return  # Already loaded

            # Check if this node has sub-genre children (Level 1 expanding)
            subs = self._svc.get_sub_genres(genre_id)
            if subs:
                # Level 1 root genre — sub-genre nodes already added in _build_tree
                self._populated.add(genre_id)
                return

            # Level 2 sub-genre (or root with no children) — load prompts
            self._load_presets_async(node, genre_id)
        except Exception as exc:
            logger.exception("on_tree_node_expanded error: %s", exc)
            self._set_status("Something went wrong", error=True)
            self.set_timer(_ERROR_DISMISS_SECS, self._clear_status)

    def _load_presets_async(self, node: TreeNode, genre_id: str) -> None:
        """Load presets in a background thread, then update the tree."""
        # ── Concurrency guard ────────────────────────────────────
        if genre_id in self._loading_genres:
            return
        self._loading_genres.add(genre_id)
        self._populated.add(genre_id)

        # Remove the placeholder
        node.remove_children()
        node.add_leaf("⏳ Generating ideas…", data=_MARKER_LOADING)

        # Show status
        genre_label = genre_id.split(".")[-1].replace("_", " ").title()
        self._set_status(f"Generating idea for {genre_label}…")

        def _worker() -> None:
            try:
                prompts = self._generate_with_retries(genre_id)
                self.app.call_from_thread(
                    self._on_presets_loaded, node, genre_id, prompts,
                )
            except Exception as exc:
                logger.exception("_load_presets_async worker crashed: %s", exc)
                self.app.call_from_thread(
                    self._on_load_failed, node, genre_id, str(exc),
                )

        thread = Thread(target=_worker, daemon=True)
        thread.start()

    def _on_presets_loaded(
        self, node: TreeNode, genre_id: str, prompts: list[str]
    ) -> None:
        """Callback: replace spinner with actual prompt leaves."""
        try:
            # Release concurrency guard
            self._loading_genres.discard(genre_id)

            node.remove_children()

            if prompts:
                self._register_prompts(genre_id, prompts)
                for prompt in prompts:
                    label = prompt[:50] + "…" if len(prompt) > 50 else prompt
                    node.add_leaf(label, data=prompt)
            else:
                node.add_leaf("(no ideas available)", data=_MARKER_LOADING)

            # Add "More ideas" refresh button
            node.add_leaf("🔄 More ideas", data=f"{_MARKER_MORE}:{genre_id}")
            node.expand()
            self._clear_status()
        except Exception as exc:
            logger.exception("_on_presets_loaded callback error: %s", exc)
            self._loading_genres.discard(genre_id)
            self._clear_status()

    def _on_load_failed(
        self, node: TreeNode, genre_id: str, error_msg: str
    ) -> None:
        """Callback: show graceful failure state in the tree."""
        try:
            self._loading_genres.discard(genre_id)
            node.remove_children()
            node.add_leaf("(no ideas available)", data=_MARKER_LOADING)
            node.add_leaf("🔄 Retry", data=f"{_MARKER_MORE}:{genre_id}")
            node.expand()

            short = (error_msg[:60] + "…") if len(error_msg) > 60 else error_msg
            self._set_status(f"Could not load ideas: {short}", error=True)
            self.set_timer(_ERROR_DISMISS_SECS, self._clear_status)
        except Exception as exc:
            logger.exception("_on_load_failed callback error: %s", exc)
            self._loading_genres.discard(genre_id)
            self._clear_status()

    # ------------------------------------------------------------------ #
    # "More ideas" handler
    # ------------------------------------------------------------------ #

    def _handle_more_ideas(self, genre_id: str, node: TreeNode) -> None:
        """Generate additional prompts and append them to the node."""
        # Find the parent genre node (the "More ideas" leaf's parent)
        parent = node.parent
        if parent is None:
            return

        # ── Concurrency guard ────────────────────────────────────
        if genre_id in self._loading_genres:
            return
        self._loading_genres.add(genre_id)

        # Remove the "More ideas" leaf, add spinner
        node.remove()
        spinner = parent.add_leaf("⏳ Generating more…", data=_MARKER_LOADING)

        genre_label = genre_id.split(".")[-1].replace("_", " ").title()
        self._set_status(f"Generating more ideas for {genre_label}…")

        def _worker() -> None:
            try:
                prompts = self._generate_with_retries(
                    genre_id, bypass_cache=True,
                )
                self.app.call_from_thread(
                    self._on_more_loaded, parent, genre_id, prompts, spinner,
                )
            except Exception as exc:
                logger.exception("_handle_more_ideas worker crashed: %s", exc)
                self.app.call_from_thread(
                    self._on_more_failed, parent, genre_id, spinner, str(exc),
                )

        thread = Thread(target=_worker, daemon=True)
        thread.start()

    def _on_more_loaded(
        self,
        parent: TreeNode,
        genre_id: str,
        prompts: list[str],
        spinner: TreeNode,
    ) -> None:
        """Callback: append new prompts after the existing ones."""
        try:
            self._loading_genres.discard(genre_id)
            spinner.remove()

            if prompts:
                self._register_prompts(genre_id, prompts)
                for prompt in prompts:
                    label = prompt[:50] + "…" if len(prompt) > 50 else prompt
                    parent.add_leaf(label, data=prompt)
            else:
                parent.add_leaf("(no new ideas)", data=_MARKER_LOADING)

            # Re-add "More ideas" at bottom
            parent.add_leaf("🔄 More ideas", data=f"{_MARKER_MORE}:{genre_id}")
            self._clear_status()
        except Exception as exc:
            logger.exception("_on_more_loaded callback error: %s", exc)
            self._loading_genres.discard(genre_id)
            self._clear_status()

    def _on_more_failed(
        self,
        parent: TreeNode,
        genre_id: str,
        spinner: TreeNode,
        error_msg: str,
    ) -> None:
        """Callback: graceful failure for 'More ideas'."""
        try:
            self._loading_genres.discard(genre_id)
            spinner.remove()
            parent.add_leaf("🔄 More ideas", data=f"{_MARKER_MORE}:{genre_id}")

            short = (error_msg[:60] + "…") if len(error_msg) > 60 else error_msg
            self._set_status(f"Could not generate ideas: {short}", error=True)
            self.set_timer(_ERROR_DISMISS_SECS, self._clear_status)
        except Exception as exc:
            logger.exception("_on_more_failed callback error: %s", exc)
            self._loading_genres.discard(genre_id)
            self._clear_status()

    # ------------------------------------------------------------------ #
    # Node selection handler
    # ------------------------------------------------------------------ #

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        try:
            node: TreeNode = event.node
            if not node.data or not isinstance(node.data, str):
                return

            data: str = node.data

            # Ignore loading markers
            if data == _MARKER_LOADING:
                return

            # Handle "More ideas" / "Retry" click
            if data.startswith(_MARKER_MORE + ":"):
                genre_id = data.split(":", 1)[1]
                self._handle_more_ideas(genre_id, node)
                return

            # Determine if preset or history by walking up to parent
            parent = node.parent
            while parent and parent.parent:
                if "History" in str(parent.label):
                    self.post_message(self.HistorySelected(data))
                    return
                parent = parent.parent

            # Everything else is a preset prompt
            self.post_message(self.PresetSelected(data))
        except Exception as exc:
            logger.exception("on_tree_node_selected error: %s", exc)
            self._set_status("Something went wrong", error=True)
            self.set_timer(_ERROR_DISMISS_SECS, self._clear_status)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def refresh_history(self) -> None:
        """Rebuild only the history section (preserves preset tree state)."""
        try:
            self._populate_history()
        except Exception as exc:
            logger.exception("refresh_history error: %s", exc)
