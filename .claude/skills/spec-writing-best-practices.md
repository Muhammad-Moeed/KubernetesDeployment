---
name: spec-writing-best-practices
description: ALWAYS follow these rules when writing or refining any spec
priority: high
---

WHEN WRITING OR REFINING ANY SPEC FILE:

Follow this exact structure:

# Feature: [Clear Name]

## User Stories
- As a [user], I want [goal] so that [benefit]

## Acceptance Criteria
- GIVEN [context]
  WHEN [action]
  THEN [expected result]

- Must handle edge cases:
  - Empty inputs → show error
  - Very long text → truncate or validate length
  - Unauthorized access → 401/403
  - Network failure → show retry

## Technical Notes
- Reference related specs: @specs/database/schema.md
- For frontend: List exact UI elements needed
- For backend: List exact API response format

## Bonus Requirements (if applicable)
- Urdu support: All UI text translatable
- Voice input: Add microphone button

Always use clear, testable language.
Never use vague words like "nice", "good", "fast".
End with: "This spec is complete and ready for implementation."