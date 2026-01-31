import pandas as pd
import pickle
import os
import ast

# ================================
# CONFIG
# ================================
CSV_PATH = r"D:\BABY_PARENT_Assistant_PROJECT\parents_dataset\5_12_year_data_parent.csv"
MODEL_PATH = r"models/parent_5_12.pkl"

os.makedirs("models", exist_ok=True)

# ================================
# HELPERS
# ================================
def normalize_text(text):
    if pd.isna(text):
        return ""
    return str(text).strip().lower()


def safe_list(value):
    """Safely convert stringified lists to Python lists."""
    if isinstance(value, list):
        return value
    try:
        return ast.literal_eval(value)
    except:
        return [str(value)]


def create_parent_steps(row):
    """
    Parent-focused, age-appropriate steps for 5–12 years
    MAX 5 steps only
    """
    steps = []

    # Step 1: Goal clarity
    steps.append(
        f"Step 1 — Understand the goal: {row['parent_learning_goal']}"
    )

    # Step 2: Skill focus
    steps.append(
        f"Step 2 — Focus on building this skill: {row['skill_name']}."
    )

    # Step 3: Teaching approach
    steps.append(
        f"Step 3 — How to guide the child: {row['how_to_teach']}"
    )

    # Step 4: Practical dos
    dos = safe_list(row["parent_dos"])
    if dos:
        steps.append(
            f"Step 4 — What to practice daily: {', '.join(dos[:2])}"
        )
    else:
        steps.append(
            "Step 4 — Stay patient, supportive, and consistent."
        )

    # Step 5: Reinforcement
    steps.append(
        f"Step 5 — Parent tip to remember: {row['parent_tip']}"
    )

    return steps[:5]


# ================================
# LOAD DATA
# ================================
df = pd.read_csv(CSV_PATH)
print(f"✅ Dataset loaded: {df.shape}")

# ================================
# CREATE PROCESSED INPUT
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

