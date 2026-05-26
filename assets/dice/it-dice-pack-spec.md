# IT Dice Pack Spec

## Goal

Define real visual dice assets tied to Data, IT, and I&D themes, reusable in app and slides.

## Dice set v1

1. Orchestration die
- ADF Trigger
- Pipeline Dependency
- Retry Policy
- Monitoring
- SLA
- Fallback

2. Ingestion die
- Batch Load
- CDC
- API Extract
- Schema Drift
- Data Contract
- Landing Zone

3. Transformation die
- Databricks Notebook
- Delta Tables
- Data Quality
- Join Strategy
- PII Handling
- Lineage

4. Inclusion Lens die
- Accessibility
- Language
- Bias Check
- Representation
- Transparency
- Shared Value

## Asset format

- Preferred: SVG (one file per face + optional combined sprite)
- Naming: die_<category>_face_<label>.svg
- Example: die_ai_face_prompt.svg

## Style guide

- Rounded square die with high contrast iconography
- Label always visible under icon
- Palette must remain accessible (WCAG-friendly contrast)
- No score/ranking visual language

## Integration target

- Streamlit app: show face SVG in rolled panel
- Mockups: replace placeholder tiles with real die graphics
- PPT export (future): embed rendered faces per session
