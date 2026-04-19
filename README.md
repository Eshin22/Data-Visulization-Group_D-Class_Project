# CS3751 Data Visualization – Class Project

## Quiz Performance Analysis & Hypothesis Verification

---

## 📋 Project Overview

This project analyzes student performance data across three quizzes to identify patterns in learning behavior, attempt strategies, and the relationship between time spent and academic performance. Through a series of carefully designed visualizations, we test **10 hypotheses** (5 provided + 5 independent) using principles of effective data visualization design.

**Course:** CS3751 Data Visualization  
**Type:** Group Project (30% of final grade)  
**Submission:** Complete project report (PDF) + source code (Zip)

---

## 📊 Dataset

The dataset contains detailed attempt records for three quizzes with the following attributes:

- **Student Code**: Unique student identifier
- **Quiz Number**: Quiz 1, 2, or 3
- **Attempt Number**: Sequential attempt (1st, 2nd, 3rd+)
- **Started On**: Timestamp of attempt start
- **Time Taken**: Total duration in minutes
- **Grade**: Total score out of 10
- **Individual Question Marks**: Breakdown of marks for questions 1-5 (q1–q5)

**Key Characteristic:** Students may attempt each quiz multiple times, allowing analysis of learning improvement patterns.

---

## 🎯 Hypotheses at a Glance

### **Task 1: Provided Hypotheses** (5 hypotheses)

| #      | Hypothesis                                                                         | Visualization Type                   | Key Finding                                                 |
| ------ | ---------------------------------------------------------------------------------- | ------------------------------------ | ----------------------------------------------------------- |
| **H1** | Students who take **longer** to complete the quiz tend to score **higher**         | Box Plot with Red-Gradient Means     | Time investment correlates with performance                 |
| **H2** | Some questions are **consistently harder** than others                             | Grouped Bar Chart                    | Question 4 (Quizzes 1-2) and Q3 (Quiz 3) are most difficult |
| **H3** | **High performers consistently improve** over attempts; **low performers erratic** | Slopegraph + Individual Trajectories | Clear divergence in improvement patterns                    |
| **H4** | **Harder questions take longer**, but **high performers answer faster**            | Violin Plot + Strip Plot             | Performance group affects time-to-difficulty relationship   |
| **H5** | **Optimal time range exists**; too fast/slow students score lower                  | Point Plot with Error Bars           | Bell-curve pattern around 15-30 minute range                |

### **Task 2: Independent Hypotheses** (5 hypotheses)

| #         | Hypothesis                                                      | Visualization Type              | Conclusion                        |
| --------- | --------------------------------------------------------------- | ------------------------------- | --------------------------------- |
| **T2-H1** | **Lower first-attempt scores** lead to **more retries**         | Line Plot with IQR Ribbon       | Spearman correlation test         |
| **T2-H2** | **Attempt 1→2 shows strongest gain**; diminishing returns after | Multi-series Line Plot          | Marginal gain visualization       |
| **T2-H3** | **Shorter time gaps between retries** → **larger improvements** | Box Plot by Time Bins           | Temporal spacing affects learning |
| **T2-H4** | **Reaching 8+ score plateaus** after 3 attempts                 | Area Chart + Marginal Gain Bars | Saturation effect detected        |
| **T2-H5** | **First-attempt performance improves** across quiz sequence     | Bar Chart with 95% CI           | Cross-quiz learning trend         |

---

## 📁 Project Structure

```
Class Project/
├── README.md                                 # This file
├── Group-D-Final_Notebook.ipynb              # Main analysis notebook
│
├── CS3751_Source_Code/
│   └── source_code/
│       ├── 01_data_preprocessing.py         # Data cleaning & preparation
│       ├── 02_generate_visualizations.py    # Hypothesis visualization generation
│       ├── README.md                        # Code documentation
│       │
│       ├── data/
│       │   ├── quiz1_marks.csv              # Raw Quiz 1 data
│       │   ├── quiz2_marks.csv              # Raw Quiz 2 data
│       │   ├── quiz3_marks.csv              # Raw Quiz 3 data
│       │   └── cleaned_data.csv             # Preprocessed dataset
│       │
│       └── figures/
│           ├── grouped_boxplot_60min.png    # H1 visualization
│           ├── grouped_bar_quiz_*.png       # H2 visualizations
│           ├── progress_analysis_quiz_*.png # H3 visualizations
│           ├── quiz_*_analysis.png          # H4 visualizations
│           ├── optimal_time_*.png           # H5 visualization
│           ├── (T2 hypothesis figures)      # Task 2 visualizations
│           └── ...
│
├── dataset/
│   └── marks/                               # Original data source
│       ├── quiz1/, quiz2/, quiz3/
│       └── quiz*_marks.csv
│
└── [Project Report PDF]                     # Final submission document
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **Jupyter Notebook** (for interactive analysis)

### Installation

1. **Clone/download the repository** and navigate to the project folder:

```bash
cd "d:\My Campus Work\Sem 06\Data Visulization\Class Project"
```

2. **Install required packages:**

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn reportlab
```

**Package Details:**

- `pandas`: Data manipulation & CSV I/O
- `numpy`: Numerical computations
- `matplotlib` & `seaborn`: Visualization rendering
- `scipy`: Statistical tests (Spearman, Kruskal-Wallis)
- `scikit-learn`: (Optional) Additional ML utilities

### Running the Analysis

#### **Option A: Interactive Jupyter Notebook** (Recommended)

```bash
jupyter notebook "Group-D-Final_Notebook.ipynb"
```

- Run cells sequentially to explore each hypothesis
- Modify parameters (e.g., quiz selection, attempt filtering) interactively
- Visualizations render inline for immediate review

#### **Option B: Command-Line Scripts**

Navigate to `CS3751_Source_Code/source_code/` and run:

```bash
# Step 1: Preprocess raw data
python 01_data_preprocessing.py
# Output: data/cleaned_data.csv

# Step 2: Generate all visualizations
python 02_generate_visualizations.py
# Output: PNG files in figures/
```

---

## � Data Preprocessing & cleaned_data.csv Generation

### **What is cleaned_data.csv?**

The `cleaned_data.csv` file is the **preprocessed dataset** generated from the raw quiz CSV files. It combines and standardizes all three quizzes (quiz1_marks.csv, quiz2_marks.csv, quiz3_marks.csv) into a single analysis-ready file.

### **Raw Data Files** (Input)

The three raw CSV files are located in `data/` folder:

- **quiz1_marks.csv** - Raw Quiz 1 attempt data
- **quiz2_marks.csv** - Raw Quiz 2 attempt data
- **quiz3_marks.csv** - Raw Quiz 3 attempt data

Each raw file contains:

- Student Code
- Attempt start time
- Attempt end time
- Time taken (in various formats)
- Grade (out of 10)
- Individual question marks (q1, q2, q3, q4, q5)

### **Data Preprocessing Steps** (01_data_preprocessing.py)

The `01_data_preprocessing.py` script performs the following operations:

#### **1. Load & Merge**

- Reads all three quiz CSV files independently
- Adds a `quiz` column to identify which quiz the record belongs to (1, 2, or 3)
- Concatenates all data into a single DataFrame

#### **2. Time Parsing & Standardization**

- Converts `time_taken` column from various string formats to numeric minutes
- Handles different time formats: "HH:MM:SS", "MM:SS", simple minutes, etc.
- Creates `time_minutes` column for consistent time-based analysis

#### **3. Attempt Numbering**

- Identifies duplicate students within each quiz (multiple attempts)
- Assigns sequential `attempt_num` (1st attempt, 2nd attempt, 3rd+ attempt)
- Sorted by student and start time to ensure correct attempt ordering

#### **4. Data Validation & Cleaning**

- Removes incomplete records (missing grade, student code, or quiz number)
- Filters outliers (e.g., attempts with 0 minutes time, invalid grades)
- Validates that all question marks (q1-q5) are numeric and between 0-2
- Removes duplicate entries (same student, same quiz, same timestamp)

#### **5. Column Standardization**

- Ensures consistent column naming across all records
- Casts data types correctly (integer for codes/quiz/attempt, float for grades/times)
- Calculates derived metrics if needed

### **Output: cleaned_data.csv**

The cleaned file contains the following columns:

| Column                       | Type     | Description                                |
| ---------------------------- | -------- | ------------------------------------------ |
| `Student Code`               | int      | Unique student identifier                  |
| `quiz`                       | int      | Quiz number (1, 2, or 3)                   |
| `attempt_num`                | int      | Sequential attempt number (1st, 2nd, 3rd+) |
| `Started on`                 | datetime | Timestamp when attempt started             |
| `time_minutes`               | float    | Time taken in minutes (standardized)       |
| `grade`                      | float    | Final grade out of 10                      |
| `q1`, `q2`, `q3`, `q4`, `q5` | float    | Individual question scores (0-2 each)      |

**Total Records:** ~2,000+ cleaned attempt records (exact count depends on filtering)

### **How to Generate cleaned_data.csv**

```bash
# Navigate to the source code folder
cd "CS3751_Source_Code/source_code"

# Make sure the raw data files are in the data/ folder:
# - data/quiz1_marks.csv
# - data/quiz2_marks.csv
# - data/quiz3_marks.csv

# Run the preprocessing script
python 01_data_preprocessing.py

# This will output: data/cleaned_data.csv
```

## �📈 Visualization Design Principles Used

### **Marks & Channels** (per visualization)

#### **Position & Length** (Most Effective for Numerical Comparisons)

- **Box Plots** (H1, T2-H3): Position on y-axis shows grade distribution; box length shows IQR
- **Bar Charts** (H2, T2-H5): Length encodes average score per question/quiz
- **Line Plots** (T2-H1, T2-H2): Position on both axes shows score vs. attempt/time

#### **Color** (Categorical & Quantitative Encoding)

- **Red Gradient** (H1): Light→Dark red intensity encodes mean grade value
- **Sequential Blue** (H2): Darker blue = later attempts (natural progression)
- **Categorical Palette** (T2-H2): Set1 colors distinguish quizzes clearly
- **White Median Ticks** (T2-H5): Contrasts with blue bars for visibility

#### **Area** (Distribution & Density)

- **Violin Plots** (H4): Width shows probability density; quartile bands aid interpretation
- **Fill Under Curve** (T2-H4): Area emphasizes total attainment trajectory
- **IQR Ribbons** (T2-H1): Shaded band shows middle 50% of data

#### **Size & Opacity**

- **Scatter Plots**: Larger dots for important statistics (e.g., mean); alpha=0.1–0.3 for jittered points reduces overplotting
- **Error Bars**: 95% CI half-widths show confidence bounds on means

### **Design Decisions**

1. **Whitegrid Background** (`sns.set_theme(style="whitegrid")`)
   - Light gridlines aid precise value reading
   - White background ensures print clarity

2. **Color-Blind Friendly**
   - Palettes tested for deuteranopia/protanopia compatibility
   - Avoid red-green contrasts alone; combine with size/pattern

3. **Title & Label Clarity**
   - Left-aligned titles for visual hierarchy
   - Y-axis labels as questions (not statements) for quick scanning

4. **Statistical Annotation**
   - Mono-space font for test results (e.g., "Spearman ρ = 0.456, p = 0.002")
   - Color-coded verdict boxes (green=Accepted, red=Rejected)

5. **Responsive Legend Placement**
   - Legends positioned outside plots (`bbox_to_anchor`) to avoid covering data
   - Sorted order (e.g., attempts 1→2→3+) match visual order

---

## 📊 Results Summary

### **Task 1 Findings**

| H1  | ❌ **REJECTED** | Moderate time (5–20 min) performs best; very long times have lower scores |
| --- | --------------- | ------------------------------------------------------------------------- |
| H2  | ✅ **ACCEPTED** | Question 4 (Q1-Q2) and Q3 (Q3) consistently harder; lower mean scores     |
| H3  | ❌ **REJECTED** | High performers plateau (ceiling effect); low performers improve steadily |
| H4  | ❌ **REJECTED** | Time distributions overlap substantially; no consistent speed advantage   |
| H5  | ❌ **REJECTED** | Faster completion correlates with higher grades; no inverted-U peak       |

### **Task 2 Findings**

| T2-H1 | ✅ **ACCEPTED** | Students scoring 0–2 initially typically retried twice; students scoring 4+ stopped after one attempt |
| ----- | --------------- | ----------------------------------------------------------------------------------------------------- |
| T2-H2 | ❌ **REJECTED** | Only Quiz 3 shows strong early gain; Quizzes 1 and 2 remain flat across early attempts                |
| T2-H3 | ✅ **ACCEPTED** | Immediate retries show largest median improvement; longer delays show marginal gains                  |
| T2-H4 | ✅ **ACCEPTED** | Most 8+ attainment happens by Attempts 2–3; gains become marginal after                               |
| T2-H5 | ✅ **ACCEPTED** | First-attempt mean increases from 3.37 → 4.66 → 6.18 across Quiz 1–3 (cumulative learning)            |

---

## 🤝 Group Information

**Group:** D

| Index No. | Name                   |
| --------- | ---------------------- |
| 220538D   | A.C.H. Rupasinghe      |
| 220138C   | D.M.S.H. Dissanayake   |
| 220144P   | J.S.P. Diwakar         |
| 220234R   | I.M.D.P. Illangasinghe |
| 220165F   | K.A.E.M. Fernando      |

**Submission Date:** [Add submission deadline]  
**Course:** CS3751 Data Visualization (Semester 6)
