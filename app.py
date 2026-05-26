"""
app.py  —  Stack Overflow Developer Survey 2023 Dashboard
Course: Exploratory Data Analysis | Instructor: Ali Hassan Sherazi | 05-June-2026
Run:  python -m streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from filters import load_and_clean, apply_filters, compute_kpis
from charts import (
    pie_remote_work, histogram_salary, line_exp_cumulative,
    bar_top_languages, scatter_exp_salary, box_salary_by_age,
    heatmap_correlation, area_devtype_by_age, count_ai_adoption,
    violin_salary_remote, bubble_countries,
)

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DevPulse · SO Survey 2023",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── FULL CUSTOM CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Clash+Display:wght@500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ═══════════════════════════════════════════════════
   GLOBAL BASE
═══════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #F8FAFC !important; /* Light background */
    color: #1E293B !important; /* Dark text */
    scroll-behavior: smooth;
}

/* App container background */
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(120deg, rgba(248, 250, 252, 1) 0%, rgba(241, 245, 249, 1) 100%) !important;
}

/* Main content padding */
[data-testid="stMain"] > div {
    padding: 1.5rem 2rem 2rem 2rem !important;
}

/* ═══════════════════════════════════════════════════
   SIDEBAR — Clean and light
═══════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
    box-shadow: 4px 0 15px rgba(0, 0, 0, 0.02) !important;
}
[data-testid="stSidebar"] * { color: #475569 !important; }

/* Sidebar top bar */
[data-testid="stSidebar"]::before {
    content: '';
    display: block;
    height: 4px;
    background: linear-gradient(90deg, #3B82F6, #8B5CF6, #EC4899);
    position: sticky;
    top: 0;
    z-index: 100;
}

/* Filter section labels */
.flabel {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #3B82F6 !important;
    padding: 16px 0 6px 0 !important;
    display: block !important;
}

/* Multiselect container */
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background: #FFFFFF !important;
    border: 2px solid #E2E8F0 !important;
    border-radius: 12px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    min-height: 46px !important;
    padding: 0 4px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child:hover,
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.12) !important;
    transform: translateY(-1px) !important;
}

/* Tags inside multiselect */
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
    border: 1px solid #BFDBFE !important;
    border-radius: 8px !important;
    color: #1D4ED8 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 4px 8px !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"]:hover {
    background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%) !important;
    transform: scale(1.02) !important;
}

/* Dropdown popover */
[data-baseweb="popover"] [data-baseweb="menu"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
    overflow: hidden !important;
}
li[role="option"] {
    background: transparent !important;
    color: #334155 !important;
    font-size: 0.85rem !important;
    padding: 10px 16px !important;
    transition: background 0.2s, color 0.2s !important;
    cursor: pointer !important;
}
li[role="option"]:hover { background: #F1F5F9 !important; color: #0F172A !important; }
li[aria-selected="true"] { background: rgba(59, 130, 246, 0.1) !important; color: #2563EB !important; font-weight: 600 !important; }

/* Selectbox (single) */
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 2px solid #E2E8F0 !important;
    border-radius: 12px !important;
    color: #1E293B !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    min-height: 46px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div:hover {
    border-color: #8B5CF6 !important;
    box-shadow: 0 6px 16px rgba(139, 92, 246, 0.12) !important;
    transform: translateY(-1px) !important;
}

/* Sliders */
[data-testid="stSlider"] > div > div > div { background: #E2E8F0 !important; border-radius: 6px !important; }
[data-testid="stSlider"] > div > div > div > div { background: linear-gradient(90deg, #3B82F6, #8B5CF6) !important; border-radius: 6px !important; }
[data-testid="stThumbValue"] { color: #3B82F6 !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 0.75rem !important; font-weight: 600 !important; }
[data-testid="stSlider"] [role="slider"] { background: #FFFFFF !important; border: 2px solid #3B82F6 !important; box-shadow: 0 2px 5px rgba(59, 130, 246, 0.3) !important; transition: transform 0.1s; }
[data-testid="stSlider"] [role="slider"]:hover { transform: scale(1.1); }

/* Text input */
[data-testid="stSidebar"] input[type="text"] {
    background: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    color: #1E293B !important;
    padding: 10px 14px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}
[data-testid="stSidebar"] input[type="text"]:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    background: #FFFFFF !important;
    outline: none !important;
}
[data-testid="stSidebar"] input::placeholder { color: #94A3B8 !important; }

/* ── RESET BUTTON — Smooth Gradient ── */
[data-testid="stSidebar"] [data-testid="stButton"] button {
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    padding: 12px 0 !important;
    width: 100% !important;
    cursor: pointer !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    transition: all 0.3s ease !important;
    margin-top: 12px !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
    background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%) !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2) !important;
}

/* ═══════════════════════════════════════════════════
   KPI METRIC CARDS
═══════════════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 20px 20px 18px !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-5px) !important;
    border-color: #3B82F6 !important;
    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.1) !important;
}
/* Accent left bar */
[data-testid="stMetric"]::before {
    content: '' !important;
    position: absolute !important;
    left: 0 !important; top: 0 !important;
    width: 4px !important; height: 100% !important;
    background: linear-gradient(180deg, #3B82F6 0%, #8B5CF6 100%) !important;
    border-radius: 12px 0 0 12px !important;
}
[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #0F172A !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
    line-height: 1.2 !important;
    margin-top: 4px !important;
}

/* ═══════════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════════ */
[data-testid="stTabs"] { border-bottom: 1px solid #E2E8F0 !important; }
[data-testid="stTabs"] button {
    color: #64748B !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 12px 24px !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all 0.2s ease !important;
    border: none !important;
    background: transparent !important;
}
[data-testid="stTabs"] button:hover { color: #3B82F6 !important; background: rgba(59, 130, 246, 0.05) !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #2563EB !important;
    font-weight: 600 !important;
    background: #FFFFFF !important;
    border-bottom: 3px solid #3B82F6 !important;
}

/* ═══════════════════════════════════════════════════
   CHART CONTAINERS
═══════════════════════════════════════════════════ */
.chart-wrap {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 24px 24px 16px 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
    transition: all 0.3s ease;
}
.chart-wrap:hover {
    border-color: #CBD5E1;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
}
.clabel {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8B5CF6;
    display: block;
    margin-bottom: 4px;
}
.ctitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #0F172A;
    margin: 0 0 16px 0;
    display: block;
}

/* ═══════════════════════════════════════════════════
   SECTION HEADERS
═══════════════════════════════════════════════════ */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3B82F6;
    border-left: 4px solid #3B82F6;
    padding-left: 12px;
    margin: 32px 0 20px 0;
    display: block;
}

/* ═══════════════════════════════════════════════════
   MISC
═══════════════════════════════════════════════════ */
hr { border: none !important; border-top: 1px solid #E2E8F0 !important; margin: 24px 0 !important; }

[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F1F5F9; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

/* Fade-up animation for columns */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(15px); }
    to   { opacity: 1; transform: translateY(0); }
}
[data-testid="column"] { animation: fadeUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both !important; }
[data-testid="column"]:nth-child(1) { animation-delay: 0.05s !important; }
[data-testid="column"]:nth-child(2) { animation-delay: 0.10s !important; }
[data-testid="column"]:nth-child(3) { animation-delay: 0.15s !important; }
[data-testid="column"]:nth-child(4) { animation-delay: 0.20s !important; }
[data-testid="column"]:nth-child(5) { animation-delay: 0.25s !important; }

[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left: 4px solid #3B82F6 !important;
    background: #EFF6FF !important;
    color: #1E3A8A !important;
}
[data-testid="stSidebar"] hr { border-top: 1px solid #E2E8F0 !important; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="⚡ Parsing 89,184 developer responses…")
def get_data():
    return load_and_clean("data/survey_results_public.csv")

df_full = get_data()
if df_full is None:
    st.error("❌  `data/survey_results_public.csv` not found.")
    st.stop()

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: clamp(20px, 4vw, 36px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.03);
            margin-bottom: 24px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;">
  
  <div style="font-family:'Space Grotesk',sans-serif; font-size:clamp(0.6rem, 2vw, 0.75rem);
              letter-spacing:0.15em; color:#3B82F6; text-transform:uppercase;
              margin-bottom:12px; font-weight: 600;
              background: rgba(59, 130, 246, 0.1);
              padding: 6px 16px; border-radius: 20px;
              border: 1px solid rgba(59, 130, 246, 0.2);">
    ◆ &nbsp; EDA PROJECT &nbsp;·&nbsp; CREATED BY AQIB MOEEN
  </div>
  
  <div style="font-family:'Inter',sans-serif; font-size:clamp(1.8rem, 5vw, 3rem);
              font-weight:800; color:#0F172A; letter-spacing:-1px; line-height:1.15;
              margin-bottom:16px; max-width: 800px;">
    Stack Overflow
    <span style="color:#3B82F6;">Developer</span>
    <span style="background:linear-gradient(90deg,#3B82F6,#8B5CF6);
                 -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
      Survey 2023 Dashboard
    </span>
  </div>
  
  <div style="font-family:'Inter',sans-serif; font-size:clamp(0.8rem, 2.5vw, 1rem);
              color:#64748B; max-width: 600px; line-height: 1.6;">
    Interactive exploration of <strong>89,184</strong> developer responses across <strong>185</strong> countries, analyzing global salaries, technology adoption, and remote work trends.
  </div>
  
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:8px 4px 16px 4px;">
      <div style="font-family:'Inter',sans-serif; font-weight:600;
                  font-size:1.1rem; color:#0F172A; letter-spacing:0.5px;">
        ⚡ &nbsp;FILTERS
      </div>
      <div style="font-family:'Space Grotesk',sans-serif; font-size:0.65rem;
                  color:#64748B; letter-spacing:0.1em; margin-top:3px; font-weight:500;">
        ALL CHARTS UPDATE LIVE
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # 1. Age
    st.markdown('<span class="flabel">👤  Age Group</span>', unsafe_allow_html=True)
    all_ages = ["Under 18 years old","18-24 years old","25-34 years old",
                "35-44 years old","45-54 years old","55-64 years old","65 years or older"]
    sel_age = st.multiselect("Age", options=all_ages, default=[], placeholder="Select age groups...", label_visibility="collapsed")

    # 2. Work Style
    st.markdown('<span class="flabel">🏠  Work Style</span>', unsafe_allow_html=True)
    all_remote = ["Remote","Hybrid (some remote, some in-person)","In-person","Not specified"]
    sel_remote = st.multiselect("Remote", options=all_remote, default=[], placeholder="Select work style...", label_visibility="collapsed")

    # 3. Education
    st.markdown('<span class="flabel">🎓  Education Level</span>', unsafe_allow_html=True)
    all_ed = sorted(df_full["EdLevel_Short"].dropna().unique().tolist())
    sel_ed = st.multiselect("Education", options=all_ed, default=[], placeholder="Select education level...", label_visibility="collapsed")

    # 4. Developer Type
    st.markdown('<span class="flabel">💻  Developer Type</span>', unsafe_allow_html=True)
    top_devtypes = df_full["DevType_Primary"].value_counts().head(12).index.tolist()
    sel_devtype = st.multiselect("DevType", options=top_devtypes, default=[], placeholder="Select developer roles...", label_visibility="collapsed")

    # 5. Salary Range
    st.markdown('<span class="flabel">💰  Salary Range (USD)</span>', unsafe_allow_html=True)
    sal_range = st.slider("Salary", min_value=0, max_value=400_000,
                          value=(0, 400_000), step=5000, format="$%d", label_visibility="collapsed")

    # 6. Experience
    st.markdown('<span class="flabel">📅  Experience (Years Pro)</span>', unsafe_allow_html=True)
    exp_range = st.slider("Exp", min_value=0, max_value=40, value=(0, 40), label_visibility="collapsed")

    # 7. AI Adoption
    st.markdown('<span class="flabel">🤖  AI Adoption</span>', unsafe_allow_html=True)
    sel_ai = st.selectbox("AI", options=["All","Yes","No, but I plan to soon","No, and I don't plan to"],
                          label_visibility="collapsed")

    # 8. Search
    st.markdown('<span class="flabel">🔍  Search Country / Role</span>', unsafe_allow_html=True)
    search_text = st.text_input("Search", placeholder="e.g. India, mobile…", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺  RESET ALL FILTERS", use_container_width=True):
        st.rerun()

    st.markdown("""
    <div style="margin-top:20px; padding:12px; background:#F8FAFC;
                border:1px solid #CBD5E1; border-radius:10px; text-align:center;">
      <span style="font-family:'Space Grotesk',sans-serif; font-size:0.65rem; font-weight: 500;
                   color:#64748B; line-height:1.9; letter-spacing:0.05em;">
        DATA SOURCE<br>
        <span style="color:#3B82F6; font-size:0.75rem; font-weight: 600;">survey_results_public.csv</span><br>
        Stack Overflow · May 2023 · ODbL
      </span>
    </div>
    """, unsafe_allow_html=True)

# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
df = apply_filters(
    df_full,
    selected_age=sel_age or all_ages,
    selected_remote=sel_remote or all_remote,
    selected_ed=sel_ed or all_ed,
    selected_devtype=sel_devtype or top_devtypes,
    salary_range=sal_range,
    years_range=exp_range,
    ai_select=sel_ai,
    search_text=search_text,
)

if df.empty:
    st.warning("⚠️  No data matches the current filters. Please adjust the sidebar.")
    st.stop()

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
kpis = compute_kpis(df)

st.markdown('<span class="section-header">◆  Key Metrics</span>', unsafe_allow_html=True)

r1 = st.columns(5)
r1[0].metric("👥 Respondents",   f"{kpis['total_respondents']:,}")
r1[1].metric("🌍 Countries",      f"{kpis['countries']}")
r1[2].metric("💵 Median Salary",  f"${kpis['median_salary']:,.0f}")
r1[3].metric("🤖 AI Adoption",    f"{kpis['ai_adoption_pct']:.1f}%")
r1[4].metric("📅 Median Exp",     f"{kpis['median_exp']:.0f} yrs")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

r2 = st.columns(5)
r2[0].metric("🏠 Remote %",       f"{kpis['remote_pct']:.1f}%")
r2[1].metric("💻 Full-Stack %",    f"{kpis['fullstack_pct']:.1f}%")
r2[2].metric("📊 Avg Salary",     f"${kpis['avg_salary']:,.0f}")
r2[3].metric("🔤 Top Language",   kpis['top_language'])
r2[4].metric("💰 With Salary",    f"{kpis['with_salary']:,}")

st.markdown("<hr>", unsafe_allow_html=True)

# ── CHART TABS ────────────────────────────────────────────────────────────────
st.markdown('<span class="section-header">◆  Visualisations — All charts reflect active filters</span>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚡  Overview",
    "💰  Salaries",
    "💻  Tech Stack",
    "🤖  AI & Culture",
    "🌍  Global",
])

# ── Tab 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<span class="clabel">Chart 01 · Pie Chart</span><span class="ctitle">Remote Work Distribution</span>', unsafe_allow_html=True)
        st.pyplot(pie_remote_work(df), use_container_width=True)
    with c2:
        st.markdown('<span class="clabel">Chart 03 · Line Chart</span><span class="ctitle">Cumulative Experience Distribution</span>', unsafe_allow_html=True)
        st.pyplot(line_exp_cumulative(df), use_container_width=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<span class="clabel">Chart 08 · Area Chart</span><span class="ctitle">Developer Type Composition by Age Group</span>', unsafe_allow_html=True)
    st.pyplot(area_devtype_by_age(df), use_container_width=True)

# ── Tab 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<span class="clabel">Chart 02 · Histogram</span><span class="ctitle">Developer Salary Distribution (USD)</span>', unsafe_allow_html=True)
    st.pyplot(histogram_salary(df), use_container_width=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<span class="clabel">Chart 06 · Box Plot</span><span class="ctitle">Salary Spread by Age Group</span>', unsafe_allow_html=True)
        st.pyplot(box_salary_by_age(df), use_container_width=True)
    with c2:
        st.markdown('<span class="clabel">Chart 10 · Violin Plot</span><span class="ctitle">Salary Shape by Work Style</span>', unsafe_allow_html=True)
        st.pyplot(violin_salary_remote(df), use_container_width=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<span class="clabel">Chart 05 · Scatter Plot</span><span class="ctitle">Experience vs Salary (coloured by Work Style)</span>', unsafe_allow_html=True)
    st.pyplot(scatter_exp_salary(df), use_container_width=True)

# ── Tab 3 ─────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<span class="clabel">Chart 04 · Bar Chart</span><span class="ctitle">Top 15 Programming Languages</span>', unsafe_allow_html=True)
    st.pyplot(bar_top_languages(df, top_n=15), use_container_width=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<span class="clabel">Chart 07 · Heatmap</span><span class="ctitle">Feature Correlation Matrix</span>', unsafe_allow_html=True)
    st.pyplot(heatmap_correlation(df), use_container_width=True)

# ── Tab 4 ─────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<span class="clabel">Chart 09 · Count Plot</span><span class="ctitle">AI Tool Adoption by Employment Type</span>', unsafe_allow_html=True)
    st.pyplot(count_ai_adoption(df), use_container_width=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<span class="clabel">◆ Filtered Data Table</span><span class="ctitle">Survey Records (first 500 rows)</span>', unsafe_allow_html=True)
    show_cols = ["Age","Country","DevType_Primary","EdLevel_Short","RemoteWork",
                 "YearsCodePro","ConvertedCompYearly","AISelect","Employment_Primary"]
    st.dataframe(
        df[show_cols].head(500).rename(columns={
            "DevType_Primary":"Dev Type","EdLevel_Short":"Education",
            "YearsCodePro":"Exp (yrs)","ConvertedCompYearly":"Salary (USD)",
            "Employment_Primary":"Employment",
        }),
        use_container_width=True, height=320,
    )

# ── Tab 5 ─────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown('<span class="clabel">★ Bonus · Bubble Chart</span><span class="ctitle">Top 15 Countries — Respondent Count vs Median Salary</span>', unsafe_allow_html=True)
    st.caption("Bubble size = respondent count  ·  Colour = median salary level")
    st.pyplot(bubble_countries(df, top_n=15), use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center;
            padding-bottom:14px; flex-wrap:wrap; gap:8px;">
  <span style="font-family:'Inter',sans-serif; font-size:0.75rem; color:#64748B;">
    Stack Overflow Developer Survey 2023 &nbsp;·&nbsp;
    Exploratory Data Analysis &nbsp;·&nbsp; Created by: Aqib Moeen
  </span>
  <span style="font-family:'Inter',sans-serif; font-size:0.75rem; color:#94A3B8;">
    Pandas &nbsp;·&nbsp; Matplotlib &nbsp;·&nbsp; Seaborn &nbsp;·&nbsp; Streamlit
  </span>
</div>
""", unsafe_allow_html=True)
