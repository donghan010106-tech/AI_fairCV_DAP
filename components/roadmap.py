"""Future Improvement Roadmap page."""

import streamlit as st
import plotly.graph_objects as go


ROADMAP = {
    "🟢 Easy (1–2 weeks)": [
        {
            "title": "Hyperparameter Tuning — RF & MLP",
            "effort": "Low",
            "impact": "Medium",
            "detail": "GridSearchCV for RF (n_estimators, max_depth, min_samples_split) and MLP "
                      "(hidden_layer_sizes, learning_rate, alpha). Expected F1 gain: 0.936 → 0.950+ for RF.",
            "paper": "—",
            "code": "sklearn.model_selection.GridSearchCV",
        },
        {
            "title": "Formal Train / Validation / Test Split",
            "effort": "Low",
            "impact": "High",
            "detail": "Create an 80/10/10 split with held-out test set. Report all final metrics on test set only. "
                      "Currently no test set exists — all reported numbers are optimistic.",
            "paper": "P1 (Peña 2023) uses 80/20 train/val",
            "code": "sklearn.model_selection.train_test_split",
        },
        {
            "title": "SHAP Explainability",
            "effort": "Low",
            "impact": "High",
            "detail": "Apply SHAP for global feature importance and local explanations per candidate. "
                      "Reveal which features drive each individual prediction — critical for fairness auditing.",
            "paper": "P1 (explainability as Human-Centric AI requirement)",
            "code": "pip install shap; shap.TreeExplainer(rf_model)",
        },
        {
            "title": "Document Binarization Threshold",
            "effort": "Very Low",
            "impact": "Medium",
            "detail": "Explicitly document the threshold used to convert continuous scores to binary labels. "
                      "Test sensitivity: does threshold choice affect fairness metrics?",
            "paper": "P1 (Table 2 — score range [0,1])",
            "code": "np.percentile(scores, 50)  # confirm median split",
        },
        {
            "title": "Fairness Reweighing (Pre-processing)",
            "effort": "Low",
            "impact": "High",
            "detail": "Apply IBM AIF360 Reweighing to assign sample weights that counteract demographic bias "
                      "in training labels. No model changes required — only sample weights added.",
            "paper": "P1 (pre-processing bias mitigation)",
            "code": "from aif360.algorithms.preprocessing import Reweighing",
        },
    ],
    "🟡 Medium (2–4 weeks)": [
        {
            "title": "Early-Fusion Multimodal Feature Combination",
            "effort": "Medium",
            "impact": "High",
            "detail": "Concatenate competency features + face embeddings + text TF-IDF/BERT features early, "
                      "train a single classifier on the combined 200+ dim representation. Test against Settings A–D.",
            "paper": "P2 (Swati 2024) — early-fusion achieves lowest MAE",
            "code": "np.concatenate([tabular, face_emb, text_emb], axis=1)",
        },
        {
            "title": "Adversarial Debiasing (In-processing)",
            "effort": "Medium",
            "impact": "High",
            "detail": "Train a classifier to predict Recommended while simultaneously training an adversary "
                      "to predict gender/ethnicity from the learned representations. The adversarial loss "
                      "penalizes demographic leakage.",
            "paper": "P1 (in-processing approaches, SensitiveNets)",
            "code": "from aif360.algorithms.inprocessing import AdversarialDebiasing",
        },
        {
            "title": "BERT / Sentence-Transformer for Biography",
            "effort": "Medium",
            "impact": "High",
            "detail": "Replace TF-IDF bag-of-words with sentence-transformers embeddings for biography text. "
                      "Use 'all-MiniLM-L6-v2' (384-dim). Include blind (anonymized) vs original bio comparison.",
            "paper": "P1 uses BiLSTM; P3 (FAIRE) uses raw LLM text scoring",
            "code": "from sentence_transformers import SentenceTransformer",
        },
        {
            "title": "Threshold Calibration per Demographic Group",
            "effort": "Medium",
            "impact": "High",
            "detail": "Post-process model predictions: find optimal per-group classification thresholds "
                      "to satisfy Equalized Odds or Demographic Parity constraints.",
            "paper": "P1 (post-processing techniques), IBM AIF360",
            "code": "from aif360.algorithms.postprocessing import EqOddsPostprocessing",
        },
        {
            "title": "Calibration Curves & Probability Calibration",
            "effort": "Low-Medium",
            "impact": "Medium",
            "detail": "RF and MLP produce uncalibrated probabilities. Apply Platt Scaling or Isotonic Regression. "
                      "Calibrated probabilities are essential for threshold tuning and fair ranking.",
            "paper": "—",
            "code": "from sklearn.calibration import CalibratedClassifierCV",
        },
    ],
    "🔴 Advanced (1–2 months)": [
        {
            "title": "Full Multimodal Neural Network (P1 Architecture)",
            "effort": "High",
            "impact": "Very High",
            "detail": "Implement the full FairCVtest architecture: ResNet-50 face branch + BiLSTM text branch "
                      "+ FC tabular branch → multimodal fusion → score predictor. Train with Adam for 16 epochs. "
                      "Compare against our classical ML baselines.",
            "paper": "P1 (Peña 2023) — Figure 4 architecture",
            "code": "PyTorch: nn.Module with 3 branches + fusion layer",
        },
        {
            "title": "SensitiveNets — Agnostic Face Embeddings",
            "effort": "High",
            "impact": "Very High",
            "detail": "Apply adversarial regularizer to remove gender/ethnicity from face embeddings during training. "
                      "Expected: KL divergence drops from 0.320 to ~0.026 (as shown in P1 results). "
                      "Compare embeddings before/after using demographic classifier accuracy.",
            "paper": "P1 — SensitiveNets (Morales et al. 2021, IEEE T-PAMI)",
            "code": "github.com/BiDAlab/FairCVtest/SensitiveNets",
        },
        {
            "title": "LLM-Based Scoring Layer (FAIRE Approach)",
            "effort": "High",
            "impact": "Very High",
            "detail": "Implement FAIRE benchmark on FairCVdb biographies: prompt Claude Haiku to score candidates "
                      "on 5 dimensions (Relevance, Skill, Impact, Achievement, Cultural Fit). "
                      "Compare LLM bias against our ML models' bias. Test name perturbation for bias detection.",
            "paper": "P3 (FAIRE 2025) — Claude Haiku is the fairest LLM tested",
            "code": "Anthropic API: claude-haiku-4-5 with FAIRE scoring prompt",
        },
        {
            "title": "Mid-Fusion Strategy Exploration",
            "effort": "High",
            "impact": "High",
            "detail": "Test selective modality fusion: dynamically select which modalities to include per sample "
                      "based on confidence scores. As P2 suggests, some modalities (textual for ethnicity) "
                      "outperform fusion in specific bias scenarios.",
            "paper": "P2 (Swati 2024) — mid-fusion as future work",
            "code": "Dynamic routing via attention weights or confidence thresholds",
        },
        {
            "title": "Fairness-Constrained Optimization (In-processing)",
            "effort": "Very High",
            "impact": "Very High",
            "detail": "Add Demographic Parity or Equalized Odds as differentiable constraints in the loss function. "
                      "Use Lagrangian relaxation or min-max optimization. Visualize the accuracy-fairness Pareto frontier.",
            "paper": "P1 (in-processing constraint-based methods)",
            "code": "fairlearn.reductions.ExponentiatedGradient with DemographicParity()",
        },
    ],
}

METRICS_RADAR = {
    "Current (LR, Setting A)":  [96.6, 99.7, 0.0, 0.0, 62.0, 0.0],
    "After Easy Wins":           [97.0, 99.7, 40.0, 30.0, 70.0, 30.0],
    "After Medium Improvements": [97.5, 99.8, 65.0, 60.0, 80.0, 55.0],
    "After Advanced Research":   [98.0, 99.9, 85.0, 80.0, 90.0, 85.0],
}
RADAR_LABELS = ["F1 (%)", "AUC (%)", "Fairness Score", "Explainability", "Coverage", "Robustness"]


def render_roadmap():
    st.markdown("""
    <div class="hero-banner" style="padding:1.8rem 2.5rem;">
        <div class="hero-title" style="font-size:1.7rem;">🚀 Future Improvement Roadmap</div>
        <p class="hero-sub">Structured research agenda from quick wins to advanced deep learning — 
        grounded in the 3 papers and current gaps identified in our experiments.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Radar chart showing improvement trajectory ─────────────────────────
    st.markdown('<div class="section-header">📈 Improvement Trajectory</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.4, 1])
    with c1:
        st.plotly_chart(_radar_chart(), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.markdown("""
        **Reading the radar chart:**

        The six axes represent key system dimensions. 
        Current implementation (LR, Setting A) excels at prediction accuracy 
        but scores 0 on Fairness Score, Explainability, and Robustness — 
        no mitigation methods applied yet.

        | Phase | Effort | Expected Lift |
        |-------|--------|---------------|
        | Easy wins | 1–2 weeks | Explainability + fair split |
        | Medium | 2–4 weeks | Fairness mitigation + BERT |
        | Advanced | 1–2 months | Full multimodal + LLM |
        """)

        st.markdown("""
        <div class="insight-box">
            ℹ️ <strong>Priority recommendation:</strong> Implement SHAP + Reweighing first 
            (highest impact/effort ratio). These alone would make the system defensible 
            for a real deployment scenario.
        </div>
        """, unsafe_allow_html=True)

    # ── Detailed roadmap by difficulty ────────────────────────────────────
    for tier, items in ROADMAP.items():
        color = "#22c55e" if "Easy" in tier else "#f59e0b" if "Medium" in tier else "#f43f5e"
        cls   = "roadmap-easy" if "Easy" in tier else "roadmap-medium" if "Medium" in tier else "roadmap-hard"

        st.markdown(f"""
        <div class="section-header" style="color:{color}; border-color:{color};">
            {tier}
        </div>
        """, unsafe_allow_html=True)

        for item in items:
            with st.expander(f"  {item['title']}  ·  Impact: {item['impact']}", expanded=False):
                cl, cr = st.columns([2, 1])
                with cl:
                    st.markdown(f"""
                    <div class="roadmap-card {cls}">
                        <div style="font-size:0.88rem; color:#e6edf3; line-height:1.7;">{item['detail']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if item["paper"] != "—":
                        st.markdown(f"""
                        <div style="margin-top:0.5rem; font-size:0.8rem; color:#8b5cf6;">
                            📚 <strong>Grounded in:</strong> {item['paper']}
                        </div>
                        """, unsafe_allow_html=True)

                with cr:
                    for label, val, col in [
                        ("Effort", item["effort"], color),
                        ("Impact", item["impact"], "#2dd4bf"),
                    ]:
                        st.markdown(f"""
                        <div class="kpi-card" style="margin-bottom:8px; padding:0.7rem 1rem;">
                            <div class="kpi-label">{label}</div>
                            <div style="font-family:'Space Mono',monospace; font-size:1rem; color:{col}; margin-top:2px;">{val}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style="background:#0d1117; border:1px solid #30363d; border-radius:6px; padding:0.6rem; margin-top:4px;">
                        <div style="font-size:0.68rem; color:#7d8590; margin-bottom:4px; text-transform:uppercase; letter-spacing:1px;">Code Hint</div>
                        <code style="font-size:0.75rem; color:#2dd4bf;">{item['code']}</code>
                    </div>
                    """, unsafe_allow_html=True)

    # ── Summary priority matrix ────────────────────────────────────────────
    st.markdown('<div class="section-header">⚡ Priority Matrix</div>', unsafe_allow_html=True)
    st.plotly_chart(_priority_matrix(), use_container_width=True, config={"displayModeBar": False})


def _radar_chart() -> go.Figure:
    colors = {"Current (LR, Setting A)": "#7d8590",
              "After Easy Wins": "#22c55e",
              "After Medium Improvements": "#f59e0b",
              "After Advanced Research": "#2dd4bf"}

    fig = go.Figure()
    for name, vals in METRICS_RADAR.items():
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=RADAR_LABELS + [RADAR_LABELS[0]],
            name=name,
            line=dict(color=colors[name], width=2),
            fill="toself",
            fillcolor=f"rgba({_hex_rgb(colors[name])},0.08)",
            hovertemplate="%{theta}: %{r:.0f}<extra></extra>",
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#21262d",
                            tickcolor="#7d8590", color="#7d8590", tickfont=dict(size=8)),
            angularaxis=dict(gridcolor="#21262d", color="#e6edf3", tickfont=dict(size=10)),
        ),
        showlegend=True,
        legend=dict(orientation="v", x=1.05, font=dict(color="#e6edf3", size=10)),
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=140, t=20, b=20),
        font=dict(color="#e6edf3"),
    )
    return fig


def _priority_matrix() -> go.Figure:
    # effort (x: low→high), impact (y: low→high)
    items = [
        ("SHAP Explainability", 1.5, 8.5, "#22c55e"),
        ("Reweighing (Pre-proc.)", 2.0, 9.0, "#22c55e"),
        ("Formal Test Set", 1.0, 8.0, "#22c55e"),
        ("Document Threshold", 0.5, 5.0, "#22c55e"),
        ("RF/MLP Hyperparam Tuning", 2.5, 6.0, "#22c55e"),
        ("Early-Fusion", 5.0, 8.5, "#f59e0b"),
        ("Adversarial Debiasing", 5.5, 9.0, "#f59e0b"),
        ("BERT Biography", 4.5, 7.5, "#f59e0b"),
        ("Threshold Calibration", 3.5, 7.0, "#f59e0b"),
        ("Multimodal NN (P1)", 8.5, 9.5, "#f43f5e"),
        ("SensitiveNets", 8.0, 9.0, "#f43f5e"),
        ("LLM Scoring (P3)", 7.5, 8.0, "#f43f5e"),
        ("Fairness Constraints", 9.0, 9.5, "#f43f5e"),
        ("Mid-Fusion", 7.0, 7.5, "#f43f5e"),
    ]

    fig = go.Figure()
    for name, effort, impact, color in items:
        fig.add_trace(go.Scatter(
            x=[effort], y=[impact], mode="markers+text",
            text=[name], textposition="top center",
            marker=dict(size=14, color=color, opacity=0.85,
                        line=dict(color="rgba(255,255,255,0.3)", width=1)),
            textfont=dict(size=9, color="#e6edf3"),
            hovertemplate=f"<b>{name}</b><br>Effort: {effort:.0f}/10<br>Impact: {impact:.0f}/10<extra></extra>",
            showlegend=False,
        ))

    # Quadrant labels
    for x, y, label in [(2.5, 9.5, "Quick Wins ✅"), (7.5, 9.5, "Major Projects 🔬"),
                         (2.5, 2.0, "Low Priority 💤"), (7.5, 2.0, "Hard + Low Value ❌")]:
        fig.add_annotation(x=x, y=y, text=label, font=dict(size=9, color="#7d8590"),
                           showarrow=False, bgcolor="rgba(0,0,0,0.4)")

    fig.add_shape(type="line", x0=5, x1=5, y0=0, y1=10, line=dict(color="#30363d", dash="dash"))
    fig.add_shape(type="line", x0=0, x1=10, y0=5, y1=5, line=dict(color="#30363d", dash="dash"))

    fig.update_layout(
        height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Implementation Effort →", range=[0, 10.5],
                   gridcolor="#21262d", color="#7d8590", zeroline=False,
                   tickvals=[0,2,4,6,8,10], ticktext=["0","Low","","","High","10"]),
        yaxis=dict(title="Expected Impact ↑", range=[0, 10.5],
                   gridcolor="#21262d", color="#7d8590", zeroline=False,
                   tickvals=[0,2,4,6,8,10], ticktext=["0","Low","","","High","10"]),
        margin=dict(l=50, r=20, t=20, b=50),
        font=dict(color="#e6edf3"),
        showlegend=False,
    )
    return fig


def _hex_rgb(h: str) -> str:
    h = h.lstrip("#")
    return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"
