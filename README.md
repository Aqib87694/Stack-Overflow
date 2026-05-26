# 📊 Stack Overflow Developer Survey 2023 — Analytics Dashboard

**Course:** Exploratory Data Analysis
**Instructor:** Ali Hassan Sherazi
**Submission Date:** 05-June-2026
**Dataset:** `survey_results_public.csv` — Stack Overflow Developer Survey 2023

---

## 📋 Project Overview

An interactive, professional-grade data visualisation dashboard analysing **89,184** developer survey responses across **84 features**. Built with **Streamlit**, **Pandas**, **Matplotlib**, and **Seaborn**. Includes **10 required chart types**, **8 interactive filters**, **10 KPI summary cards**, and a **bonus bubble chart**.

---

## 🛠️ Installation & Setup

### 1. Unzip the project
```bash
unzip so_dashboard.zip
cd so_dashboard
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
streamlit run app.py
```

Opens at **http://localhost:8501**

---

## 📂 Folder Structure

```
so_dashboard/
├── data/
│   ├── survey_results_public.csv     ← MAIN DATASET (DO NOT rename)
│   ├── survey_results_schema.csv     ← Column descriptions
│   └── README_2023.txt               ← Original dataset README
├── notebooks/
│   └── analysis.ipynb                ← EDA notebook
├── app.py                            ← Main Streamlit dashboard
├── charts.py                         ← All chart/visualisation functions
├── filters.py                        ← Data loading, cleaning & filter logic
├── requirements.txt                  ← Python dependencies
└── README.md                         ← This file
```

---

## 📊 Charts Implemented

| # | Chart Type | Insight Shown |
|---|-----------|---------------|
| 1 | **Pie Chart** | Remote / Hybrid / In-Person distribution |
| 2 | **Histogram** | Salary distribution with median/mean |
| 3 | **Line Chart** | Cumulative experience distribution |
| 4 | **Bar Chart** | Top 15 programming languages |
| 5 | **Scatter Plot** | Experience vs Salary by work style |
| 6 | **Box Plot** | Salary spread by age group |
| 7 | **Heatmap** | Feature correlation matrix |
| 8 | **Area Chart** | Developer type composition by age |
| 9 | **Count Plot** | AI adoption by employment type |
| 10 | **Violin Plot** | Salary distribution by work style |
| ★ | **Bubble Chart** | Top countries: respondents × median salary (BONUS) |

Each chart has a clear **title**, labeled **axes**, **legend** where applicable, and a consistent **dark GitHub-style colour scheme**.

---

## 🔧 Filters (All 10 charts update simultaneously)

| Filter | Type | Column Filtered |
|--------|------|----------------|
| Age Group | Multi-select | `Age` |
| Work Style | Multi-select | `RemoteWork` |
| Education Level | Multi-select | `EdLevel_Short` |
| Developer Type | Multi-select | `DevType_Primary` |
| Salary Range | Slider | `ConvertedCompYearly` |
| Experience (Years) | Slider | `YearsCodePro` |
| AI Adoption | Dropdown | `AISelect` |
| Search | Text input | `Country` / `DevType_Primary` |
| Reset | Button | Clears all filters |

---

## 💡 Key Insights

1. **AI adoption is widespread:** ~70% of developers already use or plan to use AI tools, reflecting a major 2023 trend.
2. **Remote work dominates:** Over 53% of respondents work remotely or hybrid — a lasting post-COVID shift.
3. **JavaScript still #1:** JS leads with 62% of respondents using it, followed by HTML/CSS and Python.
4. **Experience ↑ Salary:** There is a clear positive correlation between years of professional experience and annual compensation.
5. **Peak earning age 35–44:** This group shows the highest median salary ($90K+), followed by 45–54.
6. **Full-stack is the most common role:** ~29% of respondents identify as full-stack developers.
7. **US dominates globally** but India has the largest respondent count; US respondents earn ~3× the global median.

---

## ⚙️ Technical Stack

| Tool | Role |
|------|------|
| Python 3.x | Core language |
| Pandas | Data loading, cleaning, filtering, aggregation |
| NumPy | Numerical operations |
| Matplotlib | Core plotting and chart creation |
| Seaborn | Statistical visualisations (heatmap) |
| Streamlit | Interactive frontend dashboard |

---

## ⚠️ Important Notes

- The dataset file **must remain named `survey_results_public.csv`** in the `data/` folder.
- All filters are **linked** — every chart updates when any filter changes.
- First load takes ~5–10 seconds due to the 89K row dataset; subsequent interactions are instant (Streamlit cache).
- Salary filter caps at $400K to remove extreme outliers for cleaner visualisations.
