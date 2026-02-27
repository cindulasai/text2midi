# -*- coding: utf-8 -*-
"""
Sidebar Widget
Genre presets tree + generation history tree.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import Static, Tree
from textual.widgets.tree import TreeNode

from src.tui.history import HistoryManager


# ------------------------------------------------------------------ #
# Static preset prompts (used as fallback / instant load)
# ------------------------------------------------------------------ #

_PRESETS: dict[str, list[str]] = {
    "🎹 Ambient": [
        "Create a peaceful meditative ambient soundscape with floating pads and soft bells",
        "Generate a dark mysterious ambient piece with dissonant textures and drones",
        "Compose a warm ambient wash with gentle evolving synthesizer textures",
    ],
    "🎬 Cinematic": [
        "Compose an epic cinematic orchestral piece with sweeping strings and brass",
        "Create a tense cinematic score with staccato strings and building percussion",
        "Write a hopeful cinematic theme with soaring violin melody and warm orchestra",
    ],
    "🎸 Pop / Rock": [
        "Create a catchy pop track with bright synths, driving drums, and vocal melody",
        "Generate an indie rock song with jangly guitars and steady drumbeat",
        "Compose a power ballad with emotional piano intro building to full band",
    ],
    "🎷 Jazz": [
        "Write a smooth jazz improvisation with sultry saxophone and piano comping",
        "Create a bebop jazz piece with fast piano runs and walking bass",
        "Generate a cool jazz trio piece with brushed drums and muted trumpet",
    ],
    "🎧 Electronic": [
        "Generate a funky electronic groove with synth leads and syncopated bass",
        "Compose an uplifting trance anthem with arpeggiated synths and euphoric build",
        "Create a deep house track with warm bass, hi-hats, and smooth pads",
    ],
    "📻 Lo-fi": [
        "Create a melancholy lo-fi hip hop beat with vinyl crackle and gentle piano",
        "Generate a rainy-day lo-fi study beat with soft guitar and tape hiss",
        "Compose a nostalgic lo-fi beat with jazzy chords and mellow drums",
    ],
    "🎻 Classical": [
        "Write a classical chamber piece with elegant piano and sweeping cello",
        "Compose a baroque-inspired harpsichord and strings arrangement",
        "Create a romantic-era piano sonata in D minor with dramatic dynamics",
    ],
    "🎸 Funk": [
        "Generate a funky groove with slap bass, wah guitar, and tight drums",
        "Create a 70s disco-funk track with brass stabs and syncopated rhythm guitar",
        "Compose an acid jazz funk piece with organ, bass, and breakbeat drums",
    ],
}


class Sidebar(Static):
    """Left sidebar with genre presets and generation history."""

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

    def compose(self) -> ComposeResult:
        tree: Tree[str] = Tree("text2midi", id="sidebar-tree")
        tree.root.expand()
        yield tree

    def on_mount(self) -> None:
        self._build_tree()

    def _build_tree(self) -> None:
        tree = self.query_one("#sidebar-tree", Tree)
        tree.clear()

        # Presets
        presets_node = tree.root.add("🎵 Presets")
        presets_node.expand()
        for genre, prompts in _PRESETS.items():
            genre_node = presets_node.add(genre)
            for p in prompts:
                label = p[:40] + "…" if len(p) > 40 else p
                genre_node.add_leaf(label, data=p)

        # History
        history_node = tree.root.add("📂 History")
        history_node.expand()
        entries = HistoryManager.get_entries(limit=20)
        if not entries:
            history_node.add_leaf("(no history yet)")
        else:
            for entry in entries:
                label = entry.get("prompt", "")[:40]
                if len(entry.get("prompt", "")) > 40:
                    label += "…"
                genre_tag = entry.get("genre", "")
                quality = entry.get("quality", 0)
                display = f"{label}  [{genre_tag} {quality:.0%}]" if genre_tag else label
                history_node.add_leaf(display, data=entry.get("prompt", ""))

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node: TreeNode = event.node
        if node.data and isinstance(node.data, str):
            # Determine if preset or history
            # Walk up to see parent label
            parent = node.parent
            while parent and parent.parent:
                if "Presets" in str(parent.label):
                    self.post_message(self.PresetSelected(node.data))
                    return
                if "History" in str(parent.label):
                    self.post_message(self.HistorySelected(node.data))
                    return
                parent = parent.parent
            # Fallback — treat as preset
            self.post_message(self.PresetSelected(node.data))

    def refresh_history(self) -> None:
        """Rebuild the tree to reflect new history entries."""
        self._build_tree()
