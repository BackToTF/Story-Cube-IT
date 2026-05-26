from __future__ import annotations

from .models import CubeFace


IT_GENERAL_CUBES: dict[str, list[CubeFace]] = {
    "AI": [
        CubeFace("AI", 1, "Prompt", "Define a precise prompt objective."),
        CubeFace("AI", 2, "Model", "Pick the best model for the task."),
        CubeFace("AI", 3, "Bias", "Identify one potential model bias."),
        CubeFace("AI", 4, "Guardrail", "Add one safety or policy constraint."),
        CubeFace("AI", 5, "Feedback", "Use user feedback to improve output."),
        CubeFace("AI", 6, "Creativity", "Introduce one surprising creative angle."),
    ],
    "Cloud": [
        CubeFace("Cloud", 1, "API", "Expose one useful API endpoint."),
        CubeFace("Cloud", 2, "Latency", "Reduce end-to-end latency."),
        CubeFace("Cloud", 3, "Scalability", "Design for scale spikes."),
        CubeFace("Cloud", 4, "Cost", "Optimize cloud cost without losing quality."),
        CubeFace("Cloud", 5, "Observability", "Add a metric and an alert."),
        CubeFace("Cloud", 6, "Resilience", "Handle one failure mode gracefully."),
    ],
    "People": [
        CubeFace("People", 1, "Accessibility", "Make the idea inclusive by design."),
        CubeFace("People", 2, "Collaboration", "Enable cross-team collaboration."),
        CubeFace("People", 3, "Learning", "Turn this into a learning moment."),
        CubeFace("People", 4, "Ethics", "Address one ethical implication."),
        CubeFace("People", 5, "Mentoring", "Include a mentoring opportunity."),
        CubeFace("People", 6, "Impact", "Describe impact on real users."),
    ],
}


DATA_PIPELINE_ID_CUBES: dict[str, list[CubeFace]] = {
    "Orchestration": [
        CubeFace("Orchestration", 1, "ADF Trigger", "Start with a schedule or event trigger in ADF."),
        CubeFace("Orchestration", 2, "Pipeline Dependency", "Define dependencies between activities."),
        CubeFace("Orchestration", 3, "Retry Policy", "Handle transient errors with retries."),
        CubeFace("Orchestration", 4, "Monitoring", "Track pipeline health with clear signals."),
        CubeFace("Orchestration", 5, "SLA", "Set a delivery target for data freshness."),
        CubeFace("Orchestration", 6, "Fallback", "Plan a fallback path when a step fails."),
    ],
    "Ingestion": [
        CubeFace("Ingestion", 1, "Batch Load", "Ingest source data in controlled batches."),
        CubeFace("Ingestion", 2, "CDC", "Capture changes incrementally from source."),
        CubeFace("Ingestion", 3, "API Extract", "Collect data from an API endpoint."),
        CubeFace("Ingestion", 4, "Schema Drift", "Handle source schema evolution safely."),
        CubeFace("Ingestion", 5, "Data Contract", "Define source fields and quality expectations."),
        CubeFace("Ingestion", 6, "Landing Zone", "Store raw data in a governed landing area."),
    ],
    "Transformation": [
        CubeFace("Transformation", 1, "Databricks Notebook", "Transform raw data in Databricks."),
        CubeFace("Transformation", 2, "Delta Tables", "Persist curated data using Delta format."),
        CubeFace("Transformation", 3, "Data Quality", "Validate completeness and consistency rules."),
        CubeFace("Transformation", 4, "Join Strategy", "Choose correct joins to avoid data loss."),
        CubeFace("Transformation", 5, "PII Handling", "Mask or protect personal data fields."),
        CubeFace("Transformation", 6, "Lineage", "Keep lineage traceable for each transformation."),
    ],
    "InclusionLens": [
        CubeFace("InclusionLens", 1, "Accessibility", "Ensure outputs are understandable for all users."),
        CubeFace("InclusionLens", 2, "Language", "Consider multilingual needs in reporting."),
        CubeFace("InclusionLens", 3, "Bias Check", "Check for biased assumptions in data logic."),
        CubeFace("InclusionLens", 4, "Representation", "Verify that groups are fairly represented."),
        CubeFace("InclusionLens", 5, "Transparency", "Document assumptions and data limitations."),
        CubeFace("InclusionLens", 6, "Shared Value", "Describe who benefits and who may be excluded."),
    ],
}


CUBE_PACKS: dict[str, dict[str, list[CubeFace]]] = {
    "it_general": IT_GENERAL_CUBES,
    "data_pipeline_id": DATA_PIPELINE_ID_CUBES,
}


DEFAULT_PACK = "data_pipeline_id"
