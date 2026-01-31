import os
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import ast

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
# STEP CREATION (CIVICS / EVS 5–12)
# =========================
def create_civics_steps(output, solution_steps):
    steps = []

    # Step 1 — understand
    steps.append("Step 1 — Read the question carefully and understand the situation.")

    # Parse solution_steps safely (stored as string list)
    try:
        parsed_steps = ast.literal_eval(solution_steps)
        if isinstance(parsed_steps, list):
            for s in parsed_steps[:3]:
                steps.append(f"Step {len(steps)+1} — {s}")
    except:
        pass

    # Final step — conclusion
    steps.append(f"Step {len(steps)+1} — Conclude with the correct idea: {output}")

    return steps[:5]

# =========================
# PATHS
# =========================
CSV_PATH = "Merged_dataset/civics_evs_5_12_data.csv"
MODEL_PATH = "models/civics_evs_5_12.pkl"

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)
print("✅ Dataset loaded:", df.shape)

# =========================
# PROCESS INPUT
# =========================
df["processed_input"] = df["input"].apply(preprocess)

# =========================
# CREATE STEPS (MAX 5)
# =========================
df["steps"] = df.apply(
    lambda r: create_civics_steps(r["output"], r["solution_steps"]),
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

