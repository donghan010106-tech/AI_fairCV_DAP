"""Project Overview page — hero, KPIs, pipeline diagram."""

import streamlit as st
import plotly.graph_objects as go


def render_overview():
    # ── Hero ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">AI Resume Screening<br/>& Fairness Audit System</div>
        <p class="hero-sub">
            Investigating how classical ML models (LR, RF, MLP) classify job candidates using the 
            FairCVdb dataset — with explicit measurement of gender and ethnicity bias introduced 
            by biased training labels. Grounded in three peer-reviewed research papers.
        </p>
        <div style="margin-top:1rem;">
            <span class="tag tag-teal">FairCVdb · 24,000 profiles</span>
            <span class="tag tag-amber">3 ML Models</span>
            <span class="tag tag-violet">3 Research Papers</span>
            <span class="tag tag-rose">Bias Measurement</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Cards ─────────────────────────────────────────────────────────
    kpis = [
        ("24,000",  "Resume Profiles"),
        ("8",       "Input Features"),
        ("3",       "Label Variants"),
        ("0.997",   "Best ROC-AUC"),
        ("0.966",   "Best F1 Score"),
        ("0.321",   "Max EO Gap (Eth.)"),
    ]
    cols = st.columns(6)
    for col, (val, label) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Two columns: Objective + Pipeline ─────────────────────────────────
    left, right = st.columns([1, 1.3], gap="large")

    with left:
        st.markdown('<div class="section-header">🎯 Problem Statement</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-box">
            <strong>Core Question:</strong> Can classical ML classifiers accurately screen resumes 
            using only competency-based features — and do they remain fair when training labels 
            encode gender or ethnicity bias?
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **Input → System → Output**

        | Component | Detail |
        |-----------|--------|
        | **Input** | 7 competency features + 3 label types |
        | **Models** | Logistic Regression, Random Forest, MLP |
        | **Output** | Binary: Recommended / Not Recommended |
        | **Audit** | Demographic Parity Gap + Equality of Opportunity Gap |

        **3 Label Scenarios Tested:**
        - **Blind (Fair)** — scores purely from competency, no demographic penalty
        - **Gender Biased** — female candidates penalized in training scores  
        - **Ethnicity Biased** — one ethnic group overrated, another penalized
        """)

        st.markdown('<div class="section-header">🔑 Key Research Insight</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Critical Finding:</strong> Logistic Regression achieves F1=0.966 and 
            ROC-AUC=0.997 on fair labels, yet shows an Equality of Opportunity Gap of 
            <strong>0.321 on Ethnicity-Biased labels</strong> — revealing that high 
            classification accuracy does NOT guarantee fairness.
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-header">⚙️ ML Pipeline</div>', unsafe_allow_html=True)

        fig = _pipeline_diagram()
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── System Architecture ────────────────────────────────────────────────
    st.markdown('<div class="section-header">🏗️ System Architecture</div>', unsafe_allow_html=True)

    arch_cols = st.columns(5)
    arch_steps = [
        ("📦", "FairCVdb", "24K synthetic profiles\nimage + text + tabular\ngender & ethnicity labels"),
        ("🔬", "EDA & Analysis", "Distribution analysis\nBias visualization\nFeature correlation"),
        ("⚙️", "Preprocessing", "Label encoding\nTrain/val split\nFeature selection"),
        ("🤖", "Model Training", "LR · RF · MLP\nHyperparam tuning\nCross-validation"),
        ("⚖️", "Fairness Audit", "DP Gap\nEO Gap\nROC per label type"),
    ]
    for col, (icon, title, detail) in zip(arch_cols, arch_steps):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="text-align:left; padding: 1rem;">
                <div style="font-size:1.6rem; margin-bottom:0.4rem;">{icon}</div>
                <div style="font-family:'Space Mono',monospace; font-size:0.85rem; color:#2dd4bf; margin-bottom:0.4rem;">{title}</div>
                <div style="font-size:0.75rem; color:#7d8590; white-space:pre-line; line-height:1.6;">{detail}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Feature Overview Table ─────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Feature Set Overview</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        **Candidate Competency Features (used in Setting A)**

        | Feature | Range | Type |
        |---------|-------|------|
        | Suitability | {0.25, 0.5, 0.75, 1.0} | Categorical |
        | Education | {0.2, 0.4, 0.6, 0.8, 1.0} | Ordinal |
        | Experience | {0–1.0, step 0.2} | Ordinal |
        | Recommendation | {0, 1} | Binary |
        | Availability | {0.2–1.0, step 0.2} | Ordinal |
        | Language 1 | {0–1.0, step 0.2} | Ordinal |
        | Language 2 | {0–1.0, step 0.2} | Ordinal |
        | Language 3 | {0–1.0, step 0.2} | Ordinal |
        """)
    with c2:
        st.markdown("""
        **Feature Settings Tested**

        | Setting | Features Included |
        |---------|-------------------|
        | **A: Comp Only** | 7 competency features only |
        | **B: +Demo** | + Gender & Ethnicity columns |
        | **C: +Face** | + Biased face embeddings (20-dim) |
        | **D: +Blind Face** | + Agnostic face embeddings (20-dim) |

        **Key observation:** Performance differences across Settings A–D are 
        minimal (<0.01 F1 for LR/MLP), suggesting competency features already 
        capture most signal. RF degrades with face embeddings added (C/D).
        """)


# ── Helper: pipeline Sankey/flow diagram ────────────────────────────────────
def _pipeline_diagram() -> go.Figure:
    fig = go.Figure()

    nodes = [
        "FairCVdb\n(24K)", "Competency\nFeatures", "Label\nTypes",
        "LR", "RF", "MLP",
        "Accuracy\nMetrics", "Fairness\nAudit"
    ]
    positions = [
        (0.05, 0.5),
        (0.25, 0.7), (0.25, 0.3),
        (0.55, 0.82), (0.55, 0.5), (0.55, 0.18),
        (0.85, 0.7), (0.85, 0.3),
    ]
    colors_node = [
        "#2dd4bf", "#38bdf8", "#f59e0b",
        "#38bdf8", "#22c55e", "#fb923c",
        "#8b5cf6", "#f43f5e",
    ]
    edges = [
        (0, 1), (0, 2),
        (1, 3), (1, 4), (1, 5),
        (2, 3), (2, 4), (2, 5),
        (3, 6), (4, 6), (5, 6),
        (3, 7), (4, 7), (5, 7),
    ]

    for (x0, y0), (x1, y1) in [(positions[i], positions[j]) for i, j in edges]:
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color="#30363d", width=1.5),
                      xref="paper", yref="paper")

    for (x, y), label, color in zip(positions, nodes, colors_node):
        fig.add_shape(type="rect",
                      x0=x-0.085, y0=y-0.09, x1=x+0.085, y1=y+0.09,
                      fillcolor=f"rgba({_hex_to_rgb(color)},0.12)",
                      line=dict(color=color, width=1.5),
                      xref="paper", yref="paper")
        fig.add_annotation(x=x, y=y, text=label.replace("\n", "<br>"),
                            font=dict(size=9, color=color, family="Space Mono"),
                            showarrow=False, xref="paper", yref="paper",
                            align="center")

    fig.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        showlegend=False,
    )
    return fig


def _hex_to_rgb(h: str) -> str:
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r},{g},{b}"
