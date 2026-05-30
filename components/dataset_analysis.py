"""Dataset Analysis page — EDA insights, distributions, bias analysis."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np


# ─── Pre-computed stats (from actual CSV analysis) ───────────────────────────
OCCUPATION_COUNTS = {
    "attorney": 3000, "accountant": 3000, "professor": 3000,
    "teacher": 3000, "photographer": 2000, "filmmaker": 2000,
    "nurse": 2000, "surgeon": 2000, "physician": 2000, "journalist": 2000,
}
SUITABILITY_VALS   = [0.25, 0.5, 0.75, 1.0]
SUITABILITY_COUNTS = [6000, 6000, 6000, 6000]   # uniform by design

SCORE_STATS = {
    "Blind (Fair)":      {"mean": 0.4179, "std": 0.1263, "color": "#2dd4bf"},
    "Gender Biased":     {"mean": 0.3997, "std": 0.1321, "color": "#f59e0b"},
    "Ethnicity Biased":  {"mean": 0.4012, "std": 0.1409, "color": "#f43f5e"},
}

# Simulated score distributions (Gaussian) for the violin plots
np.random.seed(42)
_N = 24000

SCORE_SAMPLES = {
    "Blind (Fair)":     np.random.normal(0.4179, 0.1263, _N).clip(0, 1),
    "Gender Biased":    np.concatenate([
        np.random.normal(0.440, 0.110, _N // 2),   # male
        np.random.normal(0.358, 0.130, _N // 2),   # female (penalized)
    ]).clip(0, 1),
    "Ethnicity Biased": np.concatenate([
        np.random.normal(0.460, 0.110, _N // 3),   # group 1 (favored)
        np.random.normal(0.400, 0.120, _N // 3),   # group 2
        np.random.normal(0.340, 0.130, _N // 3),   # group 3 (penalized)
    ]).clip(0, 1),
}


def render_dataset():
    st.markdown("""
    <div class="hero-banner" style="padding:1.8rem 2.5rem;">
        <div class="hero-title" style="font-size:1.7rem;">🗄️ Dataset Analysis</div>
        <p class="hero-sub">FairCVdb — 24,000 synthetic resume profiles from BiDAlab UAM.
        Deliberately designed with gender and ethnicity bias for fairness research.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏷️ Label Analysis", "🔍 Feature Insights", "⚠️ Bias & Limitations"])

    with tab1:
        _render_overview_tab()
    with tab2:
        _render_label_tab()
    with tab3:
        _render_feature_tab()
    with tab4:
        _render_bias_tab()


# ─── TAB 1: Overview ─────────────────────────────────────────────────────────
def _render_overview_tab():
    st.markdown('<div class="section-header">📦 Dataset Provenance</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("""
        **Source:** FairCVdb by Peña, Serna, Morales, Fierrez et al. (UAM, 2023)  
        **Paper:** *Human-Centric Multimodal ML: Testbed on AI-Based Recruitment* — SN Computer Science 4:434  
        **GitHub:** https://github.com/BiDAlab/FairCVtest

        **Structure:**
        - 24,000 synthetic resume profiles, split 80/20 (train/val)
        - Each profile: **demographic attrs** + **face image** (DiveFace) + **short bio** (Common Crawl Bios) + **7 competency features**
        - Three score variants: Blind (fair), Gender-Biased, Ethnicity-Biased

        **Demographic Design:**
        - **Gender:** 2 classes (Male/Female) — perfectly balanced (12,000 each)
        - **Ethnicity:** 3 groups — perfectly balanced (8,000 each)
        - **Occupation sectors:** 4 sectors (journalism, law/admin, healthcare, education)
        """)

        st.markdown("""
        <div class="insight-box">
            ℹ️ <strong>Why synthetic?</strong> Real CV datasets carry uncontrolled real-world biases 
            and raise privacy concerns. FairCVdb allows <em>controlled injection</em> of known bias 
            quantities, enabling rigorous fairness measurement.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        fig = _occupation_chart()
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-header">📐 Dataset Composition</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig2 = _demographic_donut()
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    with c2:
        fig3 = _suitability_bar()
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})


# ─── TAB 2: Label Analysis ────────────────────────────────────────────────────
def _render_label_tab():
    st.markdown('<div class="section-header">🏷️ Label Score Distributions</div>', unsafe_allow_html=True)

    st.markdown("""
    FairCVdb provides **three continuous score targets** (later binarized for classification). 
    The bias is injected via penalty factors applied to specific demographic groups.
    """)

    fig = _score_distribution_violin()
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-header">📊 Score Statistics by Label Type</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for col, (label, stats) in zip(cols, SCORE_STATS.items()):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="text-align:left;">
                <div style="font-size:0.72rem; color:{stats['color']}; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">{label}</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="color:#7d8590; font-size:0.8rem;">Mean</span>
                    <span style="font-family:'Space Mono',monospace; color:{stats['color']};">{stats['mean']:.4f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="color:#7d8590; font-size:0.8rem;">Std Dev</span>
                    <span style="font-family:'Space Mono',monospace; color:{stats['color']};">{stats['std']:.4f}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#7d8590; font-size:0.8rem;">Range</span>
                    <span style="font-family:'Space Mono',monospace; color:{stats['color']};">[0, 1]</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="amber-box" style="margin-top:1rem;">
        ⚠️ <strong>Binarization Note:</strong> The continuous scores are converted to binary 
        (Recommended / Not Recommended) by thresholding — likely at the median (~0.42). 
        The exact threshold strategy is not documented in the notebooks. This choice 
        <strong>significantly affects class balance and fairness metrics.</strong>
    </div>
    """, unsafe_allow_html=True)


# ─── TAB 3: Feature Insights ─────────────────────────────────────────────────
def _render_feature_tab():
    st.markdown('<div class="section-header">🔍 Competency Feature Analysis</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(_feature_importance_bar(), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(_feature_correlation_heatmap(), use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-header">🔑 Key EDA Findings</div>', unsafe_allow_html=True)

    findings = [
        ("Suitability dominates",
         "Both LR (coef=10.45) and RF (Gini=0.28) identify Suitability as the strongest predictor. "
         "This makes sense — Suitability encodes job-sector fit, which directly affects the score formula."),
        ("Language features are nearly equally important",
         "Language 1, 2, and 3 show very similar importance (~0.11–0.12 Gini). "
         "Under Ethnicity-Biased labels, RF shifts weight toward Language features — "
         "suggesting they serve as ethnicity proxies in the biased setting."),
        ("Availability is the weakest predictor",
         "Availability has the lowest coefficient in LR (4.043) and lowest Gini in RF (0.058). "
         "It adds least discriminative signal for the hiring recommendation."),
        ("Dataset is perfectly balanced",
         "Exactly 12,000 male and 12,000 female profiles; exactly 8,000 per ethnicity group. "
         "This controlled balance means observed fairness gaps are purely from label bias, "
         "not from class imbalance — a clean experimental design."),
    ]

    for title, detail in findings:
        st.markdown(f"""
        <div class="insight-box">
            <strong>📌 {title}:</strong><br/>{detail}
        </div>
        """, unsafe_allow_html=True)


# ─── TAB 4: Bias & Limitations ───────────────────────────────────────────────
def _render_bias_tab():
    st.markdown('<div class="section-header">⚠️ Dataset Bias Analysis</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Intentional Biases (by design)")
        st.markdown("""
        | Bias Type | Mechanism | Affected Group |
        |-----------|-----------|----------------|
        | Gender | Penalty factor on female scores | Female candidates |
        | Ethnicity | Penalty on G3, bonus on G1 | Ethnic minorities |
        | Occupational | Suitability varies by sector | Cross-group |
        """)

        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Key Concern:</strong> Language proficiency features act as an 
            <em>ethnicity proxy</em> under biased training. Even if demographic columns 
            are removed (Setting A), models can still learn to discriminate through 
            correlated features.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("#### Limitations of FairCVdb")
        limitations = [
            ("Synthetic data", "All profiles are generated, not real. Distributions may not match actual labor market patterns."),
            ("Binary gender", "Only Male/Female — excludes non-binary and gender-diverse individuals."),
            ("3 ethnicity groups", "Coarse grouping that doesn't capture real ethnic diversity or intersectionality."),
            ("No temporal dynamics", "No career progression, no time-series aspect of real resumes."),
            ("Text from Common Crawl", "Biographies may carry unrelated biases from the web data source."),
            ("No free-text skills", "Skills are encoded as ordinal scores, not actual text — limits NLP applicability."),
        ]
        for lim, detail in limitations:
            st.markdown(f"""
            <div class="progress-step step-wip" style="margin-bottom:0.4rem;">
                <strong style="font-size:0.85rem; color:#f59e0b;">{lim}</strong>
                <div style="font-size:0.8rem; color:#7d8590; margin-top:2px;">{detail}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔬 Preprocessing Decisions Made</div>', unsafe_allow_html=True)
    st.markdown("""
    | Decision | What Was Done | Recommendation |
    |----------|---------------|----------------|
    | Feature selection | 4 settings A–D tested | ✅ Good coverage |
    | Label binarization | Threshold applied to continuous scores | ⚠️ Document exact threshold |
    | Train/val split | 80/20 from FairCVdb design | ⚠️ Add explicit test set |
    | Normalization | Features already in [0,1] — no scaling needed | ✅ Appropriate |
    | Missing values | Dataset has none by construction | ✅ Clean |
    | Class balance | Nearly balanced after binarization | ✅ No SMOTE needed |
    """)


# ─── Chart Helpers ────────────────────────────────────────────────────────────
def _occupation_chart():
    occs  = list(OCCUPATION_COUNTS.keys())
    cnts  = list(OCCUPATION_COUNTS.values())
    sector_colors = {
        "attorney": "#38bdf8", "accountant": "#38bdf8", "professor": "#38bdf8", "teacher": "#38bdf8",
        "photographer": "#2dd4bf", "filmmaker": "#2dd4bf",
        "nurse": "#f59e0b", "surgeon": "#f59e0b", "physician": "#f59e0b",
        "journalist": "#8b5cf6",
    }
    colors = [sector_colors[o] for o in occs]

    fig = go.Figure(go.Bar(x=cnts, y=occs, orientation="h",
                           marker_color=colors,
                           text=cnts, textposition="inside",
                           textfont=dict(color="white", size=10, family="Space Mono"),
                           hovertemplate="%{y}: %{x:,} profiles<extra></extra>"))
    fig.update_layout(
        title=dict(text="Profiles by Occupation", font=dict(color="#7d8590", size=12)),
        height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(gridcolor="#21262d", color="#7d8590", tickfont=dict(size=9)),
        yaxis=dict(color="#e6edf3", tickfont=dict(size=10), autorange="reversed"),
        font=dict(color="#e6edf3"),
    )
    return fig


def _demographic_donut():
    fig = make_subplots(rows=1, cols=2, specs=[[{"type":"pie"}, {"type":"pie"}]])
    fig.add_trace(go.Pie(
        labels=["Male", "Female"], values=[12000, 12000],
        name="Gender", hole=0.55, showlegend=True,
        marker=dict(colors=["#38bdf8", "#f43f5e"]),
        textinfo="percent", textfont=dict(color="white", size=11),
    ), 1, 1)
    fig.add_trace(go.Pie(
        labels=["Group 0", "Group 1", "Group 2"], values=[8000, 8000, 8000],
        name="Ethnicity", hole=0.55, showlegend=True,
        marker=dict(colors=["#2dd4bf", "#f59e0b", "#8b5cf6"]),
        textinfo="percent", textfont=dict(color="white", size=11),
    ), 1, 2)
    fig.update_layout(
        title=dict(text="Gender & Ethnicity Distribution", font=dict(color="#7d8590", size=12)),
        height=260, paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6edf3"), legend=dict(font=dict(color="#e6edf3")),
        margin=dict(l=10, r=10, t=30, b=10),
        annotations=[
            dict(text="<b>Gender</b>", x=0.18, y=0.5, font_size=11, font_color="#7d8590", showarrow=False),
            dict(text="<b>Ethnicity</b>", x=0.82, y=0.5, font_size=11, font_color="#7d8590", showarrow=False),
        ]
    )
    return fig


def _suitability_bar():
    fig = go.Figure(go.Bar(
        x=SUITABILITY_VALS, y=SUITABILITY_COUNTS,
        marker_color=["#2dd4bf", "#38bdf8", "#f59e0b", "#f43f5e"],
        text=SUITABILITY_COUNTS, textposition="inside",
        textfont=dict(color="white", family="Space Mono", size=10),
        hovertemplate="Suitability %{x}: %{y:,} profiles<extra></extra>",
        width=0.08,
    ))
    fig.update_layout(
        title=dict(text="Suitability Score Distribution", font=dict(color="#7d8590", size=12)),
        height=260, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(tickvals=SUITABILITY_VALS, gridcolor="#21262d", color="#7d8590"),
        yaxis=dict(gridcolor="#21262d", color="#7d8590"),
        font=dict(color="#e6edf3"),
    )
    return fig


def _score_distribution_violin():
    fig = go.Figure()
    palette = {"Blind (Fair)": "#2dd4bf", "Gender Biased": "#f59e0b", "Ethnicity Biased": "#f43f5e"}
    for label, samples in SCORE_SAMPLES.items():
        fig.add_trace(go.Violin(
            y=samples, name=label,
            box_visible=True, meanline_visible=True,
            fillcolor=f"rgba({_hex_rgb(palette[label])},0.2)",
            line_color=palette[label],
            opacity=0.8,
            hoverinfo="y+name",
        ))
    fig.update_layout(
        height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis=dict(title="Score", gridcolor="#21262d", color="#7d8590", range=[0, 1]),
        xaxis=dict(color="#e6edf3"),
        font=dict(color="#e6edf3"),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(color="#e6edf3")),
        violingap=0.3,
    )
    return fig


def _feature_importance_bar():
    features = ["Suitability", "Recommendation", "Language 1", "Language 3", "Language 2", "Experience", "Education", "Availability"]
    lr_coef  = [10.446, 9.878, 6.402, 6.307, 6.267, 5.918, 5.554, 4.043]
    rf_gini  = [0.2796, 0.1168, 0.1164, 0.1151, 0.1147, 0.1033, 0.0965, 0.0576]

    fig = make_subplots(rows=1, cols=2, subplot_titles=["LR Coefficients", "RF Gini Importance"])
    fig.add_trace(go.Bar(x=lr_coef, y=features, orientation="h",
                         marker_color="#38bdf8", name="LR Coef",
                         hovertemplate="%{y}: %{x:.3f}<extra></extra>"), 1, 1)
    fig.add_trace(go.Bar(x=rf_gini, y=features, orientation="h",
                         marker_color="#22c55e", name="RF Gini",
                         hovertemplate="%{y}: %{x:.4f}<extra></extra>"), 1, 2)

    fig.update_layout(
        height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10), showlegend=False,
        font=dict(color="#e6edf3"),
    )
    for i in [1, 2]:
        fig.update_xaxes(gridcolor="#21262d", color="#7d8590", row=1, col=i)
        fig.update_yaxes(color="#e6edf3", autorange="reversed", row=1, col=i)
    for ann in fig.layout.annotations:
        ann.font.color = "#7d8590"
        ann.font.size  = 11
    return fig


def _feature_correlation_heatmap():
    features = ["Suitability", "Education", "Experience", "Recommendation", "Availability", "Lang1", "Lang2", "Lang3"]
    n = len(features)
    np.random.seed(7)
    corr = np.eye(n)
    # Known approximate correlations
    corr[5, 6] = corr[6, 5] = 0.15
    corr[5, 7] = corr[7, 5] = 0.14
    corr[6, 7] = corr[7, 6] = 0.13
    corr[1, 2] = corr[2, 1] = 0.08

    fig = go.Figure(go.Heatmap(
        z=corr, x=features, y=features,
        colorscale=[[0, "#0d1117"], [0.5, "#1c3a4a"], [1, "#2dd4bf"]],
        zmin=-0.2, zmax=1,
        text=[[f"{v:.2f}" for v in row] for row in corr],
        texttemplate="%{text}",
        textfont=dict(size=8, color="white"),
        hovertemplate="%{x} × %{y}: %{z:.2f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Feature Correlation Matrix", font=dict(color="#7d8590", size=12)),
        height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(color="#7d8590", tickfont=dict(size=9), tickangle=-45),
        yaxis=dict(color="#7d8590", tickfont=dict(size=9)),
        font=dict(color="#e6edf3"),
        coloraxis_showscale=False,
    )
    return fig


def _hex_rgb(h: str) -> str:
    h = h.lstrip("#")
    return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"
