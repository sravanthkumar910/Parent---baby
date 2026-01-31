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
# STEP CREATION (LANGUAGE 5–12)
# =========================
def create_language_steps(prompt, expected_response, feedback):
    steps = []

    steps.append(
        "Step 1 — Listen carefully to the prompt and understand what you need to say or answer."
    )

    steps.append(
        f"Step 2 — Try responding to the prompt: \"{prompt}\""
    )

    steps.append(
        f"Step 3 — Check the correct response: {expected_response}"
    )

    steps.append(
        "Step 4 — Practice the response again slowly and clearly."
    )

    steps.append(
        f"Step 5 — Encouraging feedback: {feedback}"
    )

    return steps[:5]

# =========================
# PATHS
# =========================
CSV_PATH = "Merged_dataset/language_5_12_data.csv"
MODEL_PATH = "models/language_5_12.pkl"

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)
print("✅ Dataset loaded:", df.shape)

# =========================
# PROCESS INPUT PROMPT
# =========================
df["processed_input"] = df["example_prompt"].apply(preprocess)

# =========================
# CREATE STEPS (MAX 5)
# =========================
df["steps"] = df.apply(
    lambda r: create_language_steps(
        r["example_prompt"],
        r["expected_response"],
        r["feedback_example"]
    ),
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

