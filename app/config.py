import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set"
    )

MODEL_NAME = "gemini-2.5-flash"

# Debug - remove after fixing
print(f"CONFIG DEBUG - API Key loaded: {bool(GEMINI_API_KEY)}, Length: {len(GEMINI_API_KEY) if GEMINI_API_KEY else 0}")