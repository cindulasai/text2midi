"""
Track Planner Node: Create optimal track configuration based on intent.
Uses emotion-aware instrument selection for versatile music generation.
"""

import json
from typing import List

from src.agents.state import MusicState, MusicIntent, TrackConfig
from src.config.llm import LLMConfig, call_llm

try:
    from src.midigent.emotion_instruments import EmotionAwareInstrumentMapper
    EMOTION_MAPPER_AVAILABLE = True
except ImportError:
    EMOTION_MAPPER_AVAILABLE = False


def track_planner_node(state: MusicState) -> MusicState:
    """
    Agent Node: Create optimal track configuration with emotion awareness.
    
    Uses emotion-aware instrument selection to ensure:
    - Different moods get different instrument colors
    - Styles are reflected in track arrangement
    - Genre conventions are respected
    - Track generation is versatile and responsive
    """
    print("\n[MUSIC] [TRACK PLANNER AGENT] Planning emotion-aware track configuration...")
    
    if state.get("error"):
        return state
    
    intent = state.get("intent")
    if not intent:
        state["error"] = "No intent available for track planning"
        return state
    
    try:
        # Extract extended intent information
        # Prefer the richer ParsedIntent when available (from LLM Intent Engine)
        parsed_intent = state.get("parsed_intent")  # Set by new engine
        emotions = getattr(intent, 'emotions', []) or []
        style_descriptors = intent.style_descriptors or []
        specific_instruments = intent.specific_instruments or []

        # If the new engine stored instrument confidence data, use it to
        # decide whether to trust user-specified instruments or let the
        # planner choose freely.
        instrument_confidence = 0.5
        if parsed_intent is not None:
            try:
                from src.intent.schema import ParsedIntent
                if isinstance(parsed_intent, ParsedIntent) and parsed_intent.instruments:
                    min_conf = min(
                        (inst.priority / 10.0 for inst in parsed_intent.instruments),
                        default=0.5,
                    )
                    instrument_confidence = min_conf
            except ImportError:
                pass

        print(f"   Emotions: {emotions if emotions else 'Not specified'}")
        print(f"   Styles: {style_descriptors if style_descriptors else 'Not specified'}")
        if instrument_confidence >= 0.7:
            print(f"   Instruments: high-confidence user request → preserving")
        else:
            print(f"   Instruments: low-confidence → planner may override")

        if LLMConfig.DEFAULT_PROVIDER:
            track_plan = _plan_tracks_with_ai(intent)
        else:
            track_plan = _plan_tracks_with_rules(intent)
        
        # Enhance with emotion-aware instruments if available.
        # Skip emotion override when user explicitly specified instruments
        # with high confidence (the LLM Intent Engine already validated them).
        if EMOTION_MAPPER_AVAILABLE and (emotions or style_descriptors) and instrument_confidence < 0.7:
            track_plan = _enhance_with_emotion_instruments(
                track_plan, 
                intent.genre,
                emotions,
                style_descriptors,
                specific_instruments
            )
        elif specific_instruments and instrument_confidence >= 0.7:
            print("   ✓ Keeping user-specified instruments (high confidence)")
        
        # Ensure track count matches request
        if intent.track_count and len(track_plan) != intent.track_count:
            print(f"[WARN] Adjusting track count from {len(track_plan)} to {intent.track_count}")
            track_plan = _ensure_track_count(track_plan, intent.track_count, intent.genre)
        
        state["track_plan"] = track_plan
        print(f"[OK] Track plan created: {len(track_plan)} emotion-aware tracks")
        for i, track in enumerate(track_plan, 1):
            print(f"   {i}. {track.track_type:15} | {track.instrument:20} | Priority: {track.priority}")
        
    except Exception as e:
        import traceback
        state["error"] = f"Track planning failed: {str(e)}\n{traceback.format_exc()}"
        print(f"[ERROR] Error: {state['error']}")
    
    return state


def _enhance_with_emotion_instruments(
    base_tracks: List[TrackConfig],
    genre: str,
    emotions: List[str],
    style_descriptors: List[str],
    specific_instruments: List[str] = None
) -> List[TrackConfig]:
    """
    Enhance track plan with emotion-aware instrument selection.
    Replaces generic instruments with genre/emotion-appropriate ones.
    """
    if not base_tracks:
        return base_tracks
    
    try:
        # Get emotion-aware instrument recommendations
        emotion_instruments = EmotionAwareInstrumentMapper.select_instruments_for_intent(
            genre=genre,
            emotions=emotions,
            style_descriptors=style_descriptors,
            track_count=len(base_tracks),
            specific_instruments=specific_instruments
        )
        
        # Map emotion instruments to track plan
        enhanced_tracks = []
        for i, base_track in enumerate(base_tracks):
            if i < len(emotion_instruments):
                emotion_inst = emotion_instruments[i]
                
                # Keep the track type logic but update instrument
                enhanced_track = TrackConfig(
                    track_type=emotion_inst.get("track_type", base_track.track_type),
                    instrument=emotion_inst.get("instrument", base_track.instrument),
                    role=f"{base_track.role} ({emotion_inst.get('instrument', 'unknown')})",
                    priority=emotion_inst.get("priority", base_track.priority),
                    channel=emotion_inst.get("channel", base_track.channel)
                )
                enhanced_tracks.append(enhanced_track)
            else:
                enhanced_tracks.append(base_track)
        
        print("   ✓ Enhanced with emotion-aware instruments")
        return enhanced_tracks
    
    except Exception as e:
        print(f"   ⚠️  Emotion mapping failed: {e}, using base tracks")
        return base_tracks


def _plan_tracks_with_ai(intent: MusicIntent) -> List[TrackConfig]:
    """Use the central LLM client to plan tracks based on intent."""
    track_count_req = (
        f"\n**CRITICAL**: User requested EXACTLY {intent.track_count} tracks."
        if intent.track_count else ""
    )
    system_prompt = f"""You are a music producer planning track arrangements.
Analyze the user request and return ONLY valid JSON:
{{
  "tracks": [
    {{"type": "<lead|counter_melody|harmony|bass|drums|arpeggio|pad|fx>",
      "instrument": "<instrument>",
      "role": "<description>",
      "priority": <1-8>}}
  ]
}}
Rules:
- Return exactly the number of tracks requested (or infer from description)
- Match instruments to genre
- Prioritize coherent arrangement
- Never exceed 8 tracks{track_count_req}"""

    user_message = f"Genre: {intent.genre}, Request: {intent.raw_prompt}"

    try:
        result_text = call_llm(system_prompt, user_message, temperature=0.3, max_tokens=500)
        if not result_text:
            return _plan_tracks_with_rules(intent)

        if "```" in result_text:
            result_text = result_text.split("```")[1].replace("json", "").strip()

        data = json.loads(result_text)
        tracks = [
            TrackConfig(
                track_type=t.get("type", "lead"),
                instrument=t.get("instrument", "piano"),
                role=t.get("role", ""),
                priority=t.get("priority", i + 1),
                channel=i if t.get("type") != "drums" else 9,
            )
            for i, t in enumerate(data.get("tracks", [])[:8])
        ]
        return tracks if tracks else _plan_tracks_with_rules(intent)

    except Exception as exc:
        print(f"AI planning failed: {exc}, using rules-based")
        return _plan_tracks_with_rules(intent)


def _plan_tracks_with_rules(intent: MusicIntent) -> List[TrackConfig]:
    """Rule-based track planning fallback."""
    specific_instruments = intent.specific_instruments or []
    needs_drums = any(
        kw in " ".join(specific_instruments).lower()
        for kw in ("drums", "percussion", "beat", "drum")
    )
    track_count = intent.track_count or _infer_track_count(intent.energy, intent.mood)

    # Genres that should always have a beat/drum track
    RHYTHMIC_GENRES = {"lofi", "rock", "funk", "pop", "rnb", "electronic", "hip hop", "hiphop"}
    if intent.genre in RHYTHMIC_GENRES:
        needs_drums = True

    base_tracks = [
        ("lead", "piano", "Main melody"),
        ("harmony", "electric_piano", "Harmonic support"),
        ("bass", "bass", "Bass line"),
        ("drums", "drums", "Rhythm section"),
        ("arpeggio", "synth_lead", "Arpeggio pattern"),
        ("pad", "synth_pad", "Atmospheric pad"),
        ("counter_melody", "flute", "Counter melody"),
        ("fx", "fx_atmosphere", "Sound effects"),
    ]

    tracks = []
    for i in range(min(track_count, 8)):
        track_type, instrument, role = base_tracks[i % len(base_tracks)]
        tracks.append(TrackConfig(
            track_type=track_type,
            instrument=instrument,
            role=role,
            priority=i + 1,
            channel=i if track_type != "drums" else 9
        ))

    # If drums were explicitly requested or genre demands them, ensure they are present
    if needs_drums and not any(t.track_type == "drums" for t in tracks):
        tracks.append(TrackConfig(
            track_type="drums",
            instrument="drums",
            role="Rhythm section",
            priority=len(tracks) + 1,
            channel=9
        ))

    return tracks


def _infer_track_count(energy: str, mood: str) -> int:
    """Infer track count from energy and mood."""
    energy_map = {"low": 2, "medium": 4, "high": 6}
    base = energy_map.get(energy, 4)
    
    if "epic" in mood.lower() or "orchestral" in mood.lower():
        return min(base + 2, 8)
    elif "simple" in mood.lower() or "solo" in mood.lower():
        return max(base - 2, 1)
    
    return base


def _ensure_track_count(tracks: List[TrackConfig], requested: int, genre: str) -> List[TrackConfig]:
    """Adjust track list to match requested count."""
    if len(tracks) == requested:
        return tracks
    
    if len(tracks) < requested:
        # Add tracks
        priority_order = [
            ("harmony", "electric_piano", "Harmonic support"),
            ("bass", "bass", "Bass line"),
            ("drums", "drums", "Rhythm"),
            ("arpeggio", "synth_lead", "Arpeggio"),
            ("pad", "synth_pad", "Atmosphere"),
            ("counter_melody", "flute", "Counter"),
            ("fx", "fx_atmosphere", "Effects"),
        ]
        
        existing_types = {t.track_type for t in tracks}
        current_count = len(tracks)
        
        for i in range(requested - current_count):
            for track_type, instrument, role in priority_order:
                if track_type not in existing_types:
                    tracks.append(TrackConfig(
                        track_type=track_type,
                        instrument=instrument,
                        role=role,
                        priority=current_count + i + 1,
                        channel=(current_count + i) % 9 if track_type != "drums" else 9
                    ))
                    existing_types.add(track_type)
                    break
    else:
        # Remove lowest priority tracks
        tracks = sorted(tracks, key=lambda t: t.priority)[:requested]
    
    return tracks
