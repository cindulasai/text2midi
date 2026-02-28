# -*- coding: utf-8 -*-
"""
Track Planning Engine
Plans track configuration based on user input and genre.

Delegates core logic to :mod:`src.services.track_planning`.
"""

import logging
from typing import List, Optional

from src.agents.state import MusicIntent, TrackConfig
from src.config.llm import LLMConfig
from src.services.track_planning import (
    ensure_track_count,
    extract_track_count,
    plan_tracks_with_ai,
    plan_tracks_with_rules,
)

logger = logging.getLogger(__name__)


class TrackPlanner:
    """AI-powered track planning based on user prompt."""

    def plan_tracks(self, user_prompt: str, genre: str, requested_count: Optional[int] = None) -> List[TrackConfig]:
        """Determine track configuration based on prompt.

        Args:
            user_prompt: User's music description
            genre: Music genre
            requested_count: Explicit track count if specified

        Returns:
            List of TrackConfig objects
        """
        if requested_count is None:
            requested_count = extract_track_count(user_prompt)

        logger.info("🎵 Track Planning: Requested count = %s", requested_count)

        # Build a lightweight MusicIntent so the shared service can operate
        intent = MusicIntent(
            raw_prompt=user_prompt,
            genre=genre,
            track_count=requested_count,
        )

        if LLMConfig.AVAILABLE_PROVIDERS:
            tracks = plan_tracks_with_ai(intent, raw_prompt=user_prompt, requested_count=requested_count)
        else:
            tracks = plan_tracks_with_rules(intent, raw_prompt=user_prompt, requested_count=requested_count)

        logger.info("🎵 Track Planning: Generated %d track configs", len(tracks))

        if requested_count and len(tracks) != requested_count:
            logger.warning("⚠️  Track count mismatch! Requested %s, got %d. Adjusting...", requested_count, len(tracks))
            tracks = ensure_track_count(tracks, requested_count, genre)
            logger.info("🎵 Track Planning: Adjusted to %d tracks", len(tracks))

        return tracks
