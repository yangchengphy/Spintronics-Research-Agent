import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "processed_papers"
PLAN_FILE = BASE_DIR / "research_plan.md"
NOTEBOOK_FILE = BASE_DIR / "lab_notebook.md"

# --- MODEL SELECTION ---
# Gemini 3 Pro (Preview) for Deep Reasoning
TARGET_MODEL = 'models/gemini-3-pro-preview' 
# Flash 2.0 for Fast Planning/Summarizing
PLANNER_MODEL = 'models/gemini-2.5-flash'
COMPRESSOR_MODEL = 'models/gemini-2.5-flash'
EMBEDDING_MODEL_NAME = 'BAAI/bge-small-en-v1.5'

# --- LIMITS ---
CACHE_TTL_HOURS = 1
MAX_CACHE_SIZE = 2800000        # ~900k tokens
GIANT_FILE_THRESHOLD = 100000   # Compress if larger
