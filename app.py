"""
FairCV Research Dashboard — AI Resume Screening & Bias Analysis
Main entry point for Streamlit application.
"""

import streamlit as st

st.set_page_config(
    page_title="FairCV Research Dashboard",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Global CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary:    #0d1117;
    --bg-card:       #161b22;
    --bg-card2:      #1c2128;
    --accent-teal:   #2dd4bf;
    --accent-amber:  #f59e0b;
    --accent-rose:   #f43f5e;
    --accent-violet: #8b5cf6;
    --accent-sky:    #38bdf8;
    --text-primary:  #e6edf3;
    --text-muted:    #7d8590;
    --border:        #30363d;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

h1, h2, h3, h4 { font-family: 'Space Mono', monospace !important; }

.stMetric { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 1rem; }
.stMetric label { color: var(--text-muted) !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 1px; }
.stMetric [data-testid="stMetricValue"] { color: var(--accent-teal) !important; font-family: 'Space Mono', monospace; }

div[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

.hero-banner {
    background: linear-gradient(135deg, #0d1117 0%, #1a1f2e 40%, #0f2027 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; top: 0; right: 0; bottom: 0; left: 0;
    background: radial-gradient(ellipse at 70% 50%, rgba(45,212,191,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--accent-teal);
    margin: 0 0 0.5rem 0;
    letter-spacing: -1px;
}
.hero-sub {
    font-size: 1rem;
    color: var(--text-muted);
    margin: 0;
    max-width: 600px;
    line-height: 1.6;
}
.tag {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-right: 6px;
    margin-top: 8px;
}
.tag-teal   { background: rgba(45,212,191,0.15); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.3); }
.tag-amber  { background: rgba(245,158,11,0.15);  color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.tag-rose   { background: rgba(244,63,94,0.15);   color: #f43f5e; border: 1px solid rgba(244,63,94,0.3); }
.tag-violet { background: rgba(139,92,246,0.15);  color: #8b5cf6; border: 1px solid rgba(139,92,246,0.3); }

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: var(--accent-teal); }
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent-teal);
    line-height: 1;
    margin-bottom: 0.3rem;
}
.kpi-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    color: var(--accent-teal);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
    margin: 2rem 0 1.2rem 0;
}

.insight-box {
    background: var(--bg-card2);
    border-left: 3px solid var(--accent-teal);
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.9rem;
    line-height: 1.6;
}
.warning-box {
    background: rgba(244,63,94,0.08);
    border-left: 3px solid var(--accent-rose);
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.9rem;
}
.amber-box {
    background: rgba(245,158,11,0.08);
    border-left: 3px solid var(--accent-amber);
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.9rem;
}

.progress-step {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.step-done { border-left: 3px solid #22c55e; }
.step-wip  { border-left: 3px solid var(--accent-amber); }
.step-todo { border-left: 3px solid var(--border); opacity: 0.65; }

.model-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 6px;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
}
.badge-lr     { background: rgba(56,189,248,0.15); color: #38bdf8; }
.badge-rf     { background: rgba(34,197,94,0.15);  color: #22c55e; }
.badge-mlp    { background: rgba(251,146,60,0.15); color: #fb923c; }
.badge-paper  { background: rgba(139,92,246,0.15); color: #8b5cf6; }

.roadmap-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s;
}
.roadmap-card:hover { border-color: var(--accent-violet); transform: translateX(4px); }
.roadmap-easy   { border-left: 4px solid #22c55e; }
.roadmap-medium { border-left: 4px solid var(--accent-amber); }
.roadmap-hard   { border-left: 4px solid var(--accent-rose); }

.paper-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.paper-title { font-family: 'Space Mono', monospace; font-size: 0.95rem; color: var(--accent-sky); margin-bottom: 0.4rem; }
.paper-meta  { font-size: 0.76rem; color: var(--text-muted); margin-bottom: 0.8rem; }

/* Streamlit tweaks */
[data-testid="stMarkdownContainer"] p { color: var(--text-primary); line-height: 1.65; }
.stButton > button {
    background: rgba(45,212,191,0.1) !important;
    border: 1px solid rgba(45,212,191,0.4) !important;
    color: var(--accent-teal) !important;
    font-family: 'Space Mono', monospace !important;
    border-radius: 6px !important;
}
.stButton > button:hover {
    background: rgba(45,212,191,0.2) !important;
    border-color: var(--accent-teal) !important;
}
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}
[data-baseweb="tab"] { color: var(--text-muted) !important; }
[aria-selected="true"] { color: var(--accent-teal) !important; border-bottom: 2px solid var(--accent-teal) !important; }
.stTabs [data-baseweb="tab-list"] { background: var(--bg-card) !important; border-radius: 8px; padding: 4px; }
.stDataFrame { background: var(--bg-card) !important; }
[data-testid="stTable"] th { background: var(--bg-card2) !important; color: var(--text-muted) !important; }
</style>
""", unsafe_allow_html=True)


# --- Import pages ---
from components.sidebar       import render_sidebar
from components.overview       import render_overview
from components.progress_tracker import render_progress
from components.dataset_analysis import render_dataset
from components.model_analysis   import render_models
from components.paper_review     import render_papers
from components.roadmap          import render_roadmap


def main():
    page = render_sidebar()

    if page == "🏠 Project Overview":
        render_overview()
    elif page == "📊 Progress Tracker":
        render_progress()
    elif page == "🗄️ Dataset Analysis":
        render_dataset()
    elif page == "🤖 Model Development":
        render_models()
    elif page == "📚 Research Papers":
        render_papers()
    elif page == "🚀 Improvement Roadmap":
        render_roadmap()


if __name__ == "__main__":
    main()
