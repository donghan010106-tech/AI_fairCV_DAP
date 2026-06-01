import streamlit as st

st.set_page_config(
    page_title="FairCV Research Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    --accent-green:  #22c55e;
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
    background-color: #0a0e14 !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
h1, h2, h3, h4 { font-family: 'Space Mono', monospace !important; }

.stMetric { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 1rem; }
.stMetric label { color: var(--text-muted) !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 1px; }
.stMetric [data-testid="stMetricValue"] { color: var(--accent-teal) !important; font-family: 'Space Mono', monospace; }

div[data-testid="stExpander"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }

.hero-banner {
    background: linear-gradient(135deg, #0d1117 0%, #1a1f2e 40%, #0f2027 100%);
    border: 1px solid var(--border); border-radius: 16px;
    padding: 2.5rem 3rem; margin-bottom: 2rem;
    position: relative; overflow: hidden;
}
.hero-banner::before {
    content: ''; position: absolute; top: 0; right: 0; bottom: 0; left: 0;
    background: radial-gradient(ellipse at 70% 50%, rgba(45,212,191,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title { font-family: 'Space Mono', monospace; font-size: 2.2rem; font-weight: 700; color: var(--accent-teal); margin: 0 0 0.5rem 0; letter-spacing: -1px; }
.hero-sub   { font-size: 1rem; color: var(--text-muted); margin: 0; max-width: 640px; line-height: 1.6; }

.tag { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin-right: 6px; margin-top: 8px; }
.tag-teal   { background: rgba(45,212,191,0.15);  color: #2dd4bf; border: 1px solid rgba(45,212,191,0.3); }
.tag-amber  { background: rgba(245,158,11,0.15);  color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.tag-rose   { background: rgba(244,63,94,0.15);   color: #f43f5e; border: 1px solid rgba(244,63,94,0.3); }
.tag-violet { background: rgba(139,92,246,0.15);  color: #8b5cf6; border: 1px solid rgba(139,92,246,0.3); }
.tag-sky    { background: rgba(56,189,248,0.15);  color: #38bdf8; border: 1px solid rgba(56,189,248,0.3); }
.tag-green  { background: rgba(34,197,94,0.15);   color: #22c55e; border: 1px solid rgba(34,197,94,0.3); }

.kpi-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1.4rem 1.6rem; text-align: center; }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 2rem; font-weight: 700; color: var(--accent-teal); line-height: 1; margin-bottom: 0.3rem; }
.kpi-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; }

.section-header { font-family: 'Space Mono', monospace; font-size: 1.3rem; color: var(--accent-teal); border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin: 2rem 0 1.2rem 0; }

.insight-box  { background: var(--bg-card2); border-left: 3px solid var(--accent-teal);   border-radius: 0 8px 8px 0; padding: 1rem 1.2rem; margin: 0.8rem 0; font-size: 0.9rem; line-height: 1.6; }
.warning-box  { background: rgba(244,63,94,0.08);  border-left: 3px solid var(--accent-rose);   border-radius: 0 8px 8px 0; padding: 1rem 1.2rem; margin: 0.8rem 0; font-size: 0.9rem; line-height: 1.6; }
.amber-box    { background: rgba(245,158,11,0.08); border-left: 3px solid var(--accent-amber);  border-radius: 0 8px 8px 0; padding: 1rem 1.2rem; margin: 0.8rem 0; font-size: 0.9rem; line-height: 1.6; }
.green-box    { background: rgba(34,197,94,0.08);  border-left: 3px solid var(--accent-green);  border-radius: 0 8px 8px 0; padding: 1rem 1.2rem; margin: 0.8rem 0; font-size: 0.9rem; line-height: 1.6; }
.violet-box   { background: rgba(139,92,246,0.08); border-left: 3px solid var(--accent-violet); border-radius: 0 8px 8px 0; padding: 1rem 1.2rem; margin: 0.8rem 0; font-size: 0.9rem; line-height: 1.6; }

.model-badge { display: inline-block; padding: 3px 12px; border-radius: 6px; font-family: 'Space Mono', monospace; font-size: 0.78rem; font-weight: 700; }
.badge-lr    { background: rgba(56,189,248,0.15);  color: #38bdf8; }
.badge-rf    { background: rgba(34,197,94,0.15);   color: #22c55e; }
.badge-mlp   { background: rgba(251,146,60,0.15);  color: #fb923c; }

.fusion-card  { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
.fusion-early  { border-top: 3px solid #38bdf8; }
.fusion-late   { border-top: 3px solid #f43f5e; }
.fusion-hybrid { border-top: 3px solid #22c55e; }
.fusion-base   { border-top: 3px solid #7d8590; }
.fusion-title  { font-family: 'Space Mono', monospace; font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem; }
.fusion-formula { background: var(--bg-primary); border: 1px solid var(--border); border-radius: 6px; padding: 0.5rem 1rem; margin: 0.6rem 0; font-family: 'Space Mono', monospace; font-size: 0.85rem; color: var(--accent-amber); text-align: center; }

.rq-card     { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem 1.4rem; margin-bottom: 0.8rem; }
.rq-number   { font-family: 'Space Mono', monospace; font-size: 0.7rem; color: var(--accent-teal); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem; }
.rq-question { font-size: 0.95rem; font-weight: 600; margin-bottom: 0.4rem; }
.rq-answer   { font-size: 0.85rem; color: var(--text-muted); line-height: 1.5; }

.paper-card  { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
.paper-title { font-family: 'Space Mono', monospace; font-size: 0.95rem; color: var(--accent-sky); margin-bottom: 0.4rem; }
.paper-meta  { font-size: 0.76rem; color: var(--text-muted); margin-bottom: 0.8rem; }

.result-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.result-table th { background: var(--bg-card2); color: var(--text-muted); padding: 0.5rem 0.8rem; text-align: left; font-family: 'Space Mono', monospace; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid var(--border); }
.result-table td { padding: 0.5rem 0.8rem; border-bottom: 1px solid rgba(48,54,61,0.5); color: var(--text-primary); }
.result-table tr:hover td { background: var(--bg-card2); }
.best-val { color: var(--accent-teal); font-weight: 700; font-family: 'Space Mono', monospace; }
.warn-val { color: var(--accent-rose); font-weight: 700; font-family: 'Space Mono', monospace; }
.mono     { font-family: 'Space Mono', monospace; }

[data-testid="stMarkdownContainer"] p { color: var(--text-primary); line-height: 1.65; }
.stButton > button { background: rgba(45,212,191,0.1) !important; border: 1px solid rgba(45,212,191,0.4) !important; color: var(--accent-teal) !important; font-family: 'Space Mono', monospace !important; border-radius: 6px !important; }
.stButton > button:hover { background: rgba(45,212,191,0.2) !important; }
[data-baseweb="tab"] { color: var(--text-muted) !important; }
[aria-selected="true"] { color: var(--accent-teal) !important; border-bottom: 2px solid var(--accent-teal) !important; }
.stTabs [data-baseweb="tab-list"] { background: var(--bg-card) !important; border-radius: 8px; padding: 4px; }
</style>
""", unsafe_allow_html=True)

from components.sidebar           import render_sidebar
from components.overview          import render_overview
from components.dataset_eda       import render_dataset
from components.baseline_models   import render_baseline
from components.fusion_strategies import render_fusion
from components.fairness_analysis import render_fairness
from components.research_context  import render_research


def main():
    try:
        page = render_sidebar()
    except Exception as e:
        st.error(f"Sidebar error: {e}")
        return

    dispatch = {
        "Project Overview":  render_overview,
        "Dataset & EDA":     render_dataset,
        "Baseline Models":   render_baseline,
        "Fusion Strategies": render_fusion,
        "Fairness Analysis": render_fairness,
        "Research Context":  render_research,
    }

    fn = dispatch.get(page)
    if fn:
        try:
            fn()
        except Exception as e:
            st.error(f"Page render error on '{page}': {e}")
            import traceback
            st.code(traceback.format_exc())
    else:
        st.error(f"Unknown page: '{page}'")


if __name__ == "__main__":
    main()
