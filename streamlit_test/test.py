import pickle
import os
import pandas as pd

MODEL_DIR = "models"

def inspect_models():
    report = {}

    for file in os.listdir(MODEL_DIR):
        if not file.endswith(".pkl"):
            continue

        path = os.path.join(MODEL_DIR, file)
        df = pickle.load(open(path, "rb"))

        model_name = file.replace(".pkl", "")

        info = {
            "rows": len(df),
            "columns": list(df.columns),
            "domain_values": None,
            "topic_columns": []
        }

        # Domain inspection
        if "domain" in df.columns:
            info["domain_values"] = sorted(
                df["domain"].dropna().unique().tolist()
            )

        # Topic / skill fallback columns
        for col in [
            "topic",
            "skill",
            "skill_name",
            "activity",
            "subject",
            "example_type"
        ]:
            if col in df.columns:
                info["topic_columns"].append(col)

        report[model_name] = info

    return report


if __name__ == "__main__":
    report = inspect_models()

    for model, info in report.items():
        print("=" * 60)
        print(f"MODEL: {model}")
        print(f"Rows: {info['rows']}")
        print("Columns:")
        print(info["columns"])

        if info["domain_values"]:
            print("\nDomain values:")
            for d in info["domain_values"]:
                print(" -", d)
        else:
            print("\nNo domain column found.")

        if info["topic_columns"]:
            print("Topic / skill columns found:", info["topic_columns"])
        else:
            print("No topic-like columns found.")

