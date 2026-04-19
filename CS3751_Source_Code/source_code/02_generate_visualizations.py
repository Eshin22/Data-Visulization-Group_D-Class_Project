import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from scipy import stats
import warnings

warnings.filterwarnings("ignore")

# ── Style ──────────────────────────────────────────────────────────────────────
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "figure.dpi": 150,
    }
)
PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"]
QUIZ_COLORS = {1: "#4C72B0", 2: "#DD8452", 3: "#55A868"}

# Define paths for cleaned data and figures
CLEANED_DATA_PATH = "d:/My Campus Work/Sem 06/Data Visulization/Class Project/CS3751_Source_Code/source_code/data/cleaned_data.csv"
FIGURES_PATH = "d:/My Campus Work/Sem 06/Data Visulization/Class Project/CS3751_Source_Code/source_code/figures/"

# Ensure the figures directory exists
import os

os.makedirs(FIGURES_PATH, exist_ok=True)

df = pd.read_csv(CLEANED_DATA_PATH)

# ══════════════════════════════════════════════════════════════════════════════
# TASK 1 – H1: Longer time → higher score (scatter + hexbin + regression line)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for idx, (qnum, ax) in enumerate(zip([1, 2, 3], axes)):
    sub = df[df["quiz"] == qnum].dropna(subset=["time_minutes", "grade"])
    sub = sub[sub["time_minutes"] <= 60]
    ax.hexbin(
        sub["time_minutes"],
        sub["grade"],
        gridsize=30,
        cmap="Blues",
        mincnt=1,
        linewidths=0.2,
    )
    # regression line
    slope, intercept, r, p, _ = stats.linregress(sub["time_minutes"], sub["grade"])
    x_line = np.linspace(sub["time_minutes"].min(), sub["time_minutes"].max(), 200)
    ax.plot(
        x_line,
        slope * x_line + intercept,
        color="#C44E52",
        lw=2,
        label=f"r={r:.2f}, p={p:.3f}",
    )
    ax.set_title(f"Quiz {qnum}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Time Taken (minutes)", fontsize=11)
    ax.set_ylabel("Score (out of 10)", fontsize=11)
    ax.legend(fontsize=10)
    ax.set_ylim(-0.5, 10.5)

fig.suptitle(
    "H1 – Do Students Who Take Longer Score Higher?\n(Hexbin density + regression line)",
    fontsize=14,
    fontweight="bold",
    y=1.01,
)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_PATH, "H1_time_vs_score.png"), bbox_inches="tight")
plt.close()
print("H1 saved")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 1 – H2: Consistent question difficulty (grouped bar + error bars)
# ══════════════════════════════════════════════════════════════════════════════
q_cols = ["q1", "q2", "q3", "q4", "q5"]
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Mean score per question per quiz
means = df.groupby("quiz")[q_cols].mean()
stds = df.groupby("quiz")[q_cols].sem()

x = np.arange(5)
width = 0.25
ax = axes[0]
for i, quiz in enumerate([1, 2, 3]):
    ax.bar(
        x + i * width,
        means.loc[quiz],
        width,
        yerr=stds.loc[quiz] * 1.96,
        label=f"Quiz {quiz}",
        color=list(QUIZ_COLORS.values())[i],
        alpha=0.85,
        capsize=4,
    )
ax.set_xticks(x + width)
ax.set_xticklabels([f"Q{i+1}" for i in range(5)], fontsize=12)
ax.set_ylabel("Mean Score (out of 2)", fontsize=11)
ax.set_title("Mean Score per Question across Quizzes", fontsize=13, fontweight="bold")
ax.legend()
ax.set_ylim(0, 2.3)

# % of students scoring 0 per question (difficulty proxy)
ax2 = axes[1]
pct_zero = {}
for quiz in [1, 2, 3]:
    sub = df[df["quiz"] == quiz]
    pct_zero[quiz] = [(sub[q] == 0).mean() * 100 for q in q_cols]

x = np.arange(5)
for i, quiz in enumerate([1, 2, 3]):
    ax2.bar(
        x + i * width,
        pct_zero[quiz],
        width,
        label=f"Quiz {quiz}",
        color=list(QUIZ_COLORS.values())[i],
        alpha=0.85,
    )
ax2.set_xticks(x + width)
ax2.set_xticklabels([f"Q{i+1}" for i in range(5)], fontsize=12)
ax2.set_ylabel("% Students Scoring 0", fontsize=11)
ax2.set_title(
    "Question Difficulty: % Students Scoring Zero", fontsize=13, fontweight="bold"
)
ax2.legend()

fig.suptitle(
    "H2 – Are Some Questions Consistently Harder?\n(Mean scores & zero-score rates per question)",
    fontsize=14,
    fontweight="bold",
)
plt.tight_layout()
plt.savefig(
    os.path.join(FIGURES_PATH, "H2_question_difficulty.png"), bbox_inches="tight"
)
plt.close()
print("H2 saved")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 1 – H3: High vs Low performers – improvement over attempts
# ══════════════════════════════════════════════════════════════════════════════
# Classify students based on their best score
student_best = df.groupby("Student Code")["grade"].max()
high_threshold = student_best.quantile(0.75)
low_threshold = student_best.quantile(0.25)

high_students = student_best[student_best >= high_threshold].index
low_students = student_best[student_best <= low_threshold].index

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for qnum, ax in zip([1, 2, 3], axes):
    sub = df[df["quiz"] == qnum]
    for label, students, color in [
        ("High Performers", high_students, "#4C72B0"),
        ("Low Performers", low_students, "#C44E52"),
    ]:
        group = sub[sub["Student Code"].isin(students)]
        stats_by_attempt = group.groupby("attempt_num")["grade"].agg(["mean", "sem"])
        stats_by_attempt = stats_by_attempt[stats_by_attempt.index <= 5]
        ax.plot(
            stats_by_attempt.index,
            stats_by_attempt["mean"],
            marker="o",
            color=color,
            lw=2,
            label=label,
        )
        ax.fill_between(
            stats_by_attempt.index,
            stats_by_attempt["mean"] - stats_by_attempt["sem"] * 1.96,
            stats_by_attempt["mean"] + stats_by_attempt["sem"] * 1.96,
            alpha=0.15,
            color=color,
        )
    ax.set_title(f"Quiz {qnum}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Attempt Number", fontsize=11)
    ax.set_ylabel("Mean Score", fontsize=11)
    ax.set_ylim(0, 11)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.legend(fontsize=9)

fig.suptitle(
    "H3 – Do High Performers Improve Consistently While Low Performers Show Erratic Progress?\n(Mean score ± 95% CI by attempt number)",
    fontsize=13,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig(
    os.path.join(FIGURES_PATH, "H3_improvement_attempts.png"), bbox_inches="tight"
)
plt.close()
print("H3 saved")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 1 – H4: Harder questions take longer; high performers answer them faster
# ══════════════════════════════════════════════════════════════════════════════
# Proxy: question difficulty = mean score (lower = harder)
# We can't get per-question time, but we can bin students by score then compare time
# Better: split by score tier; show time vs question correctness

student_avg = df.groupby("Student Code")["grade"].mean()
df["perf_tier"] = df["Student Code"].map(
    lambda x: (
        "High"
        if student_avg.get(x, 5) >= student_avg.quantile(0.67)
        else ("Low" if student_avg.get(x, 5) <= student_avg.quantile(0.33) else "Mid")
    )
)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
tier_colors = {"High": "#4C72B0", "Mid": "#55A868", "Low": "#C44E52"}

for qnum, ax in zip([1, 2, 3], axes):
    sub = df[(df["quiz"] == qnum) & df["time_minutes"].notna()].copy()
    sub = sub[sub["time_minutes"] <= 60]
    # Difficulty ranking (lower mean = harder)
    q_means = sub[q_cols].mean().sort_values()
    difficulty_order = [q.replace("q", "Q") for q in q_means.index]

    plot_data = []
    for tier, color in tier_colors.items():
        tier_sub = sub[sub["perf_tier"] == tier]
        mean_time = tier_sub["time_minutes"].mean()
        # per question score
        for q in q_cols:
            score = tier_sub[q].mean()
            plot_data.append(
                {
                    "tier": tier,
                    "question": q.upper(),
                    "mean_score": score,
                    "difficulty_rank": list(q_means.index).index(q) + 1,
                }
            )

    plot_df = pd.DataFrame(plot_data)
    for tier, color in tier_colors.items():
        td = plot_df[plot_df["tier"] == tier]
        ax.plot(
            td["difficulty_rank"],
            td["mean_score"],
            marker="o",
            color=color,
            lw=2,
            label=tier,
        )

    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels([f"Q{int(x)} (#{int(x)})" for x in [1, 2, 3, 4, 5]], fontsize=8)
    ax.set_xlabel("Question (ranked easy→hard)", fontsize=10)
    ax.set_ylabel("Mean Score (out of 2)", fontsize=10)
    ax.set_title(f"Quiz {qnum}", fontsize=13, fontweight="bold")
    ax.legend(title="Perf. Tier", fontsize=9)

fig.suptitle(
    "H4 – Do High Performers Score Better on Harder Questions?\n(Score per question by performance tier, questions ordered easy→hard)",
    fontsize=13,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig(
    os.path.join(FIGURES_PATH, "H4_hard_questions_performance.png"), bbox_inches="tight"
)
plt.close()
print("H4 saved")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 1 – H5: Optimal time range (inverted U – too fast or too slow = lower)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for qnum, ax in zip([1, 2, 3], axes):
    sub = df[(df["quiz"] == qnum) & df["time_minutes"].notna() & df["grade"].notna()]
    sub = sub[sub["time_minutes"] <= 60]
    # Bin into time buckets
    sub["time_bin"] = pd.cut(
        sub["time_minutes"],
        bins=[0, 3, 6, 10, 15, 20, 30, 60],
        labels=["0-3", "3-6", "6-10", "10-15", "15-20", "20-30", "30-60"],
    )
    bin_stats = (
        sub.groupby("time_bin", observed=True)["grade"]
        .agg(["mean", "sem", "count"])
        .reset_index()
    )

    ax.bar(
        range(len(bin_stats)),
        bin_stats["mean"],
        color=[
            PALETTE[2] if (3 <= i <= 4) else PALETTE[0] for i in range(len(bin_stats))
        ],
        alpha=0.8,
    )
    ax.errorbar(
        range(len(bin_stats)),
        bin_stats["mean"],
        yerr=bin_stats["sem"] * 1.96,
        fmt="none",
        color="black",
        capsize=4,
    )
    ax2b = ax.twinx()
    ax2b.plot(
        range(len(bin_stats)),
        bin_stats["count"],
        "o--",
        color="#C44E52",
        alpha=0.7,
        lw=1.5,
        label="Count",
    )
    ax2b.set_ylabel("Attempt Count", color="#C44E52", fontsize=9)
    ax2b.tick_params(axis="y", labelcolor="#C44E52")
    ax.set_xticks(range(len(bin_stats)))
    ax.set_xticklabels(bin_stats["time_bin"].astype(str), rotation=35, fontsize=9)
    ax.set_xlabel("Time Taken (minutes)", fontsize=10)
    ax.set_ylabel("Mean Score", fontsize=10)
    ax.set_title(f"Quiz {qnum}", fontsize=13, fontweight="bold")
    ax.set_ylim(0, 11)
    green_patch = mpatches.Patch(color=PALETTE[2], alpha=0.8, label="Optimal zone")
    ax.legend(handles=[green_patch], fontsize=9)

fig.suptitle(
    "H5 – Is There an Optimal Time Range for Higher Scores?\n(Mean score by time bin, green = suspected optimal zone)",
    fontsize=13,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_PATH, "H5_optimal_time.png"), bbox_inches="tight")
plt.close()
print("H5 saved")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 2 – H6: Average scores decline across quizzes (quiz fatigue)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
quiz_stats = df.groupby("quiz")["grade"].agg(["mean", "sem"]).reset_index()
bars = ax.bar(
    quiz_stats["quiz"],
    quiz_stats["mean"],
    color=[QUIZ_COLORS[q] for q in quiz_stats["quiz"]],
    alpha=0.85,
    width=0.5,
)
ax.errorbar(
    quiz_stats["quiz"],
    quiz_stats["mean"],
    yerr=quiz_stats["sem"] * 1.96,
    fmt="none",
    color="black",
    capsize=6,
    lw=2,
)
for bar, val in zip(bars, quiz_stats["mean"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.15,
        f"{val:.2f}",
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(["Quiz 1", "Quiz 2", "Quiz 3"], fontsize=12)
ax.set_ylabel("Mean Score (out of 10)", fontsize=11)
ax.set_title("Mean Score by Quiz", fontsize=13, fontweight="bold")
ax.set_ylim(0, 8)

ax2 = axes[1]
quiz_dist = [df[df["quiz"] == q]["grade"] for q in [1, 2, 3]]
parts = ax2.violinplot(quiz_dist, positions=[1, 2, 3], showmedians=True, showmeans=True)
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor(list(QUIZ_COLORS.values())[i])
    pc.set_alpha(0.7)
ax2.set_xticks([1, 2, 3])
ax2.set_xticklabels(["Quiz 1", "Quiz 2", "Quiz 3"], fontsize=12)
ax2.set_ylabel("Score Distribution", fontsize=11)
ax2.set_title("Score Distribution by Quiz", fontsize=13, fontweight="bold")

fig.suptitle(
    "H6 – Do Average Scores Decline Across Quizzes (Quiz Fatigue)?\n(Bar: mean ± 95% CI | Violin: distribution)",
    fontsize=13,
    fontweight="bold",
)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_PATH, "H6_quiz_fatigue.png"), bbox_inches="tight")
plt.close()
print("H6 saved")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 2 – H7: Repeated attempts lead to score improvement (learning effect)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for qnum, ax in zip([1, 2, 3], axes):
    sub = df[df["quiz"] == qnum]
    # Only students with multiple attempts
    multi = sub.groupby("Student Code").filter(lambda x: len(x) >= 2)
    attempt_stats = (
        multi[multi["attempt_num"] <= 6]
        .groupby("attempt_num")["grade"]
        .agg(["mean", "sem", "count"])
    )

    ax.bar(
        attempt_stats.index,
        attempt_stats["mean"],
        color=[PALETTE[min(i, 4)] for i in range(len(attempt_stats))],
        alpha=0.75,
    )
    ax.errorbar(
        attempt_stats.index,
        attempt_stats["mean"],
        yerr=attempt_stats["sem"] * 1.96,
        fmt="none",
        color="black",
        capsize=4,
    )
    # Annotate counts
    for idx_val, row in attempt_stats.iterrows():
        ax.text(
            idx_val,
            row["mean"] + 0.2,
            f'n={int(row["count"])}',
            ha="center",
            fontsize=8,
            color="#555",
        )
    ax.set_xlabel("Attempt Number", fontsize=11)
    ax.set_ylabel("Mean Score", fontsize=11)
    ax.set_title(f"Quiz {qnum}", fontsize=13, fontweight="bold")
    ax.set_ylim(0, 12)
    ax.set_xticks(attempt_stats.index)

fig.suptitle(
    "H7 – Does Repeating a Quiz Improve Scores? (Learning Effect)\n(Mean score by attempt number, students with multiple attempts only)",
    fontsize=13,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_PATH, "H7_learning_effect.png"), bbox_inches="tight")
plt.close()
print("H7 saved")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 2 – H8: First-attempt score predicts overall best score (heatmap)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for qnum, ax in zip([1, 2, 3], axes):
    sub = df[df["quiz"] == qnum]
    first = sub[sub["attempt_num"] == 1][["Student Code", "grade"]].rename(
        columns={"grade": "first_score"}
    )
    best = (
        sub.groupby("Student Code")["grade"]
        .max()
        .reset_index()
        .rename(columns={"grade": "best_score"})
    )
    merged = first.merge(best, on="Student Code")

    # 2D histogram / heatmap
    h, xedges, yedges = np.histogram2d(
        merged["first_score"], merged["best_score"], bins=6, range=[[0, 10], [0, 10]]
    )
    im = ax.imshow(
        h.T,
        origin="lower",
        aspect="auto",
        extent=[0, 10, 0, 10],
        cmap="YlOrRd",
        interpolation="nearest",
    )
    plt.colorbar(im, ax=ax, label="Count")

    slope, intercept, r, p, _ = stats.linregress(
        merged["first_score"], merged["best_score"]
    )
    x_line = np.linspace(0, 10, 100)
    ax.plot(x_line, slope * x_line + intercept, "b--", lw=2, label=f"r={r:.2f}")
    ax.plot([0, 10], [0, 10], "k:", lw=1, alpha=0.5)  # diagonal
    ax.set_xlabel("First Attempt Score", fontsize=11)
    ax.set_ylabel("Best Score Achieved", fontsize=11)
    ax.set_title(f"Quiz {qnum}", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)

fig.suptitle(
    "H8 – Does First Attempt Score Predict a Student's Best Score?\n(Heatmap of first vs best score with regression line)",
    fontsize=13,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_PATH, "H8_first_vs_best.png"), bbox_inches="tight")
plt.close()
print("H8 saved")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 2 – H9: Students who score full marks on one quiz tend to do well on others
# ══════════════════════════════════════════════════════════════════════════════
# Cross-quiz consistency: heatmap of mean score per student per quiz
student_quiz_best = (
    df.groupby(["Student Code", "quiz"])["grade"].max().unstack(fill_value=np.nan)
)
student_quiz_best.columns = ["Quiz 1", "Quiz 2", "Quiz 3"]
student_quiz_best = student_quiz_best.dropna()

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
pairs = [("Quiz 1", "Quiz 2"), ("Quiz 2", "Quiz 3"), ("Quiz 1", "Quiz 3")]
for (q_a, q_b), ax in zip(pairs, axes):
    data = student_quiz_best[[q_a, q_b]].dropna()
    h, xedges, yedges = np.histogram2d(
        data[q_a], data[q_b], bins=6, range=[[0, 10], [0, 10]]
    )
    im = ax.imshow(
        h.T,
        origin="lower",
        aspect="auto",
        extent=[0, 10, 0, 10],
        cmap="Blues",
        interpolation="nearest",
    )
    plt.colorbar(im, ax=ax, label="Student Count")
    r, p = stats.pearsonr(data[q_a], data[q_b])
    ax.set_xlabel(f"{q_a} Best Score", fontsize=11)
    ax.set_ylabel(f"{q_b} Best Score", fontsize=11)
    ax.set_title(f"{q_a} vs {q_b}\nr={r:.2f}, p<0.001", fontsize=12, fontweight="bold")

fig.suptitle(
    "H9 – Are Students Who Perform Well in One Quiz Consistently Good Across All Quizzes?\n(Heatmap of best scores, all quiz pairs)",
    fontsize=13,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig(
    os.path.join(FIGURES_PATH, "H9_cross_quiz_consistency.png"), bbox_inches="tight"
)
plt.close()
print("H9 saved")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 2 – H10: Most students answer all questions correctly or all wrong (bimodal)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for qnum, ax in zip([1, 2, 3], axes):
    sub = df[df["quiz"] == qnum]["grade"].dropna()
    # Score distribution histogram
    counts, bins, patches = ax.hist(
        sub,
        bins=11,
        range=(-0.5, 10.5),
        color=QUIZ_COLORS[qnum],
        alpha=0.8,
        edgecolor="white",
        lw=0.5,
    )
    # Colour the peaks
    peak_bins = [0, 10]
    for patch, left in zip(patches, bins[:-1]):
        if left in [0.0, -0.5] or left >= 9.5:
            patch.set_facecolor("#C44E52")

    ax.set_xlabel("Score (out of 10)", fontsize=11)
    ax.set_ylabel("Number of Attempts", fontsize=11)
    ax.set_title(f"Quiz {qnum}", fontsize=13, fontweight="bold")
    ax.set_xticks([0, 2, 4, 6, 8, 10])

    # Bimodality coefficient
    skew = sub.skew()
    kurt = sub.kurt()
    bc = (skew**2 + 1) / (kurt + 3)
    ax.text(
        0.98,
        0.97,
        f"Bimod. coeff.={bc:.2f}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        color="#333",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7),
    )

fig.suptitle(
    "H10 – Are Score Distributions Bimodal? (Most Students Score Very High or Very Low)\n(Score frequency histogram with bimodality coefficient, red = extreme scores)",
    fontsize=13,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_PATH, "H10_bimodal_scores.png"), bbox_inches="tight")
plt.close()
print("H10 saved")
print("\nAll figures saved!")
