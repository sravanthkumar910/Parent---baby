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
# STEP CREATION (CHILD SAFETY)
# =========================
def create_safety_steps(scenario, response, trusted_action, goal):
    steps = []

    # Step 1 — understand situation
    steps.append("Step 1 — Understand what is happening in this situation.")

    # Step 2 — identify risk
    steps.append("Step 2 — Notice that this situation may not be safe.")

    # Step 3 — what NOT to do
    steps.append("Step 3 — Do not touch, go closer, or act without adult permission.")

    # Step 4 — correct response
    steps.append(f"Step 4 — Follow this safe response: {response}")

    # Step 5 — trusted help
    if isinstance(trusted_action, str) and trusted_action.strip():
        steps.append(f"Step 5 — Get help by doing this: {trusted_action}")
    elif isinstance(goal, str) and goal.strip():
        steps.append(f"Step 5 — Remember this safety rule: {goal}")
    else:
        steps.append("Step 5 — Always tell a trusted adult immediately.")

    return steps[:5]

# =========================
# PATHS
# =========================
CSV_PATH = "Merged_dataset/good_bad_touch_data.csv"
MODEL_PATH = "models/good_bad_touch.pkl"

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)
print("✅ Dataset loaded:", df.shape)

# =========================
# PROCESS SCENARIO TEXT
# =========================
df["processed_input"] = df["scenario"].apply(preprocess)

# =========================
# CREATE STEPS (MAX 5)
# =========================
df["steps"] = df.apply(
    lambda r: create_safety_steps(
        r["scenario"],
        r["response_guidance"],
        r["trusted_action"],
        r["learning_goal"]
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

