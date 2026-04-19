# CS3751 Data Visualization – Project Source Code

## Overview
This folder contains all Python scripts used to preprocess the quiz data,
generate visualizations, and compile the final PDF report.

## Requirements
Install dependencies with:
```
pip install pandas numpy matplotlib seaborn scipy reportlab
```

## Files

| File | Description |
|------|-------------|
| `01_data_preprocessing.py` | Loads the three quiz CSV files, parses time strings, filters incomplete/outlier attempts, computes attempt numbers, and saves `cleaned_data.csv` |
| `02_generate_visualizations.py` | Reads `cleaned_data.csv` and generates all 10 hypothesis visualizations as PNG files in the `figures/` folder |
| `03_build_report.py` | Reads `cleaned_data.csv` and all figures; assembles and exports the full project report as a PDF using ReportLab |

## How to Run

1. Place the three input files in a folder called `data/` relative to the scripts:
   - `quiz1_marks.csv`
   - `quiz2_marks.csv`
   - `quiz3_marks.csv`

   > **Note:** Update the file paths at the top of `01_data_preprocessing.py` if needed.

2. Run the scripts in order:
```bash
python 01_data_preprocessing.py   # Generates cleaned_data.csv
python 02_generate_visualizations.py  # Generates figures/*.png
python 03_build_report.py         # Generates CS3751_Project_Report.pdf
```

## Hypotheses Addressed

### Task 1 (Provided)
| ID | Hypothesis | Figure |
|----|-----------|--------|
| H1 | Longer time → higher score | H1_time_vs_score.png |
| H2 | Some questions consistently harder | H2_question_difficulty.png |
| H3 | High performers improve; low performers erratic | H3_improvement_attempts.png |
| H4 | Harder questions slower; high performers faster | H4_hard_questions_performance.png |
| H5 | Optimal time range exists | H5_optimal_time.png |

### Task 2 (Independent)
| ID | Hypothesis | Figure |
|----|-----------|--------|
| H6 | Scores decline across quizzes (fatigue) | H6_quiz_fatigue.png |
| H7 | Repeated attempts improve scores (learning) | H7_learning_effect.png |
| H8 | First attempt score predicts best score | H8_first_vs_best.png |
| H9 | High performers consistent across quizzes | H9_cross_quiz_consistency.png |
| H10 | Score distributions are bimodal | H10_bimodal_scores.png |

## Notes
- "In progress" attempts are excluded from all analyses.
- Attempts with time > 120 minutes are treated as outliers and removed.
- Performance tiers (High/Mid/Low) are based on the 67th and 33rd percentile of each student's mean grade.
