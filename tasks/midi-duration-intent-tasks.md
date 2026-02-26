# Implementation Tasks: MIDI Duration Intent Understanding

**Feature**: Intelligent MIDI Duration Parsing  
**Created**: 2026-01-31  
**Status**: Ready for Implementation  

## Prerequisites

- [ ] Review and approve specification document
- [ ] Review and approve implementation plan
- [ ] Set up development environment
- [ ] Create feature branch: `feature/duration-intent-parsing`

## Phase 1: Core Duration Parsing (3-4 hours)

### Task 1.1: Create Duration Models
**File**: `src/duration_models.py`  
**Estimated Time**: 1 hour

- [ ] Create `DurationUnit` enum with values: SECONDS, MINUTES, BARS, BEATS
- [ ] Create `DurationRequest` dataclass with fields: value, unit
- [ ] Implement `to_seconds()` method with tempo/time signature support
- [ ] Implement `to_bars()` method with tempo/time signature conversion
- [ ] Implement `__str__()` method for user-friendly display
- [ ] Create `ValidationResult` dataclass with fields: is_valid, adjusted_value, message, warning
- [ ] Add docstrings to all classes and methods
- [ ] Write unit tests for duration conversions (minutes→seconds, bars→seconds, seconds→bars)
- [ ] Test edge cases: zero, negative, very large values
- [ ] Test different tempos (60, 90, 120, 180 BPM)
- [ ] Test different time signatures (3/4, 4/4, 5/4, 6/8)

### Task 1.2: Create Duration Parser
**File**: `src/duration_parser.py`  
**Estimated Time**: 1.5 hours

- [ ] Create `DurationParser` class
- [ ] Define regex patterns for: minutes (full, abbreviated, shorthand)
- [ ] Define regex patterns for: seconds (full, abbreviated, shorthand)
- [ ] Define regex patterns for: MM:SS format
- [ ] Define regex patterns for: bars
- [ ] Define regex patterns for: beats
- [ ] Implement `parse()` method with pattern matching
- [ ] Implement `parse_with_fallback()` method with default duration
- [ ] Add comprehensive docstrings with examples
- [ ] Write unit test: parse "5 minutes" → DurationRequest(5, MINUTES)
- [ ] Write unit test: parse "5 min" → DurationRequest(5, MINUTES)
- [ ] Write unit test: parse "5m" → DurationRequest(5, MINUTES)
- [ ] Write unit test: parse "30 seconds" → DurationRequest(30, SECONDS)
- [ ] Write unit test: parse "2:30" → DurationRequest(150, SECONDS)
- [ ] Write unit test: parse "32 bars" → DurationRequest(32, BARS)
- [ ] Write unit test: parse "no duration" → None
- [ ] Write unit test: parse_with_fallback returns default
- [ ] Write unit test: case insensitivity
- [ ] Write unit test: handles multiple numbers (returns first duration found)

### Task 1.3: Create Duration Validator
**File**: `src/duration_validator.py`  
**Estimated Time**: 1 hour

- [ ] Create `DurationConfig` class with constraints: MIN_DURATION_SECONDS, MAX_DURATION_SECONDS, DEFAULT_DURATION_SECONDS
- [ ] Add config fields: STRICT_VALIDATION, SHOW_WARNINGS, SHOW_CONFIRMATION
- [ ] Create `DurationValidator` class
- [ ] Implement `validate()` method checking minimum duration
- [ ] Implement `validate()` method checking maximum duration
- [ ] Handle strict vs non-strict validation modes
- [ ] Implement `format_confirmation()` method for user-friendly messages
- [ ] Add docstrings explaining validation behavior
- [ ] Write unit test: validate normal duration (60 seconds) → valid
- [ ] Write unit test: validate too short (2 seconds) in non-strict mode → clamped to min
- [ ] Write unit test: validate too short (2 seconds) in strict mode → invalid
- [ ] Write unit test: validate too long (900 seconds) in non-strict mode → clamped to max
- [ ] Write unit test: validate too long (900 seconds) in strict mode → invalid
- [ ] Write unit test: confirmation message formatting
- [ ] Write unit test: confirmation shows conversions (bars, seconds, minutes)

## Phase 2: Integration (2-3 hours)

### Task 2.1: Integrate into Generation Pipeline
**File**: `src/midi_generator.py` (or your equivalent)  
**Estimated Time**: 1.5 hours

- [ ] Import duration parsing modules
- [ ] Create/modify `generate_midi_with_intent()` function
- [ ] Add logic to check for explicit duration parameters first
- [ ] Add logic to extract duration from user prompt
- [ ] Add duration validation step
- [ ] Handle validation failures (warnings vs errors)
- [ ] Show confirmation message to user
- [ ] Convert validated duration to seconds and bars
- [ ] Pass calculated duration to internal generation function
- [ ] Update function signature with optional duration parameters
- [ ] Add comprehensive docstring with examples
- [ ] Write integration test: prompt with "5 minutes" generates ~300 second track
- [ ] Write integration test: prompt with "32 bars" generates correct bar count
- [ ] Write integration test: prompt exceeding max gets clamped
- [ ] Write integration test: prompt with no duration uses default

### Task 2.2: Update UI/CLI Integration
**File**: UI handler or CLI entry point  
**Estimated Time**: 1 hour

- [ ] Update prompt input placeholder to show duration examples
- [ ] Add tooltip/info text explaining duration formats
- [ ] Update duration slider/input to allow None (extract from prompt)
- [ ] Wire duration parser into UI event handlers
- [ ] Display confirmation messages in UI
- [ ] Display warning messages when duration adjusted
- [ ] Test UI with various duration inputs
- [ ] Ensure error messages are user-friendly
- [ ] Add "Duration extracted: X" indicator in UI
- [ ] Update UI documentation/help text

## Phase 3: Testing & Quality Assurance (2-3 hours)

### Task 3.1: Comprehensive Unit Testing
**File**: `tests/test_duration_*.py`  
**Estimated Time**: 1 hour

- [ ] Ensure all unit tests from Phase 1 pass
- [ ] Add edge case tests: empty string, None, whitespace only
- [ ] Add edge case tests: multiple durations in one prompt
- [ ] Add edge case tests: conflicting durations (should use first)
- [ ] Add edge case tests: decimal values ("2.5 minutes")
- [ ] Add edge case tests: very large numbers
- [ ] Test with non-English characters (should fail gracefully)
- [ ] Test with malformed input (should return None)
- [ ] Verify all tests have good coverage (aim for >90%)
- [ ] Run tests with pytest and check coverage report

### Task 3.2: Integration Testing
**File**: `tests/test_integration.py`  
**Estimated Time**: 1 hour

- [ ] Test full pipeline: prompt → parse → validate → generate → output
- [ ] Test with real MIDI generation (if available)
- [ ] Verify generated MIDI file actual duration matches requested
- [ ] Test concurrent requests with different durations
- [ ] Test error handling end-to-end
- [ ] Test with various styles/genres
- [ ] Test with various tempos (slow, medium, fast)
- [ ] Verify memory usage doesn't spike with long durations
- [ ] Check for resource leaks

### Task 3.3: Manual Testing & User Acceptance
**Estimated Time**: 1 hour

- [ ] Create manual test script with real user prompts
- [ ] Test: "Generate 5 minutes of ambient music"
- [ ] Test: "Create a 2:30 track"
- [ ] Test: "Make 32 bars of jazz"
- [ ] Test: "Epic 10 minute composition"
- [ ] Test: "15 minute symphony" (should hit max limit)
- [ ] Test: "Quick jingle" (should use default)
- [ ] Test: "30 second intro"
- [ ] Test: "1 min loop"
- [ ] Verify all confirmation messages are clear
- [ ] Verify all warning messages are helpful
- [ ] Test in actual UI (if applicable)
- [ ] Get feedback from beta users (if available)

## Phase 4: Documentation & Deployment (1-2 hours)

### Task 4.1: Code Documentation
**Estimated Time**: 30 minutes

- [ ] Review all docstrings for completeness
- [ ] Add inline comments for complex logic
- [ ] Update module-level documentation
- [ ] Add type hints to all functions
- [ ] Ensure code follows project style guide
- [ ] Run linter and fix any issues
- [ ] Generate API documentation (if applicable)

### Task 4.2: User Documentation
**File**: `docs/duration-feature.md` and README updates  
**Estimated Time**: 30 minutes

- [ ] Create user guide for duration feature
- [ ] Add examples of supported formats
- [ ] Document system limits (min/max/default)
- [ ] Add troubleshooting section
- [ ] Update main README with duration feature
- [ ] Add FAQ section
- [ ] Include screenshots/examples (if UI-based)

### Task 4.3: Changelog & Release Notes
**Estimated Time**: 15 minutes

- [ ] Update CHANGELOG.md with new feature
- [ ] Write release notes highlighting duration feature
- [ ] Document any breaking changes (if any)
- [ ] List migration steps (if needed)

### Task 4.4: Deployment
**Estimated Time**: 15 minutes

- [ ] Create pull request with all changes
- [ ] Request code review
- [ ] Address review feedback
- [ ] Merge to main branch
- [ ] Tag release version
- [ ] Deploy to staging environment
- [ ] Run smoke tests in staging
- [ ] Deploy to production
- [ ] Monitor error logs for 24 hours
- [ ] Announce feature to users

## Quality Gates

### Before Phase 2
- [ ] All Phase 1 unit tests pass
- [ ] Code review completed for Phase 1
- [ ] No critical bugs found

### Before Phase 4
- [ ] All tests pass (unit + integration)
- [ ] Code coverage >90%
- [ ] Performance benchmarks met
- [ ] No memory leaks detected
- [ ] User acceptance testing completed

### Before Production Deployment
- [ ] All documentation complete
- [ ] Staging tests pass
- [ ] Security review completed (if applicable)
- [ ] Rollback plan documented
- [ ] Monitoring/alerting configured

## Risk Mitigation Checklist

- [ ] Backup plan if parsing fails: fall back to default duration
- [ ] Validation prevents crashes from extreme values
- [ ] Clear error messages help users understand issues
- [ ] Feature flag available to disable if issues arise
- [ ] Monitoring in place to detect parsing failures
- [ ] User feedback channel established

## Success Metrics (Post-Deployment)

- [ ] Monitor parsing success rate (target: >95%)
- [ ] Track user satisfaction scores
- [ ] Measure error rate for duration-related failures
- [ ] Collect user feedback on duration feature
- [ ] Analyze most common duration requests
- [ ] Identify any parsing edge cases missed

## Notes & Considerations

- **Backward Compatibility**: Existing explicit duration parameters should still work
- **Performance**: Parsing adds minimal overhead (<1ms per request)
- **Localization**: Current implementation is English-only; future versions could support other languages
- **Extensibility**: Architecture allows easy addition of new duration formats (e.g., "half an hour")

---

**Ready to Start?**
Begin with Phase 1, Task 1.1. Check off each item as you complete it.

**Questions?**
Refer to the specification and implementation plan documents for detailed context.
