# -*- coding: utf-8 -*-
"""
Integration tests for the Text2MidiApp TUI.
Uses Textual's built-in app testing pilot.
"""

import pytest

from main_tui import Text2MidiApp


class TestTuiAppLaunch:
    """Smoke tests — verify the app composes and mounts without errors."""

    @pytest.mark.asyncio
    async def test_app_launches(self):
        """App should start and compose all widgets."""
        app = Text2MidiApp()
        async with app.run_test(size=(120, 40)) as pilot:
            # Verify main containers exist
            assert app.query_one("#main-horizontal") is not None
            assert app.query_one("#sidebar") is not None
            assert app.query_one("#main-content") is not None

    @pytest.mark.asyncio
    async def test_prompt_widget_exists(self):
        app = Text2MidiApp()
        async with app.run_test(size=(120, 40)) as pilot:
            prompt_widget = app.query_one("#prompt-widget")
            assert prompt_widget is not None

    @pytest.mark.asyncio
    async def test_progress_panel_hidden_initially(self):
        app = Text2MidiApp()
        async with app.run_test(size=(120, 40)) as pilot:
            progress = app.query_one("#progress-panel")
            assert "visible" not in progress.classes

    @pytest.mark.asyncio
    async def test_output_panel_hidden_initially(self):
        app = Text2MidiApp()
        async with app.run_test(size=(120, 40)) as pilot:
            output = app.query_one("#output-panel")
            assert "visible" not in output.classes

    @pytest.mark.asyncio
    async def test_sidebar_has_presets(self):
        app = Text2MidiApp()
        async with app.run_test(size=(120, 40)) as pilot:
            tree = app.query_one("#sidebar-tree")
            assert tree is not None

    @pytest.mark.asyncio
    async def test_help_screen(self):
        """F1 should push the help screen."""
        app = Text2MidiApp()
        async with app.run_test(size=(120, 40)) as pilot:
            await pilot.press("f1")
            # Help screen should now be on the screen stack
            assert len(app.screen_stack) > 1

    @pytest.mark.asyncio
    async def test_toggle_sidebar(self):
        """Ctrl+H should toggle sidebar visibility."""
        app = Text2MidiApp()
        async with app.run_test(size=(120, 40)) as pilot:
            sidebar = app.query_one("#sidebar")
            assert sidebar.display is True
            await pilot.press("ctrl+h")
            assert sidebar.display is False
            await pilot.press("ctrl+h")
            assert sidebar.display is True
