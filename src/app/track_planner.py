# -*- coding: utf-8 -*-
"""
Track Planning Engine
Plans track configuration based on user input and genre.
"""

import json
import re
import random
from typing import List, Optional
from src.app.models import TrackConfig
from src.app.constants import GENRE_CONFIG
from src.config.llm import call_llm, LLMConfig


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
            requested_count = self._extract_track_count(user_prompt)
        
        print(f"🎵 Track Planning: Requested count = {requested_count}")
        
        if LLMConfig.AVAILABLE_PROVIDERS:
            tracks = self._plan_with_ai(user_prompt, genre, requested_count)
        else:
            tracks = self._plan_with_rules(user_prompt, genre, requested_count)
        
        print(f"🎵 Track Planning: Generated {len(tracks)} track configs")
        
        if requested_count and len(tracks) != requested_count:
            print(f"⚠️  Track count mismatch! Requested {requested_count}, got {len(tracks)}. Adjusting...")
            tracks = self._ensure_track_count(tracks, requested_count, genre)
            print(f"🎵 Track Planning: Adjusted to {len(tracks)} tracks")
        
        return tracks

    def _extract_track_count(self, text: str) -> Optional[int]:
        """Extract explicit track count from prompt."""
        patterns = [
            r'(\d+)\s*tracks?',
            r'(one|two|three|four|five|six|seven|eight)\s*tracks?',
        ]
        
        number_words = {
            "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "six": 6, "seven": 7, "eight": 8
        }
        
        text_lower = text.lower()
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                value = match.group(1)
                if value.isdigit():
                    return int(value)
                elif value in number_words:
                    return number_words[value]
        
        return None

    def _plan_with_ai(self, user_prompt: str, genre: str, requested_count: Optional[int] = None) -> List[TrackConfig]:
        """Use AI to plan tracks."""
        track_count_requirement = ""
        if requested_count:
            track_count_requirement = f"\n\n**CRITICAL REQUIREMENT**: User explicitly requested EXACTLY {requested_count} tracks. You MUST return exactly {requested_count} tracks in the tracks array."
        
        system_prompt = f"""Analyze this music request and determine the optimal track configuration.
Return ONLY valid JSON (no markdown, no explanation):
{{
  "total_tracks": <1-8>,
  "tracks": [
    {{"type": "<lead|counter_melody|harmony|bass|drums|arpeggio|pad|fx>", "instrument": "<instrument>", "role": "<purpose>", "priority": <1-8>}}
  ]
}}

Rules:
- Solo instrument requests = 1-2 tracks
- Simple requests = 2-3 tracks
- Standard arrangements = 4-5 tracks
- Rich/orchestral/epic = 6-8 tracks
- NEVER exceed 8 tracks
- Match instruments to genre conventions
- Types: lead (melody), counter_melody, harmony (chords), bass, drums, arpeggio, pad, fx{track_count_requirement}"""

        result_text = call_llm(
            system_prompt,
            f"Genre: {genre}\nRequest: {user_prompt}",
            temperature=0.3,
            max_tokens=500
        )
        
        if not result_text:
            return self._plan_with_rules(user_prompt, genre)
        
        try:
            if "```" in result_text:
                result_text = result_text.split("```")[1].replace("json", "").strip()
            
            data = json.loads(result_text)
            
            tracks = []
            for i, t in enumerate(data.get("tracks", [])[:8]):
                tracks.append(TrackConfig(
                    track_type=t.get("type", "lead"),
                    instrument=t.get("instrument", "piano"),
                    role=t.get("role", ""),
                    priority=t.get("priority", i + 1),
                    channel=i if t.get("type") != "drums" else 9
                ))
            return tracks if tracks else self._plan_with_rules(user_prompt, genre)
            
        except Exception as e:
            print(f"AI track planning failed: {e}")
            return self._plan_with_rules(user_prompt, genre)

    def _ensure_track_count(self, tracks: List[TrackConfig], requested_count: int, genre: str) -> List[TrackConfig]:
        """Ensure track plan has exactly requested_count tracks."""
        current_count = len(tracks)
        
        if current_count == requested_count:
            return tracks
        
        elif current_count < requested_count:
            additional_needed = requested_count - current_count
            print(f"  Adding {additional_needed} tracks to reach {requested_count}")
            
            track_priority = [
                ("harmony", "electric_piano", "Harmonic support"),
                ("bass", "bass", "Bass line"),
                ("drums", "drums", "Rhythm section"),
                ("arpeggio", "synth_lead", "Arpeggio pattern"),
                ("pad", "synth_pad", "Atmospheric pad"),
                ("counter_melody", "flute", "Counter melody"),
                ("fx", "fx_atmosphere", "Sound effects"),
            ]
            
            existing_types = [t.track_type for t in tracks]
            
            for i in range(additional_needed):
                for track_type, instrument, role in track_priority:
                    if track_type not in existing_types:
                        tracks.append(TrackConfig(
                            track_type=track_type,
                            instrument=instrument,
                            role=role,
                            priority=current_count + i + 1,
                            channel=(current_count + i) % 9 if track_type != "drums" else 9
                        ))
                        existing_types.append(track_type)
                        break
                else:
                    track_type, instrument, role = track_priority[i % len(track_priority)]
                    tracks.append(TrackConfig(
                        track_type=track_type,
                        instrument=instrument,
                        role=f"{role} {i+1}",
                        priority=current_count + i + 1,
                        channel=(current_count + i) % 9 if track_type != "drums" else 9
                    ))
        
        else:
            print(f"  Removing {current_count - requested_count} tracks to reach {requested_count}")
            tracks = sorted(tracks, key=lambda t: t.priority)[:requested_count]
        
        return tracks

    def _plan_with_rules(self, user_prompt: str, genre: str, requested_count: Optional[int] = None) -> List[TrackConfig]:
        """Rule-based track planning fallback."""
        prompt_lower = user_prompt.lower()
        tracks = []
        
        if requested_count:
            print(f"  Building {requested_count} tracks (explicit request)")
            base_tracks = [
                ("lead", "piano", "Main melody"),
                ("harmony", "electric_piano", "Chords"),
                ("bass", "bass", "Bass line"),
                ("drums", "drums", "Rhythm"),
                ("arpeggio", "synth_lead", "Arpeggio"),
                ("pad", "synth_pad", "Atmosphere"),
                ("counter_melody", "flute", "Counter melody"),
                ("fx", "fx_atmosphere", "Effects"),
            ]
            
            for i in range(min(requested_count, 8)):
                track_type, instrument, role = base_tracks[i % len(base_tracks)]
                tracks.append(TrackConfig(
                    track_type=track_type,
                    instrument=instrument,
                    role=role,
                    priority=i + 1,
                    channel=i if track_type != "drums" else 9
                ))
            
            return tracks
        
        is_simple = any(w in prompt_lower for w in ["solo", "simple", "minimal", "just", "only"])
        is_rich = any(w in prompt_lower for w in ["epic", "orchestral", "full", "rich", "complex", "cinematic"])
        
        has_piano = "piano" in prompt_lower
        has_guitar = "guitar" in prompt_lower
        has_strings = "string" in prompt_lower
        has_synth = "synth" in prompt_lower
        
        if is_simple:
            instrument = "piano"
            if has_guitar: instrument = "guitar"
            elif has_strings: instrument = "strings"
            elif has_synth: instrument = "synth_lead"
            
            tracks.append(TrackConfig("lead", instrument, "Main melody", 1, 0))
            if not any(w in prompt_lower for w in ["solo", "just", "only"]):
                tracks.append(TrackConfig("harmony", "electric_piano", "Light harmony", 2, 1))
        
        elif is_rich:
            tracks = [
                TrackConfig("lead", "strings", "Main melody", 1, 0),
                TrackConfig("counter_melody", "flute", "Counter line", 2, 1),
                TrackConfig("harmony", "synth_pad", "Harmonic bed", 3, 2),
                TrackConfig("pad", "choir", "Atmosphere", 4, 3),
                TrackConfig("bass", "synth_bass", "Low end", 5, 4),
                TrackConfig("drums", "drums", "Rhythm", 6, 9),
                TrackConfig("arpeggio", "piano", "Movement", 7, 5),
            ]
            if random.random() > 0.5:
                tracks.append(TrackConfig("fx", "fx_atmosphere", "Texture", 8, 6))
        
        else:
            config = GENRE_CONFIG.get(genre, GENRE_CONFIG["pop"])
            tracks.append(TrackConfig("lead", "piano", "Main melody", 1, 0))
            tracks.append(TrackConfig("harmony", "electric_piano", "Chords", 2, 1))
            tracks.append(TrackConfig("bass", "bass", "Bass line", 3, 2))
            
            if genre not in ["ambient", "classical"] or "drum" in prompt_lower:
                tracks.append(TrackConfig("drums", "drums", "Rhythm", 4, 9))
            
            if genre in ["electronic", "lofi"]:
                tracks.append(TrackConfig("arpeggio", "synth_lead", "Arpeggio", 5, 3))
            elif genre in ["ambient", "cinematic"]:
                tracks.append(TrackConfig("pad", "synth_pad", "Atmosphere", 5, 3))

        return tracks
