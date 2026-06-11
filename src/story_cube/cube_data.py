from __future__ import annotations

from .models import CubeFace


def _face(cube_id: str, face_id: int, label: str, prompt: str, options: list[str]) -> CubeFace:
    return CubeFace(cube_id=cube_id, face_id=face_id, label=label, prompt=prompt, options=options)


IT_GENERAL_CUBES: dict[str, list[CubeFace]] = {
    "AI": [
        _face("AI", 1, "Prompt", "Define a precise prompt objective.", ["Ask a focused question", "State the desired output", "Set the tone and audience", "Name the success criteria"]),
        _face("AI", 2, "Model", "Pick the best model for the task.", ["Use a small fast model", "Use a balanced general model", "Use a reasoning-heavy model", "Use a multimodal model"]),
        _face("AI", 3, "Bias", "Identify one potential model bias.", ["Watch for stereotype drift", "Check missing voices", "Review cultural assumptions", "Spot overconfidence"]),
        _face("AI", 4, "Guardrail", "Add one safety or policy constraint.", ["Block sensitive data", "Require human review", "Keep a fallback path", "Limit uncertainty claims"]),
        _face("AI", 5, "Feedback", "Use user feedback to improve output.", ["Collect quick reactions", "Track recurring issues", "Invite examples", "Compare before and after"]),
        _face("AI", 6, "Creativity", "Introduce one surprising creative angle.", ["Try a bold metaphor", "Flip the perspective", "Mix two ideas", "Add a playful twist"]),
    ],
    "Cloud": [
        _face("Cloud", 1, "API", "Expose one useful API endpoint.", ["Create a simple endpoint", "Define clear inputs", "Return a clean payload", "Document the contract"]),
        _face("Cloud", 2, "Latency", "Reduce end-to-end latency.", ["Cache hot paths", "Trim network hops", "Precompute results", "Measure the slowest step"]),
        _face("Cloud", 3, "Scalability", "Design for scale spikes.", ["Add queue buffering", "Autoscale workers", "Split the workload", "Use backpressure"]),
        _face("Cloud", 4, "Cost", "Optimize cloud cost without losing quality.", ["Remove waste", "Right-size resources", "Use cheaper storage", "Reduce idle time"]),
        _face("Cloud", 5, "Observability", "Add a metric and an alert.", ["Track errors", "Watch latency", "Alert on volume drops", "Log the right context"]),
        _face("Cloud", 6, "Resilience", "Handle one failure mode gracefully.", ["Retry safely", "Fail over", "Degrade features", "Recover automatically"]),
    ],
    "People": [
        _face("People", 1, "Accessibility", "Make the idea inclusive by design.", ["Use plain language", "Add keyboard support", "Offer alternative paths", "Reduce cognitive load"]),
        _face("People", 2, "Collaboration", "Enable cross-team collaboration.", ["Share context early", "Clarify ownership", "Invite feedback", "Sync regularly"]),
        _face("People", 3, "Learning", "Turn this into a learning moment.", ["Add a short walkthrough", "Capture a tip", "Share an example", "Invite reflection"]),
        _face("People", 4, "Ethics", "Address one ethical implication.", ["Check fairness", "Protect privacy", "Explain trade-offs", "Ask who benefits"]),
        _face("People", 5, "Mentoring", "Include a mentoring opportunity.", ["Pair up", "Shadow a teammate", "Share a template", "Review together"]),
        _face("People", 6, "Impact", "Describe impact on real users.", ["Reduce frustration", "Save time", "Increase trust", "Support better outcomes"]),
    ],
}


DATA_PIPELINE_ID_CUBES: dict[str, list[CubeFace]] = {
    "Orchestration": [
        _face("Orchestration", 1, "Mission Start", "Open the quest with a clear start signal.", ["Set the goal", "Name the first step", "Explain the stakes", "Start with a small win"]),
        _face("Orchestration", 2, "Travel Plan", "Define the order of steps in the journey.", ["Map the sequence", "List dependencies", "Choose the owner", "Set checkpoints"]),
        _face("Orchestration", 3, "Second Chance", "Add a retry path when something breaks.", ["Retry automatically", "Pause and review", "Route to fallback", "Notify the team"]),
        _face("Orchestration", 4, "Control Room", "Keep watch on progress and warnings.", ["Add a dashboard", "Watch for anomalies", "Surface warnings", "Keep everyone informed"]),
        _face("Orchestration", 5, "Deadline", "Set a clear time target for delivery.", ["Choose a target date", "Break it into milestones", "Protect focus time", "Make trade-offs explicit"]),
        _face("Orchestration", 6, "Backup Route", "Prepare a safe alternative route.", ["Keep a fallback plan", "Prepare a manual step", "Save a snapshot", "Define recovery steps"]),
    ],
    "Ingestion": [
        _face("Ingestion", 1, "Supply Drop", "Collect a new batch of source data.", ["Pull a batch", "Fetch a file", "Read from an API", "Capture a snapshot"]),
        _face("Ingestion", 2, "Live Feed", "Bring only fresh changes from the source.", ["Use CDC", "Stream updates", "Filter deltas", "Keep latency low"]),
        _face("Ingestion", 3, "Data Portal", "Pull information from an external service.", ["Connect to the API", "Use secure auth", "Validate the response", "Cache the payload"]),
        _face("Ingestion", 4, "Shape Shift", "Adapt safely when source fields change.", ["Map new fields", "Handle nulls", "Detect schema drift", "Fallback gracefully"]),
        _face("Ingestion", 5, "Quality Pact", "Agree on source quality expectations.", ["Set validation rules", "Define freshness", "Agree on ownership", "Escalate issues quickly"]),
        _face("Ingestion", 6, "Base Camp", "Store raw data in a safe landing zone.", ["Land raw data", "Tag the batch", "Keep the source trace", "Protect the original copy"]),
    ],
    "Transformation": [
        _face("Transformation", 1, "Alchemy Lab", "Transform raw ingredients into useful insight.", ["Clean the data", "Join the facts", "Standardize the rules", "Create a useful view"]),
        _face("Transformation", 2, "Treasure Vault", "Store clean data in a trusted place.", ["Save curated tables", "Protect the output", "Version the model", "Keep access controlled"]),
        _face("Transformation", 3, "Purity Check", "Validate quality before sharing results.", ["Check missing values", "Inspect duplicates", "Confirm totals", "Test edge cases"]),
        _face("Transformation", 4, "Link Bridge", "Connect datasets without losing meaning.", ["Join carefully", "Use stable keys", "Document the mapping", "Preserve lineage"]),
        _face("Transformation", 5, "Privacy Shield", "Protect personal details in the story.", ["Mask personal data", "Limit access", "Reduce exposure", "Use safe aggregation"]),
        _face("Transformation", 6, "Story Trace", "Keep every transformation explainable.", ["Write the rule", "Track the step", "Show the lineage", "Keep the reasoning visible"]),
    ],
    "InclusionLens": [
        _face("InclusionLens", 1, "Open Door", "Make the output understandable for everyone.", ["Use plain language", "Add simple examples", "Avoid jargon", "Offer a short summary"]),
        _face("InclusionLens", 2, "Many Voices", "Support diverse language and expression.", ["Invite another voice", "Use inclusive terms", "Share the floor", "Respect different styles"]),
        _face("InclusionLens", 3, "Fairness Scan", "Spot hidden bias in assumptions.", ["Question defaults", "Check missing groups", "Review edge cases", "Compare outcomes"]),
        _face("InclusionLens", 4, "Full Picture", "Check who is represented and who is missing.", ["Map the audience", "Find the gaps", "Include quieter users", "Balance the view"]),
        _face("InclusionLens", 5, "Clear Glass", "Explain assumptions and data limits.", ["State the limits", "Show what is unknown", "Name assumptions", "Be transparent"]),
        _face("InclusionLens", 6, "Shared Win", "Describe benefits across different groups.", ["List the beneficiaries", "Check shared value", "Reduce exclusion", "Keep it useful for all"]),
    ],
}


STORYBOOK_SIMPLE_CUBES: dict[str, list[CubeFace]] = {
    "OnceUpon": [
        _face("OnceUpon", 1, "Inizio", "Start the story gently.", ["Once upon a time", "One sunny morning", "Far away in a small place"]),
        _face("OnceUpon", 2, "Buonanotte", "Choose a calm opening.", ["A quiet day began", "Someone woke up smiling", "The story opened with a surprise"]),
        _face("OnceUpon", 3, "Mondo", "Choose the first feeling.", ["A happy world", "A curious world", "A magical world"]),
        _face("OnceUpon", 4, "Partenza", "Pick how the tale begins.", ["A simple hello", "A small adventure", "A gentle mystery"]),
        _face("OnceUpon", 5, "Voce", "Pick the first voice.", ["A child spoke", "A friend listened", "A soft wind answered"]),
        _face("OnceUpon", 6, "Seme", "Pick the first seed of the tale.", ["A tiny idea", "A brave wish", "A little question"]),
    ],
    "Character": [
        _face("Character", 1, "Hero", "Choose who is there.", ["A brave child", "A kind friend", "A clever animal"]),
        _face("Character", 2, "Helper", "Choose the second character.", ["A helpful sister", "A funny robot", "A gentle giant"]),
        _face("Character", 3, "Dreamer", "Choose a character with a dream.", ["A dreamer", "A tiny explorer", "A curious inventor"]),
        _face("Character", 4, "Team", "Choose a group of helpers.", ["Two best friends", "A family team", "A small brave group"]),
        _face("Character", 5, "Animal", "Choose a friendly creature.", ["A fox", "A cat", "A bird"]),
        _face("Character", 6, "Magic", "Choose a special character.", ["A little wizard", "A moon fairy", "A talking star"]),
    ],
    "Setting": [
        _face("Setting", 1, "Forest", "Choose where the story happens.", ["In a green forest", "Near a shining river", "Inside a cozy house"]),
        _face("Setting", 2, "Castle", "Choose a place for the tale.", ["A bright castle", "A secret garden", "A friendly village"]),
        _face("Setting", 3, "Sky", "Choose a sky-like place.", ["Up in the clouds", "On a windy hill", "Under a rainbow"]),
        _face("Setting", 4, "Sea", "Choose a watery place.", ["By the sea", "On a little boat", "At a beach at sunset"]),
        _face("Setting", 5, "Town", "Choose a place with people.", ["In a busy town", "At a market", "In a school yard"]),
        _face("Setting", 6, "Home", "Choose a familiar place.", ["At home", "In a bedroom fort", "Around a kitchen table"]),
    ],
    "Event": [
        _face("Event", 1, "Find", "Choose what happens.", ["They found a clue", "They discovered a treasure", "They met someone new"]),
        _face("Event", 2, "Move", "Choose the action.", ["They set off", "They ran quickly", "They followed a path"]),
        _face("Event", 3, "Play", "Choose a lively event.", ["They played a game", "They sang a song", "They danced together"]),
        _face("Event", 4, "Ask", "Choose a conversation moment.", ["They asked for help", "They made a promise", "They shared an idea"]),
        _face("Event", 5, "Try", "Choose a trial moment.", ["They tried again", "They built something", "They opened a door"]),
        _face("Event", 6, "Meet", "Choose a meeting moment.", ["They met a guide", "They met a stranger", "They met a friend"]),
    ],
    "Problem": [
        _face("Problem", 1, "Lost", "Choose the problem.", ["Something was lost", "They could not agree", "The path was unclear"]),
        _face("Problem", 2, "Rain", "Choose a small trouble.", ["Rain fell", "The light went out", "A door was stuck"]),
        _face("Problem", 3, "Scared", "Choose a worry.", ["Someone felt scared", "A voice was missing", "A plan felt too big"]),
        _face("Problem", 4, "Mix-Up", "Choose a mix-up.", ["The map was wrong", "The box was empty", "A message got mixed up"]),
        _face("Problem", 5, "Delay", "Choose a delay.", ["Time ran short", "The group waited", "The answer took too long"]),
        _face("Problem", 6, "Oops", "Choose a small mistake.", ["They made a mistake", "They forgot a step", "They needed a new plan"]),
    ],
    "Resolution": [
        _face("Resolution", 1, "Help", "Choose how it ends.", ["A friend helped", "They worked together", "They asked kindly"]),
        _face("Resolution", 2, "Fix", "Choose a fix.", ["They found a fix", "They repaired it", "They made it better"]),
        _face("Resolution", 3, "Share", "Choose a shared ending.", ["They shared the win", "Everyone laughed", "They celebrated together"]),
        _face("Resolution", 4, "Learn", "Choose a lesson.", ["They learned something", "They felt proud", "They understood each other"]),
        _face("Resolution", 5, "Home", "Choose a safe ending.", ["They went home happy", "They rested at last", "They felt safe again"]),
        _face("Resolution", 6, "Next", "Choose a new start.", ["A new adventure began", "They planned tomorrow", "They said goodbye for now"]),
    ],
}


CUBE_PACKS: dict[str, dict[str, list[CubeFace]]] = {
    "it_general": IT_GENERAL_CUBES,
    "data_pipeline_id": DATA_PIPELINE_ID_CUBES,
    "storybook_simple": STORYBOOK_SIMPLE_CUBES,
}


DEFAULT_PACK = "data_pipeline_id"
