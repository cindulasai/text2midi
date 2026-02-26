# MidiGen AI Skills

This folder contains reusable prompts, patterns, and knowledge that inform AI assistant behavior when working with MidiGen.

## Available Skills

### 1. Code Review Checklist
See `code_review.md` - Guidelines for reviewing MidiGen code

### 2. Music Generation Patterns
See `music_patterns.md` - Music theory and generation patterns

### 3. Refactoring Strategies
See `refactoring.md` - How to refactor and improve MidiGen code

### 4. Documentation Standards
See `documentation.md` - Writing effective documentation

## Constitution

Project principles are defined in [../constitution.md](../constitution.md)

## Quick Reference

### Module Purposes
- `src/app/models.py` - Data structures
- `src/app/generator.py` - Music generation logic
- `src/app/intent_parser.py` - NLP understanding
- `src/config/llm.py` - LLM provider management

### Common Patterns
- Use dataclasses for data structures
- Type hint all function signatures
- Include docstrings with Args/Returns
- Validate inputs early and comprehensively
- Log meaningful messages

### Testing
- Write unit tests for new features
- Test edge cases and error handling
- Maintain >80% code coverage
- Run tests before committing

---

Use these skills to improve code quality and consistency across the project.
