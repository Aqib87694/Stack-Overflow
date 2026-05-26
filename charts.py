"""
charts.py  —  All 10 required charts + 1 bonus bubble chart
Stack Overflow Developer Survey 2023 Dashboard
Colour scheme matches the "DevPulse" dark UI theme.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns

# ── LIGHT THEME COLOUR PALETTE ────────────────────────────────────────────────
BG       = "#F8FAFC"       # deepest background (app background)
SURF     = "#FFFFFF"       # chart background (white cards)
SURF2    = "#F1F5F9"       # slightly darker surface (slate 100)
BORDER   = "#E2E8F0"       # border / grid lines
TEXT     = "#0F172A"       # main text (slate 900)
MUTED    = "#64748B"       # muted / axis labels (slate 500)
NEON     = "#3B82F6"       # primary blue accent
PURPLE   = "#8B5CF6"       # violet accent
FIRE     = "#EF4444"       # red/coral (highlight)
AMBER    = "#F59E0B"       # warm amber
GOLD     = "#EAB308"       # gold/yellow
SKY      = "#0EA5E9"       # sky blue
LIME     = "#84CC16"       # lime green

PALETTE = [NEON, PURPLE, FIRE, AMBER, GOLD, SKY, LIME,
           "#FF6EB4", "#40E0D0", "#C084FC"]


def _base(w=10, h=5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURF)
    return fig, ax


def _style(fig, ax=None, axes=None):
    targets = [ax] if ax is not None else (list(axes) if axes else [])
    for a in targets:
        a.set_facecolor(SURF)
        a.tick_params(colors=MUTED, labelsize=9)
        a.xaxis.label.set_color(TEXT)
        a.yaxis.label.set_color(TEXT)
        a.title.set_color(NEON)
        a.title.set_fontsize(12)
        a.title.set_fontweight("bold")
        for spine in a.spines.values():
            spine.set_edgecolor(BORDER)
        a.set_axisbelow(True)
        a.grid(color=BORDER, linewidth=0.5, alpha=0.7, linestyle="--")
    fig.tight_layout(pad=2.5)
    return fig


def _fmt_k(v, _=None):
    if v >= 1e6:  return f"${v/1e6:.1f}M"
    if v >= 1e3:  return f"${v/1e3:.0f}K"
    return f"${v:.0f}"


# ── 1. PIE CHART — Remote Work Distribution ──────────────────────────────────
# WHY: Shows proportional split of work styles (Remote/Hybrid/In-person).
# A pie chart is ideal here because the 3 categories sum to 100%
# and proportional comparison is the primary goal.

def pie_remote_work(df: pd.DataFrame) -> plt.Figure:
    counts = df["RemoteWork"].value_counts()
    counts = counts[counts.index != "Not specified"]
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    explode = [0.04] * len(counts)
    wedges, texts, autos = ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=[NEON, PURPLE, FIRE][:len(counts)],
        startangle=140,
        explode=explode,
        wedgeprops=dict(edgecolor=BG, linewidth=3, antialiased=True),
        textprops=dict(color=TEXT, fontsize=9.5),
        pctdistance=0.75,
    )
    for at in autos:
        at.set_color(BG)
        at.set_fontweight("bold")
        at.set_fontsize(8.5)
    ax.set_title("Remote Work Distribution", color=NEON, fontsize=12,
                 fontweight="bold", pad=14)
    # Add count annotations
    total = counts.sum()
    for wedge, count in zip(wedges, counts.values):
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = 1.25 * np.cos(np.deg2rad(angle))
        y = 1.25 * np.sin(np.deg2rad(angle))
        ax.text(x, y, f"n={count:,}", ha="center", va="center",
                color=MUTED, fontsize=7.5)
    return _style(fig)


# ── 2. HISTOGRAM — Salary Distribution ───────────────────────────────────────
# WHY: Reveals the shape, skewness, and spread of developer salaries.
# Histogram shows the full frequency distribution — not just averages —
# exposing the long right tail typical of tech compensation.

def histogram_salary(df: pd.DataFrame) -> plt.Figure:
    sal = df["ConvertedCompYearly"].dropna()
    sal = sal[sal <= 400_000]
    fig, ax = _base(10, 5)
    n, bins, patches = ax.hist(sal, bins=65, edgecolor=BG, linewidth=0.3)
    # Colour bars by range
    for patch, left in zip(patches, bins[:-1]):
        if left < 50_000:   c = PURPLE
        elif left < 120_000: c = NEON
        elif left < 200_000: c = AMBER
        else:                c = FIRE
        patch.set_facecolor(c)
        patch.set_alpha(0.82)
    med   = sal.median()
    mean_ = sal.mean()
    ax.axvline(med,   color=NEON,  linewidth=2,   linestyle="--",
               label=f"Median  ${med:,.0f}", zorder=5)
    ax.axvline(mean_, color=FIRE, linewidth=1.8, linestyle=":",
               label=f"Mean     ${mean_:,.0f}", zorder=5)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_k))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{int(v):,}"))
    ax.set_xlabel("Annual Salary (USD)")
    ax.set_ylabel("Number of Respondents")
    ax.set_title("Developer Salary Distribution (USD)")
    legend = ax.legend(facecolor=SURF2, labelcolor=TEXT, fontsize=9,
                       edgecolor=BORDER, framealpha=0.9)
    # Colour legend: salary zones
    zone_patches = [
        mpatches.Patch(color=PURPLE, label="<$50K",     alpha=0.82),
        mpatches.Patch(color=NEON,   label="$50K–$120K", alpha=0.82),
        mpatches.Patch(color=AMBER,  label="$120K–$200K",alpha=0.82),
        mpatches.Patch(color=FIRE,   label=">$200K",     alpha=0.82),
    ]
    ax.legend(handles=zone_patches + [
        plt.Line2D([0],[0], color=NEON,  linewidth=2, linestyle="--", label=f"Median ${med:,.0f}"),
        plt.Line2D([0],[0], color=FIRE, linewidth=1.8,linestyle=":", label=f"Mean  ${mean_:,.0f}"),
    ], facecolor=SURF2, labelcolor=TEXT, fontsize=8, edgecolor=BORDER)
    return _style(fig, ax)


# ── 3. LINE CHART — Cumulative Experience ────────────────────────────────────
# WHY: Shows how experience is distributed across the respondent pool.
# Cumulative line reveals what % of developers have ≤N years experience —
# essential for understanding seniority composition in the dataset.

def line_exp_cumulative(df: pd.DataFrame) -> plt.Figure:
    exp = df["YearsCodePro"].dropna().sort_values()
    x      = np.arange(0, 41)
    counts = [(exp <= yr).sum() for yr in x]
    pcts   = [c / len(exp) * 100 for c in counts]
    fig, ax = _base(9, 5)
    ax.plot(x, pcts, color=NEON, linewidth=2.5, zorder=3)
    ax.fill_between(x, pcts, alpha=0.12, color=NEON)
    # Reference lines at 25/50/75%
    for pct, label in [(25,"25%"),(50,"50%"),(75,"75%")]:
        yrs = next((xi for xi, p in zip(x, pcts) if p >= pct), None)
        if yrs is not None:
            ax.axhline(pct,  color=BORDER, linewidth=0.8, linestyle="--")
            ax.axvline(yrs,  color=PURPLE, linewidth=1,   linestyle=":", alpha=0.7)
            ax.text(yrs + 0.3, pct + 1.5, f"{yrs}yr", color=PURPLE,
                    fontsize=7.5, va="bottom")
    ax.set_xlabel("Years of Professional Coding Experience")
    ax.set_ylabel("Cumulative % of Respondents")
    ax.set_title("Cumulative Distribution of Professional Experience")
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 102)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    return _style(fig, ax)


# ── 4. BAR CHART — Top Languages ─────────────────────────────────────────────
# WHY: Horizontal bar is the clearest chart for comparing ranked categories
# with long labels. Shows which languages dominate developer workflows.

def bar_top_languages(df: pd.DataFrame, top_n: int = 15) -> plt.Figure:
    lang = (
        df["LanguageHaveWorkedWith"].dropna()
        .str.split(";").explode().str.strip()
        .value_counts().head(top_n).sort_values()
    )
    total = df["LanguageHaveWorkedWith"].notna().sum()
    fig, ax = _base(9, 6)
    colors = [NEON if i == len(lang)-1 else PALETTE[i % len(PALETTE)]
              for i in range(len(lang))]
    bars = ax.barh(lang.index, lang.values, color=colors,
                  edgecolor=BG, height=0.72, linewidth=0.5)
    for bar, val in zip(bars, lang.values):
        pct = val / total * 100
        ax.text(val + 200, bar.get_y() + bar.get_height()/2,
                f"{val:,}  ({pct:.1f}%)",
                va="center", ha="left", color=TEXT, fontsize=7.8)
    ax.set_xlabel("Respondents Using Language")
    ax.set_title(f"Top {top_n} Programming Languages")
    ax.set_xlim(0, lang.max() * 1.18)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{v/1000:.0f}K"))
    return _style(fig, ax)


# ── 5. SCATTER PLOT — Experience vs Salary ───────────────────────────────────
# WHY: Reveals the relationship between two key numeric variables.
# Colouring by work style adds a third dimension, showing whether
# remote/hybrid workers earn more at the same experience level.

def scatter_exp_salary(df: pd.DataFrame) -> plt.Figure:
    sub = df[["YearsCodePro","ConvertedCompYearly","RemoteWork"]].dropna()
    sub = sub[sub["ConvertedCompYearly"] <= 400_000]
    sub = sub.sample(min(4000, len(sub)), random_state=42)
    fig, ax = _base(10, 5)
    remote_map = {"Remote": NEON, "Hybrid (some remote, some in-person)": PURPLE,
                  "In-person": FIRE}
    for rtype, color in remote_map.items():
        grp = sub[sub["RemoteWork"] == rtype]
        if len(grp):
            ax.scatter(grp["YearsCodePro"], grp["ConvertedCompYearly"],
                       color=color, alpha=0.35, s=10, label=rtype, linewidths=0)
    # Trend line
    z = np.polyfit(sub["YearsCodePro"], sub["ConvertedCompYearly"], 1)
    xs = np.linspace(0, 40, 100)
    ax.plot(xs, np.poly1d(z)(xs), color=GOLD, linewidth=2.2,
            linestyle="--", label="Overall trend", zorder=4)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_k))
    ax.set_xlabel("Years of Professional Experience")
    ax.set_ylabel("Annual Salary (USD)")
    ax.set_title("Experience vs Salary — coloured by Work Style")
    ax.legend(facecolor=SURF2, labelcolor=TEXT, fontsize=8.5,
              edgecolor=BORDER, markerscale=2.5)
    return _style(fig, ax)


# ── 6. BOX PLOT — Salary by Age Group ────────────────────────────────────────
# WHY: Box plot shows median, IQR, and outliers simultaneously —
# far richer than a bar chart of averages. Here it reveals how earning
# power peaks and spreads differently across age cohorts.

def box_salary_by_age(df: pd.DataFrame) -> plt.Figure:
    age_order = ["Under 18 years old","18-24 years old","25-34 years old",
                 "35-44 years old","45-54 years old","55-64 years old","65 years or older"]
    sub = df[["Age","ConvertedCompYearly"]].dropna()
    sub = sub[sub["ConvertedCompYearly"] <= 400_000]
    pairs = [(a, l) for a, l in zip(age_order, ["<18","18-24","25-34","35-44","45-54","55-64","65+"])
             if len(sub[sub["Age"]==a]) >= 2]
    if not pairs:
        fig, ax = _base(10, 5)
        ax.text(0.5, 0.5, "Not enough data for this filter combination",
                ha="center", va="center", color=MUTED, fontsize=11, transform=ax.transAxes)
        ax.set_title("Salary Distribution by Age Group")
        return _style(fig, ax)
    age_order_f, labels = zip(*pairs)
    groups = [sub[sub["Age"]==a]["ConvertedCompYearly"].values for a in age_order_f]
    fig, ax = _base(10, 5)
    bp = ax.boxplot(
        groups, labels=labels, patch_artist=True, notch=False,
        medianprops=dict(color=GOLD, linewidth=2.5),
        flierprops=dict(marker="o", color=FIRE, alpha=0.25, markersize=2.5),
        whiskerprops=dict(color=MUTED, linewidth=1.2),
        capprops=dict(color=MUTED, linewidth=1.2),
        boxprops=dict(linewidth=1.2),
    )
    for i, patch in enumerate(bp["boxes"]):
        patch.set_facecolor(PALETTE[i % len(PALETTE)])
        patch.set_alpha(0.65)
        patch.set_edgecolor(BORDER)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_k))
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Annual Salary (USD)")
    ax.set_title("Salary Distribution by Age Group")
    return _style(fig, ax)


# ── 7. HEATMAP — Correlation Matrix ─────────────────────────────────────────
# WHY: Correlation heatmap shows pairwise relationships across all numeric
# features in one glance. Identifies which variables are linked —
# e.g. does salary correlate with experience? Does AI use correlate with exp?

def heatmap_correlation(df: pd.DataFrame) -> plt.Figure:
    cols = {
        "YearsCode": "Yrs Coding", "YearsCodePro": "Yrs Pro",
        "WorkExp": "Work Exp", "ConvertedCompYearly": "Salary",
    }
    sub = df[[c for c in cols if c in df.columns]].rename(columns=cols).copy()
    sub["AI User"]  = (df["AISelect"] == "Yes").astype(int)
    sub["Is Remote"] = (df["RemoteWork"] == "Remote").astype(int)
    corr = sub.dropna().corr()
    fig, ax = _base(7.5, 6)
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    cmap = sns.diverging_palette(260, 10, s=85, l=45, as_cmap=True)
    sns.heatmap(
        corr, ax=ax, mask=mask,
        annot=True, fmt=".2f", cmap=cmap,
        linewidths=1, linecolor=BG,
        annot_kws={"size": 9, "weight": "bold", "color": TEXT},
        vmin=-1, vmax=1,
        cbar_kws={"shrink": 0.75},
    )
    ax.set_title("Feature Correlation Matrix")
    ax.tick_params(axis="x", rotation=40, labelsize=9, colors=TEXT)
    ax.tick_params(axis="y", rotation=0,  labelsize=9, colors=TEXT)
    # Style the colorbar
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color=TEXT, labelsize=8)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT)
    return _style(fig, ax)


# ── 8. AREA CHART — Developer Type by Age ────────────────────────────────────
# WHY: Stacked area shows both individual composition and cumulative total
# across groups. Here it reveals how developer roles shift across age cohorts —
# more students at 18–24, more seniors at 35–44 etc.

def area_devtype_by_age(df: pd.DataFrame) -> plt.Figure:
    top_dt = df["DevType_Primary"].value_counts().head(6).index.tolist()
    age_order = ["18-24 years old","25-34 years old","35-44 years old",
                 "45-54 years old","55-64 years old"]
    short = {
        "Developer, full-stack": "Full-Stack", "Developer, back-end": "Back-End",
        "Developer, front-end": "Front-End",
        "Developer, desktop or enterprise applications": "Desktop/Ent.",
        "Other (please specify):": "Other", "Developer, mobile": "Mobile",
        "Student": "Student",
    }
    label_map = {
        "18-24 years old":"18-24","25-34 years old":"25-34","35-44 years old":"35-44",
        "45-54 years old":"45-54","55-64 years old":"55-64",
    }
    fig, ax = _base(10, 5)
    present_ages = [a for a in age_order if a in df["Age"].values]
    sub = df[df["Age"].isin(present_ages) & df["DevType_Primary"].isin(top_dt)]
    if sub.empty or len(present_ages) < 2 or not top_dt:
        ax.text(0.5, 0.5, "Not enough data for this filter combination",
                ha="center", va="center", color=MUTED, fontsize=11, transform=ax.transAxes)
        ax.set_title("Developer Type Composition by Age Group")
        return _style(fig, ax)
    pivot = sub.groupby(["Age","DevType_Primary"]).size().unstack(fill_value=0)
    pivot = pivot.reindex(present_ages, fill_value=0)
    pivot = pivot[[c for c in top_dt if c in pivot.columns]]
    pivot = pivot.loc[:, (pivot != 0).any(axis=0)].astype(float)
    if pivot.empty:
        ax.text(0.5, 0.5, "Not enough data for this filter combination",
                ha="center", va="center", color=MUTED, fontsize=11, transform=ax.transAxes)
        ax.set_title("Developer Type Composition by Age Group")
        return _style(fig, ax)
    pivot.columns = [short.get(c, c[:18]) for c in pivot.columns]
    pivot.index   = [label_map.get(i, i) for i in pivot.index]
    pivot.plot.area(ax=ax, color=PALETTE[:len(pivot.columns)], alpha=0.78, linewidth=0)
    ax.set_xlabel("Age Group"); ax.set_ylabel("Respondents")
    ax.set_title("Developer Type Composition by Age Group")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{int(v):,}"))
    ax.tick_params(axis="x", rotation=0)
    ax.legend(facecolor=SURF2, labelcolor=TEXT, fontsize=8, edgecolor=BORDER,
              loc="upper right", framealpha=0.9)
    return _style(fig, ax)


# ── 9. COUNT PLOT — AI Adoption by Employment ────────────────────────────────
# WHY: Count plot (grouped bar) shows frequency of categories.
# Grouping by employment type reveals whether freelancers, full-timers,
# or students differ in their AI tool adoption patterns.

def count_ai_adoption(df: pd.DataFrame) -> plt.Figure:
    ai_map = {
        "Yes": "Using AI Now",
        "No, but I plan to soon": "Plan to Soon",
        "No, and I don't plan to": "Not Planning",
    }
    emp_map = {
        "Employed, full-time": "Full-Time",
        "Employed, part-time": "Part-Time",
        "Independent contractor, freelancer, or self-employed": "Freelancer",
        "Student": "Student",
        "Not employed, but looking for work": "Job Seeking",
    }
    sub = df[df["AISelect"].isin(ai_map)].copy()
    sub["AI_Label"] = sub["AISelect"].map(ai_map)
    sub["Emp"]      = sub["Employment_Primary"].map(emp_map).fillna("Other")
    top_emp = sub["Emp"].value_counts().head(5).index
    sub = sub[sub["Emp"].isin(top_emp)]
    pivot = sub.groupby(["Emp","AI_Label"]).size().unstack(fill_value=0)
    ai_cols = ["Using AI Now","Plan to Soon","Not Planning"]
    pivot = pivot.reindex(columns=[a for a in ai_cols if a in pivot.columns])
    fig, ax = _base(10, 5)
    x = np.arange(len(pivot))
    w = 0.26
    colors = [NEON, AMBER, FIRE]
    for i, col in enumerate(pivot.columns):
        bars = ax.bar(x + (i - 1) * w, pivot[col].values,
                      width=w, color=colors[i], edgecolor=BG, label=col, alpha=0.88)
        for bar in bars:
            h = bar.get_height()
            if h > 50:
                ax.text(bar.get_x() + bar.get_width()/2, h + 30,
                        f"{int(h):,}", ha="center", va="bottom",
                        color=TEXT, fontsize=7.2)
    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index, rotation=12, ha="right")
    ax.set_ylabel("Respondents")
    ax.set_title("AI Tool Adoption by Employment Type")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{int(v):,}"))
    ax.legend(facecolor=SURF2, labelcolor=TEXT, fontsize=9, edgecolor=BORDER)
    return _style(fig, ax)


# ── 10. VIOLIN PLOT — Salary by Work Style ───────────────────────────────────
# WHY: Violin plot shows full probability density, not just spread like a box.
# It reveals whether remote salaries are uniformly distributed or cluster
# around specific points — insight that box plots hide.

def violin_salary_remote(df: pd.DataFrame) -> plt.Figure:
    remote_types = ["Remote","Hybrid (some remote, some in-person)","In-person"]
    labels       = ["Remote","Hybrid","In-Person"]
    sub = df[df["RemoteWork"].isin(remote_types)][["RemoteWork","ConvertedCompYearly"]].dropna()
    sub = sub[sub["ConvertedCompYearly"] <= 300_000]
    data = [sub[sub["RemoteWork"]==r]["ConvertedCompYearly"].values for r in remote_types]
    # Remove empty groups so violinplot doesn't crash
    positions = [i+1 for i, d in enumerate(data) if len(d) >= 2]
    data      = [d for d in data if len(d) >= 2]
    labels_present = [l for l, d_all in zip(labels, [sub[sub["RemoteWork"]==r]["ConvertedCompYearly"].values for r in remote_types]) if len(d_all) >= 2]
    fig, ax = _base(8, 5)
    if not data:
        ax.text(0.5, 0.5, "Not enough data for this filter combination",
                ha="center", va="center", color=MUTED, fontsize=11, transform=ax.transAxes)
        ax.set_title("Salary Distribution by Work Style")
        return _style(fig, ax)
    parts = ax.violinplot(data, positions=positions, showmedians=True,
                         showextrema=True, widths=0.7)
    colors = [NEON, PURPLE, FIRE]
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colors[i])
        pc.set_edgecolor(BG)
        pc.set_alpha(0.72)
    for key in ("cmedians", "cmins", "cmaxes", "cbars"):
        parts[key].set_color(GOLD)
        parts[key].set_linewidth(2)
    ax.set_xticks(positions)
    ax.set_xticklabels(labels_present)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_k))
    ax.set_xlabel("Work Style")
    ax.set_ylabel("Annual Salary (USD)")
    ax.set_title("Salary Distribution by Work Style")
    return _style(fig, ax)


# ── BONUS BUBBLE — Countries ──────────────────────────────────────────────────
# WHY: Bubble chart encodes 3 dimensions: X=country rank, Y=median salary,
# size=respondent count. This reveals geographic salary disparities
# while also showing where most survey participants are from.

def bubble_countries(df: pd.DataFrame, top_n: int = 15) -> plt.Figure:
    sub = df[["Country","ConvertedCompYearly"]].copy()
    sub = sub[sub["ConvertedCompYearly"] <= 400_000]
    top_c = df["Country"].value_counts().head(top_n).index
    grp = (
        sub[sub["Country"].isin(top_c)]
        .groupby("Country")
        .agg(count=("ConvertedCompYearly","size"),
             med_sal=("ConvertedCompYearly","median"))
        .reset_index()
        .sort_values("count", ascending=False)
    )
    fig, ax = _base(12, 6)
    sizes = (grp["count"] / grp["count"].max()) * 2800 + 100
    sc = ax.scatter(
        range(len(grp)), grp["med_sal"],
        s=sizes, c=grp["med_sal"],
        cmap="plasma", alpha=0.88,
        edgecolors=BORDER, linewidth=1.2, zorder=3,
    )
    cbar = fig.colorbar(sc, ax=ax, shrink=0.75)
    cbar.set_label("Median Salary (USD)", color=TEXT, fontsize=9)
    cbar.ax.yaxis.set_tick_params(color=TEXT, labelsize=8)
    cbar.ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_k))
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT)
    for i, row in grp.reset_index().iterrows():
        short = row["Country"].replace(" of America","").replace("United Kingdom","UK")
        ax.text(i, row["med_sal"] * 1.06, short,
                ha="center", va="bottom", color=TEXT, fontsize=7.2, rotation=22)
    ax.set_xticks([])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_k))
    ax.set_ylabel("Median Annual Salary (USD)")
    ax.set_title(f"Top {top_n} Countries — Respondent Count vs Median Salary\n"
                 "(bubble size = number of respondents)")
    return _style(fig, ax)
