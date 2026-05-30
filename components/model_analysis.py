"""Model Development page — performance, fairness, feature importance analysis."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# ─── Ground-truth metrics from the uploaded charts ────────────────────────────
SETTINGS = ["A: Comp Only", "B: +Demo", "C: +Face", "D: +Blind Face"]
MODELS   = ["LR", "RF", "MLP"]

PERF_F1 = {
    "LR":  [0.966, 0.966, 0.964, 0.965],
    "RF":  [0.936, 0.934, 0.907, 0.905],
    "MLP": [0.965, 0.964, 0.960, 0.962],
}
PERF_AUC = {
    "LR":  [0.997, 0.997, 0.997, 0.997],
    "RF":  [0.987, 0.987, 0.976, 0.975],
    "MLP": [0.996, 0.997, 0.996, 0.996],
}

# Fairness gaps (Setting A)
LABELS_F = ["Blind", "Gender Bias", "Eth Bias"]
DP_GENDER = {"LR": [0.005, 0.003, 0.004], "RF": [0.011, 0.004, 0.004], "MLP": [0.004, 0.011, 0.007]}
EO_GENDER = {"LR": [0.001, 0.011, 0.321], "RF": [0.004, 0.016, 0.259], "MLP": [0.001, 0.001, 0.252]}
DP_ETHN   = {"LR": [0.023, 0.116, 0.017], "RF": [0.022, 0.119, 0.023], "MLP": [0.020, 0.136, 0.014]}
EO_ETHN   = {"LR": [0.007, 0.278, 0.020], "RF": [0.004, 0.247, 0.054], "MLP": [0.005, 0.273, 0.026]}

LR_COEF = {"Suitability": 10.446, "Recommendation": 9.878, "Language 1": 6.402,
           "Language 3": 6.307, "Language 2": 6.267, "Experience": 5.918,
           "Education": 5.554, "Availability": 4.043}

RF_GINI = {"Suitability": 0.2796, "Recommendation": 0.1168, "Language 1": 0.1164,
           "Language 3": 0.1151, "Language 2": 0.1147, "Experience": 0.1033,
           "Education": 0.0965, "Availability": 0.0576}

COLORS = {"LR": "#38bdf8", "RF": "#22c55e", "MLP": "#fb923c"}
LABEL_COLORS = {"Blind": "#2dd4bf", "Gender Bias": "#f59e0b", "Eth Bias": "#f43f5e"}


def render_models():
    st.markdown("""
    <div class="hero-banner" style="padding:1.8rem 2.5rem;">
        <div class="hero-title" style="font-size:1.7rem;">🤖 Model Development</div>
        <p class="hero-sub">Logistic Regression, Random Forest & MLP trained across 4 feature settings 
        and 3 label types. Performance vs fairness trade-off analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Performance", "⚖️ Fairness Gaps", "🔍 Feature Analysis", "🧠 Model Deep-Dive"])

    with tab1:
        _render_performance()
    with tab2:
        _render_fairness()
    with tab3:
        _render_features()
    with tab4:
        _render_deepdive()


# ─── TAB 1: Performance ──────────────────────────────────────────────────────
def _render_performance():
    st.markdown('<div class="section-header">📈 Model Performance — Blind (Fair) Label</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        All metrics below are evaluated on <strong>Blind (Fair) labels</strong> — the fairness-ideal scenario 
        where scores are purely competency-based. This is the "ceiling" for what a fair system should achieve.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(_grouped_bar("F1 Score", PERF_F1), use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.plotly_chart(_grouped_bar("ROC-AUC", PERF_AUC), use_container_width=True, config={"displayModeBar": False})

    # Summary table
    st.markdown('<div class="section-header">📊 Results Summary Table</div>', unsafe_allow_html=True)

    rows = []
    for m in MODELS:
        for i, setting in enumerate(SETTINGS):
            rows.append({
                "Model": m, "Setting": setting,
                "F1 (Blind)": f"{PERF_F1[m][i]:.3f}",
                "AUC (Blind)": f"{PERF_AUC[m][i]:.3f}",
                "F1 Δ vs A": f"{PERF_F1[m][i]-PERF_F1[m][0]:+.3f}" if i > 0 else "—",
            })

    import pandas as pd
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="amber-box">
        ⚠️ <strong>Critical Observation:</strong> Adding face embeddings (Setting C vs A) 
        <em>hurts</em> RF performance (F1: 0.936 → 0.907, AUC: 0.987 → 0.976) while 
        barely affecting LR and MLP. This suggests RF overfits to irrelevant face-embedding 
        dimensions that don't add signal for this tabular-dominant task.
    </div>
    """, unsafe_allow_html=True)


# ─── TAB 2: Fairness ─────────────────────────────────────────────────────────
def _render_fairness():
    st.markdown('<div class="section-header">⚖️ Fairness Gaps — Setting A (Competency Only)</div>', unsafe_allow_html=True)

    st.markdown("""
    Two fairness metrics measured across 3 label types × 3 models.  
    **Lower = fairer model.** The Blind label represents the ideal; Gender Bias and Ethnicity Bias 
    show how training labels corrupt the model's fairness.
    """)

    metric_sel = st.selectbox("Select Fairness Metric", [
        "Demographic Parity Gap — Gender",
        "Equality of Opportunity Gap — Gender",
        "Demographic Parity Gap — Ethnicity",
        "Equality of Opportunity Gap — Ethnicity",
    ])

    data_map = {
        "Demographic Parity Gap — Gender":       DP_GENDER,
        "Equality of Opportunity Gap — Gender":  EO_GENDER,
        "Demographic Parity Gap — Ethnicity":    DP_ETHN,
        "Equality of Opportunity Gap — Ethnicity": EO_ETHN,
    }

    fig = _fairness_grouped_bar(data_map[metric_sel], metric_sel)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # All-in-one summary
    st.markdown('<div class="section-header">📋 Full Fairness Summary</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Gender Fairness**")
        for m in MODELS:
            eo_eth = EO_GENDER[m][2]
            color = "#f43f5e" if eo_eth > 0.25 else "#f59e0b" if eo_eth > 0.1 else "#22c55e"
            st.markdown(f"""
            <div class="progress-step {'step-done' if eo_eth < 0.1 else 'step-wip'}">
                <span class="model-badge badge-{'lr' if m=='LR' else 'rf' if m=='RF' else 'mlp'}">{m}</span>
                <span style="margin-left:8px; font-size:0.82rem;">EO Gap (Eth.Bias): 
                <strong style="color:{color};">{eo_eth:.3f}</strong></span>
            </div>
            """, unsafe_allow_html=True)
    with c2:
        st.markdown("**Key Fairness Insights**")
        st.markdown("""
        <div class="warning-box">
            🔴 <strong>Ethnicity EO Gaps are critical</strong>: LR=0.321, RF=0.259, MLP=0.252 
            on Ethnicity-Biased labels — well above the 0.1 acceptable threshold.
        </div>
        <div class="insight-box">
            ✅ <strong>On Blind labels</strong>, all models are nearly perfectly fair 
            (DP Gap ≤ 0.023 for both demographics). The bias comes entirely from label design.
        </div>
        <div class="amber-box">
            ⚠️ <strong>LR highest EO gap on Ethnicity</strong> despite best accuracy — 
            confirming that optimizing for accuracy does not guarantee fairness.
        </div>
        """, unsafe_allow_html=True)


# ─── TAB 3: Feature Analysis ─────────────────────────────────────────────────
def _render_features():
    st.markdown('<div class="section-header">🔍 Feature Importance by Model</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = _feature_bar(LR_COEF, "#38bdf8", "LR Feature Coefficients (Setting A, Blind)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown("""
        <div class="insight-box">
            LR assigns roughly equal weight to Language 1/2/3 (6.27–6.40), 
            confirming they provide independent signal rather than redundant information.
            Availability is the weakest predictor (4.04 vs 10.45 for Suitability).
        </div>
        """, unsafe_allow_html=True)

    with c2:
        fig = _feature_bar(RF_GINI, "#22c55e", "RF Gini Importance (Setting A, Blind)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown("""
        <div class="insight-box">
            RF importance is more distributed than LR coefficients, with Suitability 
            still dominant (0.28) but Language features more balanced (~0.11 each). 
            This suggests RF captures non-linear interactions among language skills.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">⚠️ Feature Shift Under Biased Labels (RF)</div>', unsafe_allow_html=True)
    fig2 = _rf_shift_chart()
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>Proxy Feature Effect:</strong> Under Ethnicity-Biased labels, RF increases 
        Language 1 importance (0.116 → 0.174) while Recommendation drops (0.117 → 0.093). 
        This means Language features are acting as <em>proxies for ethnicity</em> — a red flag 
        that persists even without explicit demographic features in the input.
    </div>
    """, unsafe_allow_html=True)


# ─── TAB 4: Model Deep-Dive ──────────────────────────────────────────────────
def _render_deepdive():
    model_sel = st.selectbox("Select Model", MODELS)

    if model_sel == "LR":
        _lr_deepdive()
    elif model_sel == "RF":
        _rf_deepdive()
    else:
        _mlp_deepdive()


def _lr_deepdive():
    st.markdown('<div class="section-header">📐 Logistic Regression Analysis</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, metric, val, color in [
        (c1, "Best F1",   "0.966", "#38bdf8"),
        (c2, "Best AUC",  "0.997", "#38bdf8"),
        (c3, "Best C",    "100",   "#7d8590"),
    ]:
        with col:
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-value" style="color:{color};">{val}</div>
                <div class="kpi-label">{metric}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("**Hyperparameter Tuning (5-Fold CV):**")
    c_vals = [1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2]
    cv_f1  = [0.9626, 0.9706, 0.9714, 0.9714, 0.9714, 0.9715]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=c_vals, y=cv_f1, mode="lines+markers",
                             line=dict(color="#38bdf8", width=2),
                             marker=dict(size=8, color="#38bdf8"),
                             fill="tozeroy", fillcolor="rgba(56,189,248,0.08)",
                             hovertemplate="C=%{x:.0e}<br>CV F1=%{y:.4f}<extra></extra>"))
    fig.add_vline(x=100, line_dash="dash", line_color="#f43f5e",
                  annotation_text="Best C=100", annotation_font_color="#f43f5e")
    fig.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      xaxis=dict(type="log", title="C (regularization)", gridcolor="#21262d",
                                 color="#7d8590", tickfont=dict(family="Space Mono")),
                      yaxis=dict(title="CV F1", gridcolor="#21262d", color="#7d8590"),
                      margin=dict(l=10, r=10, t=10, b=10), font=dict(color="#e6edf3"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class="insight-box">
        F1 plateaus from C=0.1 onwards — LR is largely insensitive to regularization strength 
        beyond this point. The task is nearly linearly separable with competency features. 
        Selecting C=100 provides minimal benefit over C=0.1 but causes no harm.
    </div>
    <div class="amber-box">
        ⚠️ <strong>Issue:</strong> LR confusion matrix (Blind, Setting A) shows 
        TN=2366, FP=62, FN=99, TP=2273. The 99 false negatives (missed recommendations) 
        disproportionately affect minority groups in biased settings.
    </div>
    """, unsafe_allow_html=True)


def _rf_deepdive():
    st.markdown('<div class="section-header">🌲 Random Forest Analysis</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, metric, val, color in [
        (c1, "Best F1",   "0.936", "#22c55e"),
        (c2, "Best AUC",  "0.987", "#22c55e"),
        (c3, "n_trees",   "100",   "#7d8590"),
    ]:
        with col:
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-value" style="color:{color};">{val}</div>
                <div class="kpi-label">{metric}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    **Key observations from RF analysis:**

    - RF underperforms LR and MLP on F1 (0.936 vs ~0.965) despite similar AUC (0.987 vs 0.997)
    - This gap suggests RF's decision boundaries are slightly less calibrated for this near-linear task
    - RF confusion matrix (Blind): TN=2278, FP=150, FN=154, TP=2218 — more balanced errors than LR
    - Adding face embeddings (C/D) *degrades* RF performance significantly (F1: 0.936 → 0.905)

    **Why RF struggles with face embeddings:**
    - 20-dim face embeddings add high-dimensional noise for RF's axis-aligned splits
    - RF treats each embedding dimension as an independent feature — no spatial reasoning
    - LR and MLP learn to down-weight irrelevant dimensions via regularization/backprop
    """)

    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>No hyperparameter tuning performed for RF.</strong> 
        Default sklearn settings used. Tuning n_estimators, max_depth, min_samples_split 
        via GridSearchCV could close the gap with LR/MLP. This is a priority for Phase 7.
    </div>
    """, unsafe_allow_html=True)


def _mlp_deepdive():
    st.markdown('<div class="section-header">🧠 MLP Neural Network Analysis</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, metric, val, color in [
        (c1, "Best F1",      "0.965",   "#fb923c"),
        (c2, "Best AUC",     "0.997",   "#fb923c"),
        (c3, "Architecture", "[32,16]", "#7d8590"),
        (c4, "Best Epoch",   "24",      "#7d8590"),
    ]:
        with col:
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-value" style="color:{color}; font-size:1.4rem;">{val}</div>
                <div class="kpi-label">{metric}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("**Training Loss Curves (simulated from mlp_loss_curves.png):**")

    np.random.seed(42)
    epochs_blind = np.arange(1, 25)
    train_blind  = 0.75 * np.exp(-0.22 * epochs_blind) + 0.02
    val_blind    = -1.0 + 0.3 * np.exp(-0.25 * epochs_blind) + np.random.normal(0, 0.01, 24)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epochs_blind, y=train_blind, name="Train Loss",
                             line=dict(color="#2dd4bf", width=2)))
    fig.add_trace(go.Scatter(x=epochs_blind, y=val_blind, name="Val Loss",
                             line=dict(color="#2dd4bf", width=2, dash="dot")))
    fig.add_vline(x=24, line_dash="dash", line_color="#f59e0b",
                  annotation_text="Best epoch: 24", annotation_font_color="#f59e0b")

    fig.update_layout(height=260, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      xaxis=dict(title="Epoch", gridcolor="#21262d", color="#7d8590"),
                      yaxis=dict(title="Loss", gridcolor="#21262d", color="#7d8590"),
                      margin=dict(l=10, r=10, t=10, b=30),
                      font=dict(color="#e6edf3"),
                      legend=dict(orientation="h", y=1.02, font=dict(color="#e6edf3")))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>Anomalous Validation Loss:</strong> MLP validation loss goes negative 
        (down to ~-1.0) across all label types. This is physiclaly impossible for log-loss 
        and indicates a bug — likely the BCE loss is computed differently from sklearn's 
        convention, or train/val sets have different label distributions. 
        <strong>This must be investigated before trusting MLP results.</strong>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="amber-box">
        ⚠️ <strong>Architecture not tuned:</strong> [32, 16] was chosen without systematic 
        search. Deeper architectures ([64, 32, 16]) or wider layers may improve performance. 
        Dropout (not applied) could help generalization. Batch normalization unexplored.
    </div>
    """, unsafe_allow_html=True)


# ─── Chart Helpers ────────────────────────────────────────────────────────────
def _grouped_bar(metric: str, data: dict) -> go.Figure:
    fig = go.Figure()
    for model in MODELS:
        fig.add_trace(go.Bar(
            x=SETTINGS, y=data[model], name=model,
            marker_color=COLORS[model],
            text=[f"{v:.3f}" for v in data[model]], textposition="outside",
            textfont=dict(size=9, color="white", family="Space Mono"),
            hovertemplate=f"{model}<br>%{{x}}: %{{y:.3f}}<extra></extra>",
        ))
    ymin = min(v for vals in data.values() for v in vals) - 0.02
    fig.update_layout(
        title=dict(text=metric, font=dict(color="#7d8590", size=12)),
        height=330, barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(gridcolor="#21262d", color="#7d8590", tickfont=dict(size=9)),
        yaxis=dict(gridcolor="#21262d", color="#7d8590", range=[ymin, 1.01]),
        legend=dict(orientation="h", y=1.02, font=dict(color="#e6edf3")),
        font=dict(color="#e6edf3"),
    )
    return fig


def _fairness_grouped_bar(data: dict, title: str) -> go.Figure:
    fig = go.Figure()
    for model in MODELS:
        fig.add_trace(go.Bar(
            x=LABELS_F, y=data[model], name=model,
            marker_color=COLORS[model],
            text=[f"{v:.3f}" for v in data[model]], textposition="outside",
            textfont=dict(size=9, color="white", family="Space Mono"),
            hovertemplate=f"{model}<br>%{{x}}: %{{y:.3f}}<extra></extra>",
        ))
    fig.update_layout(
        title=dict(text=title, font=dict(color="#7d8590", size=12)),
        height=320, barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(color="#7d8590"),
        yaxis=dict(gridcolor="#21262d", color="#7d8590", title="Gap (lower=fairer)"),
        legend=dict(orientation="h", y=1.02, font=dict(color="#e6edf3")),
        font=dict(color="#e6edf3"),
        shapes=[dict(type="line", x0=-0.5, x1=2.5, y0=0.1, y1=0.1,
                     line=dict(color="#f43f5e", dash="dash", width=1))],
        annotations=[dict(x=2.5, y=0.1, text="threshold=0.1", font=dict(color="#f43f5e", size=9),
                          showarrow=False, xanchor="right")],
    )
    return fig


def _feature_bar(data: dict, color: str, title: str) -> go.Figure:
    features = list(data.keys())
    values   = list(data.values())
    fig = go.Figure(go.Bar(
        x=values, y=features, orientation="h",
        marker_color=color, marker_opacity=0.85,
        text=[f"{v:.3f}" for v in values], textposition="inside",
        textfont=dict(color="white", size=9, family="Space Mono"),
        hovertemplate="%{y}: %{x:.3f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(color="#7d8590", size=11)),
        height=290, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(gridcolor="#21262d", color="#7d8590"),
        yaxis=dict(color="#e6edf3", autorange="reversed"),
        font=dict(color="#e6edf3"),
    )
    return fig


def _rf_shift_chart() -> go.Figure:
    features = ["Suitability", "Recommendation", "Language 1", "Language 3", "Language 2", "Experience", "Education", "Availability"]
    blind    = [0.2796, 0.1168, 0.1164, 0.1151, 0.1147, 0.1033, 0.0965, 0.0576]
    gender   = [0.209,  0.127,  0.124,  0.120,  0.120,  0.097,  0.094,  0.059]
    ethnicity= [0.200,  0.093,  0.174,  0.165,  0.163,  0.100,  0.083,  0.052]

    fig = go.Figure()
    for vals, name, color in [(blind, "Blind", "#2dd4bf"), (gender, "Gender Biased", "#f59e0b"), (ethnicity, "Eth Biased", "#f43f5e")]:
        fig.add_trace(go.Bar(x=vals, y=features, orientation="h", name=name,
                             marker_color=color, opacity=0.8,
                             hovertemplate=f"{name}<br>%{{y}}: %{{x:.3f}}<extra></extra>"))
    fig.update_layout(
        title=dict(text="RF Feature Importance — Does Bias Shift Which Features Matter?", font=dict(color="#7d8590", size=12)),
        height=310, barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(gridcolor="#21262d", color="#7d8590"),
        yaxis=dict(color="#e6edf3", autorange="reversed"),
        legend=dict(orientation="h", y=1.02, font=dict(color="#e6edf3")),
        font=dict(color="#e6edf3"),
    )
    return fig
