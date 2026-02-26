# MidiGen v2.0 Implementation Plan

## Overview
Implement dynamic track generation and multi-turn conversation capabilities.

---

## Task Checklist

### Phase 1: Dynamic Track Planning
- [ ] 1.1 Create TrackConfig dataclass
- [ ] 1.2 Create TrackPlanner class with AI track analysis
- [ ] 1.3 Add new track type generators (counter_melody, arpeggio, pad, fx)
- [ ] 1.4 Update IntentParser to include track planning
- [ ] 1.5 Modify process_message to use dynamic tracks

### Phase 2: Session Management  
- [ ] 2.1 Create CompositionSession dataclass
- [ ] 2.2 Create SessionManager class
- [ ] 2.3 Add session state tracking to MidiGenApp
- [ ] 2.4 Update AI prompts with session context

### Phase 3: Multi-Turn Actions
- [ ] 3.1 Implement action detection (extend/modify/section/reset)
- [ ] 3.2 Create extend_composition() method
- [ ] 3.3 Create modify_tracks() method  
- [ ] 3.4 Implement MIDI merging for extensions
- [ ] 3.5 Add section management (verse, chorus, bridge)

### Phase 4: UI Enhancements
- [ ] 4.1 Add session state panel to UI
- [ ] 4.2 Add track list visualization
- [ ] 4.3 Add suggested actions after generation
- [ ] 4.4 Improve export options

---

## Current Task: Phase 1.1 - TrackConfig Dataclass

Starting implementation now.
