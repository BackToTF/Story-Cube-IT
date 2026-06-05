# Lessons Learned - Story Cube - I&D - 2026-06-04

## Stack(s) involved

python / streamlit / ux

---

### Patterns proposed for library

#### Prompt Metaphorization For Non-Technical Facilitation
- Class: reusable for agent-library
- Domain: ux
- Assigned agent: web-developer
- Target skill: packages/nextjs/fintech-dashboard/0.1.0/.github/skills/dashboard-ux/SKILL.md
- Problem: Technical wording in player-facing prompts reduced clarity for mixed technical/non-technical workshop groups.
- Solution: Replace implementation labels with intuitive metaphors while preserving the same underlying data mapping.
- Code snippet:
	```python
	# Keep backend keys stable, adapt only display labels.
	DISPLAY_LABELS = {
			"pipeline_id": "Journey Step",
			"sync_error": "Signal Mismatch",
			"source_table": "Source Card",
	}

	def render_label(raw_key: str) -> str:
			return DISPLAY_LABELS.get(raw_key, raw_key.replace("_", " ").title())
	```
- Proposed addition: add a subsection on terminology abstraction for mixed-audience dashboards and workshop UIs.

---

### Anti-patterns confirmed

None confirmed as standalone library anti-patterns in this session.

---

### Project-specific findings (not for library)

#### Mirrored Dice Visual Ritual
- Class: project-specific only
- Context: Showing 6 dice as 3 unique + 3 mirrored improved perceived game feel in this workshop demo.
- Resolution: Kept scoring logic based on unique outcomes while mirroring only the visual layer.
- Follow-up: Validate if the same perception gain holds in larger facilitation groups.

---

### Library review checklist

- [x] All library patterns are anonymized (no client names, catalogs, tables)
- [x] Every pattern has an assigned agent from the Agent Assignment Matrix
- [x] Code snippets compile / run as-is with placeholder values
- [x] Target skill path exists in agent-library (or flagged as new)
- [x] Each pattern has a clear why it matters for future re-use
