# -*- coding: utf-8 -*-
"""
Intent Parser
Parses natural language input to extract music generation parameters.
"""

import re
import json
from typing import Dict, Any, Optional
from src.app.models import CompositionSession
from src.app.constants import GENRE_CONFIG, SCALES
from src.app.track_planner import TrackPlanner
from src.config.llm import call_llm, LLMConfig

try:
    from src.midigent.duration_parser import DurationParser
    from src.midigent.duration_validator import DurationValidator, DurationConfig
    DURATION_PARSER_AVAILABLE = True
except ImportError:
    DURATION_PARSER_AVAILABLE = False


class IntentParser:
    """Parse natural language into music parameters."""

    def __init__(self):
        self.track_planner = TrackPlanner()

    def parse(self, user_input: str, session: Optional[CompositionSession] = None) -> Dict[str, Any]:
        """Parse user input with session context.
        
        Args:
            user_input: User's natural language input
            session: Current composition session (optional)
            
        Returns:
            Dictionary with parsed parameters
        """
        if LLMConfig.AVAILABLE_PROVIDERS:
            return self._parse_with_ai(user_input, session)
        return self._parse_with_keywords(user_input, session)

    def _parse_with_ai(self, user_input: str, session: Optional[CompositionSession] = None) -> Dict[str, Any]:
        """Use AI to parse intent with session context."""
        session_context = ""
        if session and session.total_bars > 0:
            track_summary = ", ".join([t.name for t in session.tracks])
            session_context = f"""
CURRENT COMPOSITION:
- Genre: {session.genre}
- Key: {session.key} {session.mode}
- Tempo: {session.tempo} BPM
- Duration: {session.total_bars} bars
- Tracks: {track_summary}

Previous messages: {len(session.messages)}
"""

        system_prompt = f"""You are a music assistant. Extract parameters from natural language.
{session_context}
Return ONLY valid JSON:
{{
  "action": "<new|extend|modify|reset>",
  "genre": "<pop|rock|electronic|lofi|jazz|classical|ambient|cinematic|funk|rnb>",
  "mood": "<descriptive word>",
  "tempo": <60-180 or null>,
  "key": "<C|Dm|F#|etc or null>",
  "energy": "<low|medium|high>",
  "duration_bars": <8|16|32>,
  "modify_target": "<all|melody|bass|drums|etc or null>",
  "changes": "<description of changes or null>"
}}

Action rules:
- "new" = fresh composition (default for first message)
- "extend" = add more bars, add tracks ("add strings", "continue", "more bars")
- "modify" = change existing ("make it faster", "change key", "louder drums")
- "reset" = start over ("new song", "start fresh", "forget that")"""

        result_text = call_llm(
            system_prompt,
            user_input,
            provider=session.llm_provider if session else LLMConfig.DEFAULT_PROVIDER,
            temperature=0.3,
            max_tokens=300
        )
        
        if not result_text:
            return self._parse_with_keywords(user_input, session)
        
        try:
            if "```" in result_text:
                result_text = result_text.split("```")[1].replace("json", "").strip()
            
            result = json.loads(result_text)
            
            # Plan tracks based on parsed result
            genre = result.get("genre", "pop")
            if result.get("action") in ["new", "extend"]:
                result["track_plan"] = self.track_planner.plan_tracks(user_input, genre)
            
            return result

        except Exception as e:
            print(f"AI parsing failed: {e}")
            return self._parse_with_keywords(user_input, session)

    def _parse_with_keywords(self, user_input: str, session: Optional[CompositionSession] = None) -> Dict[str, Any]:
        """Keyword-based parsing fallback."""
        text = user_input.lower()
        
        result = {
            "action": "new",
            "genre": "pop",
            "mood": "",
            "tempo": None,
            "key": None,
            "energy": "medium",
            "duration_bars": 16,
            "modify_target": None,
            "changes": None
        }

        # Detect action
        if session and session.total_bars > 0:
            if any(w in text for w in ["add", "more", "continue", "extend", "another"]):
                result["action"] = "extend"
            elif any(w in text for w in ["change", "make it", "faster", "slower", "louder", "quieter"]):
                result["action"] = "modify"
            elif any(w in text for w in ["new", "start over", "reset", "fresh", "forget"]):
                result["action"] = "reset"
            else:
                result["action"] = "new"

        # Genre
        for genre in GENRE_CONFIG:
            if genre in text:
                result["genre"] = genre
                break

        # Mood and energy
        mood_energy = {
            "happy": ("happy", "high"), "upbeat": ("happy", "high"),
            "sad": ("sad", "low"), "melancholic": ("melancholic", "low"),
            "calm": ("calm", "low"), "relaxing": ("relaxing", "low"),
            "energetic": ("energetic", "high"), "intense": ("intense", "high"),
            "mysterious": ("mysterious", "medium"), "dark": ("dark", "medium"),
            "epic": ("epic", "high"), "peaceful": ("peaceful", "low"),
        }
        for word, (mood, energy) in mood_energy.items():
            if word in text:
                result["mood"] = mood
                result["energy"] = energy
                break

        # Tempo
        tempo_match = re.search(r'(\d{2,3})\s*bpm', text)
        if tempo_match:
            result["tempo"] = int(tempo_match.group(1))
        elif "faster" in text and session:
            result["tempo"] = min(180, session.tempo + 20)
        elif "slower" in text and session:
            result["tempo"] = max(60, session.tempo - 20)

        # Key
        key_match = re.search(r'\b([A-G][#b]?)\s*(major|minor|m)?\b', user_input, re.IGNORECASE)
        if key_match:
            key = key_match.group(1).upper()
            mode = key_match.group(2)
            if mode and mode.lower() in ["minor", "m"]:
                key += "m"
            result["key"] = key

        # Duration
        if DURATION_PARSER_AVAILABLE:
            duration_request = DurationParser.parse(user_input)
            if duration_request:
                tempo = result.get("tempo") or (session.tempo if session else 120)
                config = DurationConfig()
                validation = DurationValidator.validate(duration_request, tempo=tempo, config=config)
                
                if validation.is_valid:
                    if validation.adjusted_value is not None:
                        from src.midigent.duration_models import DurationRequest, DurationUnit
                        adjusted_request = DurationRequest(validation.adjusted_value, DurationUnit.SECONDS)
                        result["duration_bars"] = adjusted_request.to_bars(tempo=tempo)
                        if validation.warning:
                            print(validation.warning)
                    else:
                        result["duration_bars"] = duration_request.to_bars(tempo=tempo)
                        result["duration_confirmation"] = DurationValidator.format_confirmation(duration_request, tempo=tempo)
                else:
                    result["duration_bars"] = 16
                    if validation.message:
                        print(validation.message)
            else:
                if "short" in text:
                    result["duration_bars"] = 8
                elif "long" in text:
                    result["duration_bars"] = 32
        else:
            dur_match = re.search(r'(\d+)\s*bars?', text)
            if dur_match:
                result["duration_bars"] = min(64, int(dur_match.group(1)))
            elif "short" in text:
                result["duration_bars"] = 8
            elif "long" in text:
                result["duration_bars"] = 32

        # Track planning
        result["track_plan"] = self.track_planner.plan_tracks(user_input, result["genre"])

        return result
