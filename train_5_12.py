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
    tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
    tokens = [stemmer.stem(t) for t in tokens]
    return set(tokens)

# =========================
# STEP CREATION (ACADEMICS 5–12)
# =========================
def create_steps_5_12(activity, goal):
    text = activity.lower()
    steps = []

    # Step 1 — setup
    steps.append("Step 1 — Set up a quiet space with learning materials ready.")

    # Step 2 — introduce concept
    steps.append(f"Step 2 — Explain the activity clearly: {activity}")

    # Step 3 — keyword-based academic logic
    if any(k in text for k in ["add", "subtract", "multiply", "divide", "math"]):
        steps.append("Step 3 — Work through one example together before independent practice.")
    elif any(k in text for k in ["pattern", "sequence", "logic", "reason"]):
        steps.append("Step 3 — Discuss the pattern or logic and ask the child to predict outcomes.")
    elif any(k in text for k in ["time", "clock", "calendar"]):
        steps.append("Step 3 — Use real-life examples to explain time-related concepts.")
    elif any(k in text for k in ["problem", "solve", "puzzle"]):
        steps.append("Step 3 — Encourage the child to think aloud while solving the problem.")
    else:
        steps.append("Step 3 — Demonstrate the task once and guide step by step.")

    # Step 4 — independent attempt
    steps.append("Step 4 — Let the child attempt the activity independently with guidance if needed.")

    # Step 5 — reinforce goal
    if isinstance(goal, str) and goal.strip():
        steps.append(f"Step 5 — Review and practice again to strengthen: {goal}")
    else:
        steps.append("Step 5 — Review the activity and practice again for better understanding.")

    return steps[:5]

# =========================
# PATHS
# =========================
CSV_PATH = "Merged_dataset/5_12_year_data.csv"
MODEL_PATH = "models/academics_5_12.pkl"

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)
print("✅ Dataset loaded:", df.shape)

# =========================
# PROCESS TEXT
# =========================
df["processed_activity"] = df["activity"].apply(preprocess)

# =========================
# CREATE STEPS (MAX 5)
# =========================
df["steps"] = df.apply(
    lambda r: create_steps_5_12(r["activity"], r.get("goal")),
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

