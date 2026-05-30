"""Progress Tracker — timeline and stage status."""

import streamlit as st
import plotly.graph_objects as go


STAGES = [
    {
        "name": "Dataset Collection & Understanding",
        "status": "done",
        "pct": 100,
        "desc": "Acquired FairCVdb (24,000 synthetic resume profiles) from BiDAlab UAM. "
                "Understood 3 modalities: tabular competencies, face images (DiveFace), text bios (Common Crawl). "
                "Confirmed 3 label types: Blind, Gender-Biased, Ethnicity-Biased.",
        "files": ["FairCVdb.csv", "s42979-023-01733-0.pdf (Peña et al. 2023)"],
        "result": "24,000 profiles loaded. 8 competency features + 3 label targets confirmed.",
        "issues": "None — dataset well-structured and balanced (12K per gender, ~8K per ethnicity group).",
    },
    {
        "name": "Exploratory Data Analysis (EDA)",
        "status": "done",
        "pct": 100,
        "desc": "Performed full EDA: class distribution, feature correlations, label distributions, "
                "occupation breakdown, bias score comparisons between demographic groups.",
        "files": ["FairCV_EDA_v2.ipynb"],
        "result": "Dataset perfectly balanced across gender/ethnicity. Suitability is most predictive feature. "
                  "Blind scores ~ N(0.42, 0.13). Biased labels create measurable distribution shifts.",
        "issues": "Blind label is near-continuous (regression), but binarized at threshold for classification. "
                  "Threshold choice not formally justified — may affect fairness metrics.",
    },
    {
        "name": "Data Preprocessing",
        "status": "done",
        "pct": 100,
        "desc": "Selected 4 feature settings (A–D): competency-only, +demographics, +face embeddings, +blind embeddings. "
                "Applied label binarization. Prepared train/val splits. Handled categorical encoding.",
        "files": ["FairCV_Models.ipynb", "pipeline/preprocessing.py"],
        "result": "4 feature settings × 3 label types = 12 experiment conditions ready for training.",
        "issues": "No explicit test set separation found — train/val only. Risk of optimistic evaluation. "
                  "⚠️ Recommend adding held-out test set for final reporting.",
    },
    {
        "name": "Baseline Model Training",
        "status": "done",
        "pct": 100,
        "desc": "Trained Logistic Regression (C=100, L2), Random Forest (default), and MLP (layers=[32,16], "
                "early stopping, Adam) across all 12 experiment conditions. Applied 5-fold CV for LR tuning.",
        "files": ["FairCV_Models.ipynb", "lr_hyperparam.png", "mlp_loss_curves.png"],
        "result": "LR: F1=0.966, AUC=0.997 (Setting A, Blind). RF: AUC=0.987. MLP: F1=0.965, AUC=0.996.",
        "issues": "RF underperforms LR/MLP significantly on F1 (0.936 vs 0.966). MLP validation loss "
                  "goes negative (log-loss artifact) — check loss function implementation.",
    },
    {
        "name": "Initial Fairness Evaluation",
        "status": "done",
        "pct": 100,
        "desc": "Measured Demographic Parity Gap and Equality of Opportunity Gap for gender and ethnicity "
                "across all models and feature settings. Generated ROC curves per label type.",
        "files": ["compare_perf.png", "compare_fairness.png", "lr_roc.png", "rf_roc.png", "mlp_cm.png"],
        "result": "LR fairest on gender DP (0.005), but worst on Ethnicity EO Gap (0.321). "
                  "MLP shows highest DP gap on Gender-Biased labels (0.011). RF most consistent across settings.",
        "issues": "Large EO gaps on Ethnicity-Biased labels across all models (0.252–0.321). "
                  "No fairness mitigation applied yet. All models learn and reproduce the biases.",
    },
    {
        "name": "Feature Importance & Interpretability",
        "status": "done",
        "pct": 100,
        "desc": "Extracted LR coefficients and RF Gini importance. Compared feature rankings across label types. "
                "Analyzed whether bias shifts which features models prioritize.",
        "files": ["lr_coef.png", "rf_importance.png", "rf_importance_by_label.png"],
        "result": "Suitability (#1) and Recommendation (#2) dominate in all models. Under Ethnicity-Biased "
                  "labels, RF reprioritizes Language features (proxy effect). LR: Suitability coef = 10.446.",
        "issues": "Language features acting as ethnicity proxies under biased labels is a critical finding "
                  "that should be highlighted in the final report.",
    },
    {
        "name": "Advanced Optimization",
        "status": "wip",
        "pct": 30,
        "desc": "Planned: Fairness-aware training (reweighting, adversarial debiasing), SHAP explanations, "
                "threshold optimization per demographic group, ensemble methods.",
        "files": [],
        "result": "Not yet started. LR C=100 selected; RF and MLP not yet tuned via GridSearch.",
        "issues": "Priority: implement fairness constraints (e.g., Demographic Parity regularizer). "
                  "Then: SHAP for global + local explanations. Then: calibration.",
    },
    {
        "name": "Model Improvement (NLP/Deep Learning)",
        "status": "todo",
        "pct": 0,
        "desc": "Planned: BERT-based biography encoder, multimodal fusion (early/late), "
                "SensitiveNets for agnostic face embeddings, LLM-based scoring as per FAIRE paper.",
        "files": ["2407_16892v1.pdf (Swati et al. 2024)", "2504_01420v1.pdf (FAIRE 2025)"],
        "result": "N/A",
        "issues": "Requires GPU resources and extended training time. Must align with FairCVtest architecture.",
    },
    {
        "name": "Final Deployment / Demo",
        "status": "todo",
        "pct": 0,
        "desc": "Planned: Streamlit inference demo, REST API (FastAPI), Docker container, "
                "live resume screening with fairness audit output.",
        "files": ["inference/predictor.py"],
        "result": "N/A",
        "issues": "Should include explainability (LIME/SHAP) in the demo output.",
    },
    {
        "name": "Final Report & Presentation",
        "status": "todo",
        "pct": 0,
        "desc": "Planned: Academic report covering dataset, methodology, results, fairness analysis, "
                "paper connections, limitations, and future work.",
        "files": [],
        "result": "N/A",
        "issues": "Dashboard (this file) will serve as visual supplement to the written report.",
    },
]


def render_progress():
    st.markdown("""
    <div class="hero-banner" style="padding: 1.8rem 2.5rem;">
        <div class="hero-title" style="font-size:1.7rem;">📊 Project Progress Tracker</div>
        <p class="hero-sub">End-to-end timeline from dataset collection to deployment.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary row ────────────────────────────────────────────────────────
    done  = sum(1 for s in STAGES if s["status"] == "done")
    wip   = sum(1 for s in STAGES if s["status"] == "wip")
    todo  = sum(1 for s in STAGES if s["status"] == "todo")
    total = len(STAGES)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, color in [
        (c1, f"{done}/{total}", "Stages Complete", "#22c55e"),
        (c2, f"{wip}",          "In Progress",     "#f59e0b"),
        (c3, f"{todo}",         "Not Started",     "#7d8590"),
        (c4, "62%",             "Overall Progress", "#2dd4bf"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value" style="color:{color};">{val}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Gantt / Timeline Chart ─────────────────────────────────────────────
    st.markdown('<div class="section-header">📅 Project Timeline</div>', unsafe_allow_html=True)
    st.plotly_chart(_gantt_chart(), use_container_width=True, config={"displayModeBar": False})

    # ── Stage details ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Stage Details</div>', unsafe_allow_html=True)

    status_icons = {"done": "✅", "wip": "🔄", "todo": "⏳"}
    status_colors = {"done": "#22c55e", "wip": "#f59e0b", "todo": "#7d8590"}
    step_classes = {"done": "step-done", "wip": "step-wip", "todo": "step-todo"}

    for i, stage in enumerate(STAGES, 1):
        icon  = status_icons[stage["status"]]
        color = status_colors[stage["status"]]
        cls   = step_classes[stage["status"]]

        with st.expander(f"{icon} {i:02d}. {stage['name']}  —  {stage['pct']}% complete", expanded=(stage["status"] == "wip")):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**📝 What was done:**  \n{stage['desc']}")

                if stage["issues"]:
                    cls_box = "warning-box" if stage["status"] != "todo" else "amber-box"
                    st.markdown(f'<div class="{cls_box}">⚡ <strong>Issues / Notes:</strong> {stage["issues"]}</div>',
                                unsafe_allow_html=True)

            with col2:
                if stage["files"]:
                    st.markdown("**📁 Related Files:**")
                    for f in stage["files"]:
                        st.markdown(f"- `{f}`")

                if stage["result"] != "N/A":
                    st.markdown(f"""
                    <div class="insight-box" style="margin-top:0.6rem;">
                        <strong>Result:</strong><br/>{stage['result']}
                    </div>
                    """, unsafe_allow_html=True)

            # Progress bar
            st.markdown(f"""
            <div style="margin-top:0.8rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="font-size:0.75rem; color:#7d8590;">Stage completion</span>
                    <span style="font-family:'Space Mono',monospace; font-size:0.75rem; color:{color};">{stage['pct']}%</span>
                </div>
                <div style="background:#0d1117; border-radius:4px; height:6px;">
                    <div style="background:{color}; width:{stage['pct']}%; height:100%; border-radius:4px; transition:width 0.5s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def _gantt_chart() -> go.Figure:
    names = [f"{i+1}. {s['name']}" for i, s in enumerate(STAGES)]
    pcts  = [s["pct"] for s in STAGES]
    colors = {"done": "#22c55e", "wip": "#f59e0b", "todo": "#30363d"}
    bar_colors = [colors[s["status"]] for s in STAGES]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=pcts,
        y=names,
        orientation="h",
        marker=dict(
            color=bar_colors,
            line=dict(color="rgba(0,0,0,0)", width=0),
        ),
        text=[f"{p}%" if p > 0 else "" for p in pcts],
        textposition="inside",
        textfont=dict(color="white", family="Space Mono", size=10),
        hovertemplate="<b>%{y}</b><br>Progress: %{x}%<extra></extra>",
    ))

    fig.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=10, b=10),
        xaxis=dict(
            range=[0, 105],
            ticksuffix="%",
            gridcolor="#21262d",
            color="#7d8590",
            tickfont=dict(family="Space Mono", size=9),
        ),
        yaxis=dict(
            color="#e6edf3",
            tickfont=dict(size=10),
            autorange="reversed",
        ),
        bargap=0.3,
        font=dict(color="#e6edf3"),
    )
    return fig
