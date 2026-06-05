---
applyTo: "**"
---

# Continuous Lessons Learned — Pattern Detection

While working on this project, passively monitor for reusable patterns, edge cases, and anti-patterns.
When detected, append exactly one compact callout at the end of the response.

## When to surface a pattern

Surface callout when:
- Solving a non-obvious technical problem.
- Discovering an anti-pattern and the reason it failed.
- Applying a convention not yet covered in current skills.
- Handling an edge case that required more than one attempt.

Do not surface callouts for routine operations.

## Callout format

---
💡 **Lesson detected** — *[Pattern Name]*
- **Domain**: python / ux / powerbi / databricks / common
- **What**: One reusable insight.
- **Why it matters**: When this should be reused.
- **Target skill**: `packages/<domain>/<package>/skills/<skill>/SKILL.md`
- 👉 Run `contribute-back` at end of session to save this.
---

## Rules

- Maximum one callout per response.
- Keep it anonymous.
- Skip if unsure whether reusable.
