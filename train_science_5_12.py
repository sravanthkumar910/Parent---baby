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
# STEP CREATION (SCIENCE 5–12)
# =========================
def create_science_steps(output, solution_steps):
    steps = []

    # Step 1 — understand question
    steps.append("Step 1 — Read the science question carefully and understand what is being asked.")

    # Use up to 3 reasoning steps
    try:
        parsed = ast.literal_eval(solution_steps)
        if isinstance(parsed, list):
            for s in parsed[:3]:
                steps.append(f"Step {len(steps)+1} — {s}")
    except:
        pass

    # Final conclusion
    steps.append(f"Step {len(steps)+1} — The correct conclusion is: {output}")

    return steps[:5]

# =========================
# PATHS
# =========================
CSV_PATH = "Merged_dataset/science_5_12_data.csv"
MODEL_PATH = "models/science_5_12.pkl"

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
    lambda r: create_science_steps(r["output"], r["solution_steps"]),
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

