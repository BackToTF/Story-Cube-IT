AVAILABLE_MODES = {
    "basic_storytelling": "Tell a short story with the rolled faces.",
    "advanced_storytelling": "Use all six faces from one cube category.",
    "six_word_story": "Create a six-word story from one or two faces.",
    "collaborative": "Each player extends the story with one new face.",
    "idea_generation": "Generate at least three distinct IT ideas.",
    "pipeline_story": "Build a data pipeline story from orchestration to impact.",
}


def is_supported_mode(mode: str) -> bool:
    return mode in AVAILABLE_MODES
