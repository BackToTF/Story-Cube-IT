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
        CubeFace("Orchestration", 1, "Mission Start", "Open the quest with a clear start signal."),
        CubeFace("Orchestration", 2, "Travel Plan", "Define the order of steps in the journey."),
        CubeFace("Orchestration", 3, "Second Chance", "Add a retry path when something breaks."),
        CubeFace("Orchestration", 4, "Control Room", "Keep watch on progress and warnings."),
        CubeFace("Orchestration", 5, "Deadline", "Set a clear time target for delivery."),
        CubeFace("Orchestration", 6, "Backup Route", "Prepare a safe alternative route."),
    ],
    "Ingestion": [
        CubeFace("Ingestion", 1, "Supply Drop", "Collect a new batch of source data."),
        CubeFace("Ingestion", 2, "Live Feed", "Bring only fresh changes from the source."),
        CubeFace("Ingestion", 3, "Data Portal", "Pull information from an external service."),
        CubeFace("Ingestion", 4, "Shape Shift", "Adapt safely when source fields change."),
        CubeFace("Ingestion", 5, "Quality Pact", "Agree on source quality expectations."),
        CubeFace("Ingestion", 6, "Base Camp", "Store raw data in a safe landing zone."),
    ],
    "Transformation": [
        CubeFace("Transformation", 1, "Alchemy Lab", "Transform raw ingredients into useful insight."),
        CubeFace("Transformation", 2, "Treasure Vault", "Store clean data in a trusted place."),
        CubeFace("Transformation", 3, "Purity Check", "Validate quality before sharing results."),
        CubeFace("Transformation", 4, "Link Bridge", "Connect datasets without losing meaning."),
        CubeFace("Transformation", 5, "Privacy Shield", "Protect personal details in the story."),
        CubeFace("Transformation", 6, "Story Trace", "Keep every transformation explainable."),
    ],
    "InclusionLens": [
        CubeFace("InclusionLens", 1, "Open Door", "Make the output understandable for everyone."),
        CubeFace("InclusionLens", 2, "Many Voices", "Support diverse language and expression."),
        CubeFace("InclusionLens", 3, "Fairness Scan", "Spot hidden bias in assumptions."),
        CubeFace("InclusionLens", 4, "Full Picture", "Check who is represented and who is missing."),
        CubeFace("InclusionLens", 5, "Clear Glass", "Explain assumptions and data limits."),
        CubeFace("InclusionLens", 6, "Shared Win", "Describe benefits across different groups."),
    ],
}


CUBE_PACKS: dict[str, dict[str, list[CubeFace]]] = {
    "it_general": IT_GENERAL_CUBES,
    "data_pipeline_id": DATA_PIPELINE_ID_CUBES,
}


DEFAULT_PACK = "data_pipeline_id"
