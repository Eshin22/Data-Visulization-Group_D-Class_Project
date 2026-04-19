import pandas as pd
import numpy as np
import re

# Configuration paths
DATA_PATH = "d:/My Campus Work/Sem 06/Data Visulization/Class Project/CS3751_Source_Code/source_code/data/"
SAVE_PATH = "d:/My Campus Work/Sem 06/Data Visulization/Class Project/CS3751_Source_Code/source_code/data/cleaned_data.csv"


def parse_time_seconds(time_str):
    if pd.isna(time_str) or str(time_str).strip() in ["-", ""]:
        return np.nan
    time_str = str(time_str).strip()
    total_seconds = 0
    days = re.search(r"(\d+)\s*day", time_str)
    hours = re.search(r"(\d+)\s*hour", time_str)
    mins = re.search(r"(\d+)\s*min", time_str)
    secs = re.search(r"(\d+)\s*sec", time_str)
    if days:
        total_seconds += int(days.group(1)) * 86400
    if hours:
        total_seconds += int(hours.group(1)) * 3600
    if mins:
        total_seconds += int(mins.group(1)) * 60
    if secs:
        total_seconds += int(secs.group(1))
    return total_seconds if total_seconds > 0 else np.nan


def load_and_clean():
    dfs = []
    for i in range(1, 4):
        df = pd.read_csv(f"{DATA_PATH}quiz{i}_marks.csv")
        df["quiz"] = i
        df.columns = [c.strip() for c in df.columns]
        # Keep only finished attempts
        df = df[df["State"] == "Finished"].copy()
        # Parse grade
        df["grade"] = pd.to_numeric(df["Grade/10.00"], errors="coerce")
        # Parse time
        df["time_seconds"] = df["Time taken"].apply(parse_time_seconds)
        df["time_minutes"] = df["time_seconds"] / 60
        # Parse question marks
        for q in range(1, 6):
            col = f"Q. {q} /2.00"
            df[f"q{q}"] = pd.to_numeric(df[col], errors="coerce")
        # Remove outliers in time (> 2 hours likely left browser open)
        df = df[df["time_seconds"] <= 7200]
        dfs.append(df)
    combined = pd.concat(dfs, ignore_index=True)
    # Add attempt number per student per quiz
    combined = combined.sort_values(["Student Code", "quiz", "Started on"])
    combined["attempt_num"] = combined.groupby(["Student Code", "quiz"]).cumcount() + 1
    print("Combined shape:", combined.shape)
    print("Quizzes:", combined["quiz"].value_counts().sort_index())
    print("Grade stats:\n", combined["grade"].describe())
    print("Time stats (mins):\n", combined["time_minutes"].describe())
    return combined


df = load_and_clean()
df.to_csv(SAVE_PATH, index=False)
print("\nSaved cleaned data")
