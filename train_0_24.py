import os
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# =========================
# NLTK SETUP
# =========================
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def preprocess(text):
    text = str(text).lower()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalnum()]
    tokens = [t for t in tokens if t not in stop_words]
    tokens = [stemmer.stem(t) for t in tokens]
    return set(tokens)

# =========================
# STEP CREATION (0–24 ONLY)
# =========================
def create_steps_0_24(activity, goal):
    text = activity.lower()
    steps = []

    # Step 1 — environment (always)
    steps.append("Step 1 — Create a calm, safe, and comfortable space for the baby.")

    # Step 2 — activity-specific intro
    steps.append(f"Step 2 — Gently introduce the activity: {activity}")

    # Step 3 — keyword-based baby logic
    if any(k in text for k in ["look", "see", "watch", "eye", "visual"]):
        steps.append("Step 3 — Slowly move objects to help the baby focus and track visually.")
    elif any(k in text for k in ["sound", "listen", "hear", "shake", "rattle"]):
        steps.append("Step 3 — Make gentle sounds and pause to let the baby respond.")
    elif any(k in text for k in ["hold", "grasp", "touch", "reach"]):
        steps.append("Step 3 — Encourage the baby to touch or grasp using slow movements.")
    elif any(k in text for k in ["move", "roll", "turn", "lift"]):
        steps.append("Step 3 — Support the baby’s movement while ensuring safety.")
    else:
        steps.append("Step 3 — Demonstrate the activity slowly so the baby can observe.")

    # Step 4 — interaction
    steps.append("Step 4 — Watch the baby’s reaction and respond with smiles, words, or touch.")

    # Step 5 — reinforcement (goal-aware)
    if isinstance(goal, str) and goal.strip():
        steps.append(f"Step 5 — Repeat regularly to support: {goal}")
    else:
        steps.append("Step 5 — Repeat the activity often to support early development.")

    # Guarantee max 5 steps
    return steps[:5]

# =========================
# PATHS
# =========================
CSV_PATH = "Merged_dataset/0_24_month_data.csv"
MODEL_PATH = "models/baby_0_24.pkl"

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)
print("✅ Dataset loaded:", df.shape)

# =========================
# PROCESS TEXT
# =========================
df["processed_activity"] = df["activity_idea"].apply(preprocess)

# =========================
# CREATE STEPS (MAX 5)
# =========================
df["steps"] = df.apply(
    lambda r: create_steps_0_24(r["activity_idea"], r["development_goal"]),
    axis=1
)

# =========================
# SAVE MODEL
# =========================
os.makedirs("models", exist_ok=True)
df.to_pickle(MODEL_PATH)

print("✅ Training complete")
print("✅ Model saved to:", MODEL_PATH)
print("✅ Columns:", df.columns.tolist())

