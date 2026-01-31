import pandas as pd
import pickle
import os
import ast

# ================================
# CONFIG
# ================================
CSV_PATH = r"D:\BABY_PARENT_Assistant_PROJECT\parents_dataset\25_60_data_parent.csv"
MODEL_PATH = r"models/parent_25_60.pkl"

os.makedirs("models", exist_ok=True)

# ================================
# HELPERS
# ================================
def normalize_text(text):
    if pd.isna(text):
        return ""
    return str(text).strip().lower()


def safe_list(value):
    """Ensure list-type columns are usable."""
    if isinstance(value, list):
        return value
    try:
        return ast.literal_eval(value)
    except:
        return [str(value)]


def create_parent_steps(row):
    """
    Parent-focused steps (MAX 5)
    Dataset-specific logic for 25–60 months
    """
    steps = []

    steps.append(f"Step 1 — Understand the goal: {row['parent_learning_goal']}")

    steps.append(
        f"Step 2 — Focus on the skill: {row['skill_name']} in daily routines."
    )

    steps.append(
        f"Step 3 — How to guide: {row['how_to_teach']}"
    )

    dos = safe_list(row["parent_dos"])
    if dos:
        steps.append(
            f"Step 4 — What to do: {', '.join(dos[:2])}"
        )
    else:
        steps.append("Step 4 — Stay calm, patient, and consistent.")

    steps.append(
        f"Step 5 — Remember: {row['parent_tip']}"
    )

    return steps[:5]


# ================================
# LOAD DATA
# ================================
df = pd.read_csv(CSV_PATH)

print(f"✅ Dataset loaded: {df.shape}")

# ================================
# PROCESS INPUT
# ================================
df["processed_input"] = (
    df["domain"].apply(normalize_text) + " | " +
    df["skill_name"].apply(normalize_text) + " | " +
    df["parent_learning_goal"].apply(normalize_text)
)

# ================================
# CREATE STEPS
# ================================
df["steps"] = df.apply(create_parent_steps, axis=1)

# ================================
# SAVE MODEL
# ================================
with open(MODEL_PATH, "wb") as f:
    pickle.dump(df, f)

print("✅ Training complete")
print(f"✅ Model saved to: {MODEL_PATH}")
print(f"✅ Columns: {list(df.columns)}")

