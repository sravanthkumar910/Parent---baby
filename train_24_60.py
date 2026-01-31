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
# STEP CREATION (24–60 ONLY)
# =========================
def create_steps_24_60(activity, goal):
    text = activity.lower()
    steps = []

    # Step 1 — setup
    steps.append("Step 1 — Set up a safe space with enough room for movement and play.")

    # Step 2 — introduce activity
    steps.append(f"Step 2 — Explain and show the activity: {activity}")

    # Step 3 — keyword-based logic (toddler/preschool focus)
    if any(k in text for k in ["sort", "match", "group", "stack"]):
        steps.append("Step 3 — Demonstrate sorting or grouping slowly and let the child copy.")
    elif any(k in text for k in ["count", "number", "shape", "color"]):
        steps.append("Step 3 — Name objects aloud and encourage the child to repeat or point.")
    elif any(k in text for k in ["run", "jump", "climb", "balance"]):
        steps.append("Step 3 — Support physical movement while watching for balance and safety.")
    elif any(k in text for k in ["pretend", "imagine", "role", "story"]):
        steps.append("Step 3 — Join the child in pretend play and ask simple questions.")
    else:
        steps.append("Step 3 — Demonstrate the activity once and guide the child step by step.")

    # Step 4 — independence
    steps.append("Step 4 — Encourage the child to try independently while you observe.")

    # Step 5 — reinforcement (goal-aware)
    if isinstance(goal, str) and goal.strip():
        steps.append(f"Step 5 — Repeat and praise efforts to support: {goal}")
    else:
        steps.append("Step 5 — Repeat the activity and praise the child’s effort.")

    return steps[:5]

# =========================
# PATHS
# =========================
CSV_PATH = "Merged_dataset/24_60_month_data.csv"
MODEL_PATH = "models/child_24_60.pkl"

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
    lambda r: create_steps_24_60(r["activity"], r.get("goal")),
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


