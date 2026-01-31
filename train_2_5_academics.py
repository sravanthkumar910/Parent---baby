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
# STEP CREATION (ACADEMICS 2–5)
# =========================
def create_steps_2_5(activity, goal):
    text = activity.lower()
    steps = []

    # Step 1 — setup
    steps.append("Step 1 — Prepare a quiet learning space with simple materials.")

    # Step 2 — introduce
    steps.append(f"Step 2 — Clearly introduce the activity: {activity}")

    # Step 3 — keyword-based academic focus
    if any(k in text for k in ["count", "number", "math", "add", "subtract"]):
        steps.append("Step 3 — Demonstrate counting or number use with real objects.")
    elif any(k in text for k in ["letter", "alphabet", "sound", "phonics"]):
        steps.append("Step 3 — Say the letters or sounds aloud and ask the child to repeat.")
    elif any(k in text for k in ["shape", "color", "pattern", "sort", "match"]):
        steps.append("Step 3 — Show how to identify, match, or sort items step by step.")
    elif any(k in text for k in ["story", "read", "listen", "sentence"]):
        steps.append("Step 3 — Read or explain slowly and ask simple questions.")
    else:
        steps.append("Step 3 — Demonstrate the task once and guide the child gently.")

    # Step 4 — practice
    steps.append("Step 4 — Let the child try independently and support if needed.")

    # Step 5 — reinforce (goal-aware)
    if isinstance(goal, str) and goal.strip():
        steps.append(f"Step 5 — Practice again to reinforce: {goal}")
    else:
        steps.append("Step 5 — Repeat the activity to strengthen understanding.")

    return steps[:5]

# =========================
# PATHS
# =========================
CSV_PATH = "Merged_dataset/2_5_academics_data.csv"
MODEL_PATH = "models/academics_2_5.pkl"

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
    lambda r: create_steps_2_5(r["activity"], r.get("goal")),
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


