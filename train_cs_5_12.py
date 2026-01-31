import os
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

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
# STEP CREATION (CS 5–12)
# =========================
def create_steps_cs(output, solution_steps):
    steps = []

    # Step 1 — introduction
    steps.append("Step 1 — Understand the question and what is being asked.")

    # Step 2–3 — explanation from solution_steps
    if isinstance(solution_steps, str) and solution_steps.strip():
        parts = re.split(r'\.|\n', solution_steps)
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) >= 1:
            steps.append(f"Step 2 — {parts[0]}")
        if len(parts) >= 2:
            steps.append(f"Step 3 — {parts[1]}")
    else:
        steps.append("Step 2 — Go through the concept step by step.")
        steps.append("Step 3 — Look at simple examples to understand it better.")

    # Step 4 — child engagement
    steps.append("Step 4 — Ask the child to explain the idea in their own words.")

    # Step 5 — final answer
    steps.append(f"Step 5 — Conclude with the correct answer: {output}")

    return steps[:5]

# =========================
# PATHS
# =========================
CSV_PATH = "Merged_dataset/cs_5_12_data.csv"
MODEL_PATH = "models/cs_5_12.pkl"

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)
print("✅ Dataset loaded:", df.shape)

# =========================
# PROCESS INPUT TEXT
# =========================
df["processed_input"] = df["input"].apply(preprocess)

# =========================
# CREATE STEPS (MAX 5)
# =========================
df["steps"] = df.apply(
    lambda r: create_steps_cs(r["output"], r["solution_steps"]),
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

