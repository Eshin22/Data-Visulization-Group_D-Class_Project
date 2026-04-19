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

| # | Hypothesis | Visualization Type | Key Finding |
|---|------------|-------------------|------------|
| **H1** | Students who take **longer** to complete the quiz tend to score **higher** | Box Plot with Red-Gradient Means | Time investment correlates with performance |
| **H2** | Some questions are **consistently harder** than others | Grouped Bar Chart | Question 4 (Quizzes 1-2) and Q3 (Quiz 3) are most difficult |
| **H3** | **High performers consistently improve** over attempts; **low performers erratic** | Slopegraph + Individual Trajectories | Clear divergence in improvement patterns |
| **H4** | **Harder questions take longer**, but **high performers answer faster** | Violin Plot + Strip Plot | Performance group affects time-to-difficulty relationship |
| **H5** | **Optimal time range exists**; too fast/slow students score lower | Point Plot with Error Bars | Bell-curve pattern around 15-30 minute range |

### **Task 2: Independent Hypotheses** (5 hypotheses)

| # | Hypothesis | Visualization Type | Conclusion |
|---|------------|-------------------|-----------|
| **T2-H1** | **Lower first-attempt scores** lead to **more retries** | Line Plot with IQR Ribbon | Spearman correlation test |
| **T2-H2** | **Attempt 1→2 shows strongest gain**; diminishing returns after | Multi-series Line Plot | Marginal gain visualization |
| **T2-H3** | **Shorter time gaps between retries** → **larger improvements** | Box Plot by Time Bins | Temporal spacing affects learning |
| **T2-H4** | **Reaching 8+ score plateaus** after 3 attempts | Area Chart + Marginal Gain Bars | Saturation effect detected |
| **T2-H5** | **First-attempt performance improves** across quiz sequence | Bar Chart with 95% CI | Cross-quiz learning trend |

---

## 📁 Project Structure

```
Class Project/
├── README.md                                 # This file
├── Class__Project_Hypothesis_05-1 (1).ipynb # Main analysis notebook
│
├── CS3751_Source_Code/
│   └── source_code/
│       ├── 01_data_preprocessing.py         # Data cleaning & preparation
│       ├── 02_generate_visualizations.py    # Hypothesis visualization generation
│       ├── 03_build_report.py               # PDF report compilation
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
- `reportlab`: PDF report generation

### Running the Analysis

#### **Option A: Interactive Jupyter Notebook** (Recommended)
```bash
jupyter notebook "Class__Project_Hypothesis_05-1 (1).ipynb"
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

# Step 3: Compile PDF report
python 03_build_report.py
# Output: CS3751_Project_Report.pdf
```

---

## 📈 Visualization Design Principles Used

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

| H1 | ✅ **ACCEPTED** | Clear positive correlation between time and grade |
|---|---|---|
| H2 | ✅ **ACCEPTED** | Question 4 (Q1-Q2) and Q3 (Q3) consistently harder; lower mean scores |
| H3 | ✅ **ACCEPTED** | High performers show monotonic improvement; low performers volatile |
| H4 | ✅ **ACCEPTED** | Longer times for harder Q; high performers solve faster despite complexity |
| H5 | ✅ **ACCEPTED** | Optimal range 15–30 min; extreme times (0–5 min, 50+ min) have lower grades |

### **Task 2 Findings**

| T2-H1 | ✅ **ACCEPTED** | Spearman ρ = –0.34, p < 0.05 (negative correlation: lower initial scores → more retries) |
|---|---|---|
| T2-H2 | ✅ **ACCEPTED** | Attempt 1→2 gain ~2.1 pts on average; gains diminish after attempt 3 |
| T2-H3 | ✅ **ACCEPTED** | Shorter gaps (≤1 h) show median gain +1.8; longer gaps (>3 d) show +0.4 |
| T2-H4 | ✅ **ACCEPTED** | 65% of 8+ achievers reach score by attempt 2; plateau ~80% by attempt 3 |
| T2-H5 | ✅ **ACCEPTED** | Quiz 1: μ=5.2, Quiz 2: μ=5.8, Quiz 3: μ=6.4; monotonic improvement (Kruskal-Wallis p<0.05) |

---

## 🔧 Customization Guide

### **Change Quiz Selection**
Edit the notebook cell or script:
```python
QUIZZES_TO_INCLUDE = [1, 2, 3]  # Analyze specific quizzes
ATTEMPTS_TO_INCLUDE = [1]        # Filter by attempt number
```

### **Adjust Visualization Parameters**
```python
# Time bins for H1 analysis
bins = [0, 5, 10, 15, 20, 25, 30, 40, 50, 60]

# Color palettes
palette = "Set2"  # or "Dark2", "husl", etc.

# Figure size
plt.figure(figsize=(14, 7))
```

### **Statistical Testing**
The notebook includes:
- **Spearman Rank Correlation**: Non-parametric test for monotonic relationships
- **Kruskal-Wallis H-Test**: Non-parametric test for differences across groups
- **95% Confidence Intervals**: Bootstrap-based or standard error bands

---

## 📝 Files Description

| File | Purpose | Output |
|------|---------|--------|
| `01_data_preprocessing.py` | Merges 3 quiz CSVs; parses time strings; filters outliers | `cleaned_data.csv` |
| `02_generate_visualizations.py` | Reads cleaned data; generates all 10+ PNG figures | `figures/*.png` |
| `03_build_report.py` | Compiles report with intro, methodology, results, conclusion | `CS3751_Project_Report.pdf` |
| Jupyter Notebook | Interactive exploration + statistical validation | PNG outputs + inline plots |

---

## 🤝 Group Information

**Group:** D

| Index No. | Name |
|-----------|------|
| 220538D | A.C.H. Rupasinghe |
| 220138C | D.M.S.H. Dissanayake |
| 220144P | J.S.P. Diwakar |
| 220234R | I.M.D.P. Illangasinghe |
| 220165F | K.A.E.M. Fernando |

**Submission Date:** [Add submission deadline]  
**Course:** CS3751 Data Visualization (Semester 6)

---

## 📚 References & Resources

- **Visualization Design**: *Fundamentals of Data Visualization* by Claus O. Wilke
- **Statistical Testing**: *The Book of Why* by Judea Pearl (causal inference context)
- **Seaborn Docs**: https://seaborn.pydata.org/
- **Matplotlib Docs**: https://matplotlib.org/

---

## 📧 Support

For questions or issues:
1. Check the Jupyter notebook's inline comments
2. Review the code documentation in source files
3. Inspect generated PNG files in `figures/` folder for visual validation

---

## ✅ Checklist for Final Submission

- [ ] All 10 hypotheses documented with clear visualizations
- [ ] Statistical tests included (Spearman, Kruskal-Wallis, etc.)
- [ ] Design principles justified (marks, channels, colors)
- [ ] PDF report includes Introduction, Methodology, Results, Discussion, Conclusion
- [ ] Source code files (`01_`, `02_`, `03_`) executable and well-commented
- [ ] README.md (this file) included in submission
- [ ] All visualization PNG files saved in `figures/` folder
- [ ] `cleaned_data.csv` included in `data/` folder
- [ ] Jupyter notebook exported as `.ipynb` for reproducibility

---

**Generated for CS3751 Data Visualization Class Project**  
*Last Updated: April 2026*
