# -*- coding: utf-8 -*-
"""
LangGraph workflow builder for agentic music generation.
Defines the complete graph structure with all nodes, edges, and routing logic.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import Literal

from src.agents.state import MusicState
from src.agents.intent_parser_node import intent_parser_node
from src.agents.track_planner_node import track_planner_node
from src.agents.theory_validator_node import music_theory_validator_node
from src.agents.track_generator_node import track_generator_node
from src.agents.quality_control_node import quality_control_agent_node, quality_control_router
from src.agents.refinement_node import refinement_agent_node, refinement_router
from src.agents.midi_creator_node import midi_creation_agent_node
from src.agents.session_summary_node import session_summary_agent_node


def build_music_generation_graph():
    """
    Build the complete LangGraph for agentic music generation.
    
    Graph Flow:
    1. Intent Parser → Understand user request
    2. Track Planner → Plan optimal track configuration
    3. Theory Validator → Validate music theory choices
    4. Track Generator → Generate musical tracks
    5. Quality Control → Assess quality (conditional refinement)
    6. [Optional Refinement] → Fix issues if needed
    7. MIDI Creator → Create final MIDI file
    8. Session Summary → Generate summary
    """
    
    graph = StateGraph(MusicState)
    
    # ============== ADD NODES ==============
    
    # Understanding phase
    graph.add_node("intent_parser", intent_parser_node)
    
    # Planning phase
    graph.add_node("track_planner", track_planner_node)
    
    # Validation phase
    graph.add_node("theory_validator", music_theory_validator_node)
    
    # Generation phase
    graph.add_node("track_generator", track_generator_node)
    
    # Quality assurance phase
    graph.add_node("quality_control", quality_control_agent_node)
    
    # Optional refinement
    graph.add_node("refinement", refinement_agent_node)
    
    # Output phase
    graph.add_node("midi_creator", midi_creation_agent_node)
    graph.add_node("session_summary", session_summary_agent_node)
    
    # ============== ADD EDGES ==============
    
    # Linear flow for main path
    graph.add_edge(START, "intent_parser")
    graph.add_edge("intent_parser", "track_planner")
    graph.add_edge("track_planner", "theory_validator")
    graph.add_edge("theory_validator", "track_generator")
    graph.add_edge("track_generator", "quality_control")
    
    # Conditional: Quality check determines if refinement needed
    graph.add_conditional_edges(
        "quality_control",
        quality_control_router,
        {
            "refine": "refinement",
            "finalize": "midi_creator",
        }
    )
    
    # Refinement can loop back to quality check or proceed to finalization
    graph.add_conditional_edges(
        "refinement",
        refinement_router,
        {
            "recheck": "quality_control",
            "finalize": "midi_creator",
        }
    )
    
    # Finalization flow
    graph.add_edge("midi_creator", "session_summary")
    graph.add_edge("session_summary", END)
    
    # Compile with memory
    return graph.compile(checkpointer=MemorySaver())


def get_agentic_graph():
    """

    """
    return build_music_generation_graph()


# ============== GRAPH INTROSPECTION ==============

def describe_graph():
    """Print a human-readable description of the graph structure."""
    description = """
╔════════════════════════════════════════════════════════════════╗
║         MidiGen Agentic Architecture (LangGraph)              ║
╚════════════════════════════════════════════════════════════════╝

WORKFLOW PHASES:
═══════════════════════════════════════════════════════════════

1️⃣  UNDERSTANDING
   └─ intent_parser: Parse user request, extract musical intent
      (Genre, energy, mood, track count, tempo, key)

2️⃣  PLANNING  
   └─ track_planner: Plan optimal track configuration
      (Instruments, roles, priorities for each track)

3️⃣  VALIDATION
   └─ theory_validator: Validate music theory choices
      (Check genre fit, harmonic/melodic balance, rhythm section)

4️⃣  GENERATION
   └─ track_generator: Generate actual musical tracks
      (Create MIDI notes for each track type in parallel)

5️⃣  QUALITY ASSURANCE
   ├─ quality_control: Assess track quality
   │  (Check diversity, density, balance, velocity variation)
   │
   ├─ [CONDITIONAL LOOP]
   │  If issues found + iterations remaining:
   │  └─ refinement: Fix problematic tracks → re-check quality
   │
   └─ Continue if quality acceptable or max iterations reached

6️⃣  OUTPUT
   ├─ midi_creator: Create and save MIDI file
   └─ session_summary: Generate summary

CONDITIONAL ROUTING:
═══════════════════════════════════════════════════════════════

Quality Control Router:
  ├─ If needs_refinement AND iterations remaining → "refine"
  └─ Otherwise → "finalize"

Refinement Router:
  ├─ If iterations remaining → "recheck" (loop to quality_control)
  └─ Otherwise → "finalize" (skip to midi_creator)

ERROR HANDLING:
═══════════════════════════════════════════════════════════════
• Each node checks for errors in state
• If error found, node skips processing
• On error, graph routes to session_summary for clean shutdown

STATE MANAGEMENT:
═══════════════════════════════════════════════════════════════
• Checkpointing: MemorySaver (can be upgraded to SQLite)
• Thread-safe sessions: Each composition gets unique thread_id
• Full state persistence: Can save/resume sessions

AGENT SPECIALIZATIONS:
═══════════════════════════════════════════════════════════════
• Intent Parser: NLP-based (uses Groq LLM when available)
• Track Planner: AI-guided with rule-based fallback
• Theory Validator: Music theory domain knowledge
• Track Generator: Statistical generation per track type
• Quality Control: Heuristic-based assessment
• Refinement: Parameter-based regeneration
• MIDI Creator: Standard MIDI file format
• Session Summary: Natural language generation

IMPROVEMENTS OVER MONOLITHIC:
═══════════════════════════════════════════════════════════════
✓ Separation of concerns: Each agent has single responsibility
✓ Self-reflection: Quality agent decides if refinement needed
✓ State transparency: Full state available at each step
✓ Conditional execution: Routes depend on state evaluation
✓ Memory & persistence: Can resume sessions
✓ Extensibility: Easy to add new agents/nodes
✓ Testability: Each agent/node can be tested independently
✓ Parallel-ready: Multiple agents could run in parallel
"""
    return description
