import os
import ast
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
# STEP CREATION (PARENT 0–24)
# =========================
def create_parent_steps(row):
    steps = []

    # Step 1 — learning goal
    steps.append(
        f"Step 1 — Understand the goal: {row['parent_learning_goal']}"
    )

    # Step 2 — how to teach
    steps.append(
        f"Step 2 — What to do: {row['how_to_teach']}"
    )

    # Step 3 — DOs (max 2)
    try:
        dos = ast.literal_eval(row["parent_dos"])
        if isinstance(dos, list) and dos:
            steps.append(
                "Step 3 — Do this: " + ", ".join(dos[:2])
            )
    except Exception:
        pass

    # Step 4 — DON'Ts (max 2)
    try:
        donts = ast.literal_eval(row["parent_donts"])
        if isinstance(donts, list) and donts:
            steps.append(
                "Step 4 — Avoid this: " + ", ".join(donts[:2])
            )
    except Exception:
        pass

    # Step 5 — practical tip
    steps.append(
        f"Step 5 — Helpful tip: {row['parent_tip']}"
    )

    return steps[:5]

# =========================
# PATHS (ABSOLUTE — SAFE)
# =========================
CSV_PATH = r"D:\BABY_PARENT_Assistant_PROJECT\parents_dataset\0_24_data_parent.csv"
MODEL_DIR = r"D:\BABY_PARENT_Assistant_PROJECT\parents_dataset\models"
MODEL_PATH = os.path.join(MODEL_DIR, "parent_0_24.pkl")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)
print("✅ Dataset loaded:", df.shape)

# =========================
# CREATE PROCESSED INPUT
# =========================
df["processed_input"] = (
    df["skill_name"].astype(str) + " " +
    df["parent_learning_goal"].astype(str)
).apply(preprocess)

# =========================
# CREATE STEPS (≤5)
# =========================
df["steps"] = df.apply(create_parent_steps, axis=1)

# =========================
# SAVE MODEL
# =========================
os.makedirs(MODEL_DIR, exist_ok=True)
df.to_pickle(MODEL_PATH)

print("✅ Training complete")
print("✅ Model saved to:", MODEL_PATH)
print("✅ Columns:", df.columns.tolist())

print("🚀 Script started")
print("Saving to:", MODEL_PATH)

os.makedirs(MODEL_DIR, exist_ok=True)
print("📁 Model directory exists")

print("🚨 ABOUT TO SAVE FILE")
df.to_pickle(MODEL_PATH)

print("✅ Save function completed")

import os
print("📂 File exists?", os.path.exists(MODEL_PATH))
