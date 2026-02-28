# -*- coding: utf-8 -*-
"""
__init__ for agents module - Exports main components.
"""

from src.agents.state import MusicState, MusicIntent, TrackConfig
from src.agents.intent_parser_node import intent_parser_node
from src.agents.track_planner_node import track_planner_node
from src.agents.theory_validator_node import music_theory_validator_node
from src.agents.track_generator_node import track_generator_node
from src.agents.quality_control_node import quality_control_agent_node
from src.agents.refinement_node import refinement_agent_node
from src.agents.midi_creator_node import midi_creation_agent_node
from src.agents.session_summary_node import session_summary_agent_node
from src.agents.graph import (
    build_music_generation_graph,
    get_agentic_graph,
    describe_graph,
)

__all__ = [
    # State
    "MusicState",
    "MusicIntent",
    "TrackConfig",
    # Nodes
    "intent_parser_node",
    "track_planner_node",
    "music_theory_validator_node",
    "track_generator_node",
    "quality_control_agent_node",
    "refinement_agent_node",
    "midi_creation_agent_node",
    "session_summary_agent_node",
    # Graph
    "build_music_generation_graph",
    "get_agentic_graph",
    "describe_graph",
]
