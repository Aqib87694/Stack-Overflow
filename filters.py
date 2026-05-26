"""
filters.py
----------
Data loading, cleaning, and filtering for the Stack Overflow Developer Survey 2023 Dashboard.
All logic centralised here — app.py stays lean.
"""

import pandas as pd
import numpy as np

DATASET_PATH = "data/survey_results_public.csv"

# ── 1. LOAD & CLEAN ──────────────────────────────────────────────────────────

def load_and_clean(filepath: str = DATASET_PATH) -> pd.DataFrame:
    """
    Load survey_results_public.csv, clean and engineer features.
    Returns cleaned DataFrame or None if file missing.
    """
    try:
        df = pd.read_csv(filepath, low_memory=False)
    except FileNotFoundError:
        return None

    # ── Drop irrelevant / mostly-null columns ────────────────────────────────
    drop_cols = [
        "Q120", "TechList", "PurchaseInfluence", "BuyNewTool",
        "Currency", "CompTotal",        # use ConvertedCompYearly instead
        "TBranch", "ICorPM",
        "Knowledge_1","Knowledge_2","Knowledge_3","Knowledge_4",
        "Knowledge_5","Knowledge_6","Knowledge_7","Knowledge_8",
        "Frequency_1","Frequency_2","Frequency_3",
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # ── Numeric coercion ─────────────────────────────────────────────────────
    df["YearsCode"] = pd.to_numeric(df["YearsCode"], errors="coerce")
    df["YearsCodePro"] = pd.to_numeric(df["YearsCodePro"], errors="coerce")
    df["WorkExp"] = pd.to_numeric(df["WorkExp"], errors="coerce")
    df["ConvertedCompYearly"] = pd.to_numeric(df["ConvertedCompYearly"], errors="coerce")

    # ── Remove extreme salary outliers (keep < $600K) ────────────────────────
    df.loc[df["ConvertedCompYearly"] > 600_000, "ConvertedCompYearly"] = np.nan

    # ── Clean Age ─────────────────────────────────────────────────────────────
    df["Age"] = df["Age"].fillna("Unknown")

    # ── Clean Employment (take first value for multi-select) ─────────────────
    df["Employment_Primary"] = df["Employment"].str.split(";").str[0].fillna("Unknown")

    # ── Simplify EdLevel ─────────────────────────────────────────────────────
    ed_map = {
        "Bachelor's degree (B.A., B.S., B.Eng., etc.)": "Bachelor's",
        "Master's degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's",
        "Some college/university study without earning a degree": "Some College",
        "Associate degree (A.A., A.S., etc.)": "Associate",
        "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "High School",
        "Professional degree (JD, MD, Ph.D, Ed.D, etc.)": "PhD/Prof.",
        "Primary/elementary school": "Primary School",
        "Something else": "Other",
    }
    df["EdLevel_Short"] = df["EdLevel"].map(ed_map).fillna(df["EdLevel"].fillna("Unknown"))

    # ── Primary DevType ───────────────────────────────────────────────────────
    df["DevType_Primary"] = df["DevType"].str.split(";").str[0].fillna("Unknown")

    # ── RemoteWork ────────────────────────────────────────────────────────────
    df["RemoteWork"] = df["RemoteWork"].fillna("Not specified")

    # ── AI Sentiment short ────────────────────────────────────────────────────
    df["AISent"] = df["AISent"].fillna("No response")

    # ── Salary band ──────────────────────────────────────────────────────────
    def salary_band(s):
        if pd.isna(s):      return "Unknown"
        if s < 30_000:      return "<$30K"
        elif s < 60_000:    return "$30K–$60K"
        elif s < 100_000:   return "$60K–$100K"
        elif s < 150_000:   return "$100K–$150K"
        elif s < 250_000:   return "$150K–$250K"
        else:               return "$250K+"
    df["SalaryBand"] = df["ConvertedCompYearly"].apply(salary_band)

    # ── Experience bucket ─────────────────────────────────────────────────────
    def exp_bucket(y):
        if pd.isna(y):  return "Unknown"
        if y < 2:       return "0–1 yrs"
        elif y < 5:     return "2–4 yrs"
        elif y < 10:    return "5–9 yrs"
        elif y < 20:    return "10–19 yrs"
        else:           return "20+ yrs"
    df["ExpBucket"] = df["YearsCodePro"].apply(exp_bucket)

    return df.reset_index(drop=True)


# ── 2. APPLY FILTERS ─────────────────────────────────────────────────────────

def apply_filters(
    df: pd.DataFrame,
    selected_age: list = None,
    selected_remote: list = None,
    selected_ed: list = None,
    selected_devtype: list = None,
    selected_country: list = None,
    salary_range: tuple = None,
    years_range: tuple = None,
    ai_select: str = "All",
    search_text: str = "",
) -> pd.DataFrame:
    """Apply all sidebar filters; all charts update from this result."""
    f = df.copy()

    if selected_age:
        f = f[f["Age"].isin(selected_age)]

    if selected_remote:
        f = f[f["RemoteWork"].isin(selected_remote)]

    if selected_ed:
        f = f[f["EdLevel_Short"].isin(selected_ed)]

    if selected_devtype:
        f = f[f["DevType_Primary"].isin(selected_devtype)]

    if selected_country:
        f = f[f["Country"].isin(selected_country)]

    if salary_range:
        lo, hi = salary_range
        mask = (
            f["ConvertedCompYearly"].isna() |
            ((f["ConvertedCompYearly"] >= lo) & (f["ConvertedCompYearly"] <= hi))
        )
        f = f[mask]

    if years_range:
        lo, hi = years_range
        mask = (
            f["YearsCodePro"].isna() |
            ((f["YearsCodePro"] >= lo) & (f["YearsCodePro"] <= hi))
        )
        f = f[mask]

    if ai_select != "All":
        f = f[f["AISelect"] == ai_select]

    if search_text.strip():
        term = search_text.strip().lower()
        f = f[f["Country"].str.lower().str.contains(term, na=False) |
              f["DevType_Primary"].str.lower().str.contains(term, na=False)]

    return f.reset_index(drop=True)


# ── 3. KPIs ───────────────────────────────────────────────────────────────────

def compute_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    sal = df["ConvertedCompYearly"].dropna()
    ai_yes = (df["AISelect"] == "Yes").sum()
    total = len(df)
    return {
        "total_respondents":  total,
        "countries":          df["Country"].nunique(),
        "median_salary":      sal.median() if len(sal) else 0,
        "avg_salary":         sal.mean()   if len(sal) else 0,
        "ai_adoption_pct":    ai_yes / total * 100 if total else 0,
        "median_exp":         df["YearsCodePro"].median(),
        "remote_pct":         (df["RemoteWork"] == "Remote").sum() / total * 100 if total else 0,
        "fullstack_pct":      df["DevType_Primary"].str.contains("full-stack", case=False, na=False).sum() / total * 100 if total else 0,
        "with_salary":        len(sal),
        "top_language":       (
                                  df["LanguageHaveWorkedWith"]
                                  .str.split(";").explode()
                                  .value_counts().index[0]
                                  if df["LanguageHaveWorkedWith"].notna().any() else "N/A"
                              ),
    }
