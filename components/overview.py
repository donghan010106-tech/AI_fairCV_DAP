import streamlit as st


def render_overview():
    # ── Hero ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">FairCV Research Dashboard</div>
        <p class="hero-sub">
            A comparative study of Early, Late, and Weighted Hybrid Fusion strategies
            for fair AI-based resume screening — using Sentence-BERT embeddings,
            lightweight classifiers, and fairness-aware evaluation on FairCVdb.
        </p>
        <div style="margin-top:0.8rem;">
            <span class="tag tag-teal">FairCVdb</span>
            <span class="tag tag-violet">Sentence-BERT</span>
            <span class="tag tag-sky">Early Fusion</span>
            <span class="tag tag-rose">Late Fusion</span>
            <span class="tag tag-green">Hybrid Fusion</span>
            <span class="tag tag-amber">Fairness Audit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ───────────────────────────────────────────────────────
    kpis = [
        ("24,000",  "Resume Profiles",       "Synthetic, FairCVdb"),
        ("3",       "Fusion Strategies",     "Early · Late · Hybrid"),
        ("5",       "Research Questions",    "RQ1 – RQ5"),
        ("12",      "Total Experiments",     "4 strategies × 3 classifiers"),
        ("0.997",   "Best ROC-AUC",          "LR / MLP, Blind label"),
        ("3",       "Fairness Metrics",      "DP · EOO · Disparate Impact"),
    ]
    cols = st.columns(6)
    for col, (val, label, sub) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{label}</div>
                <div style="font-size:0.68rem; color:#7d8590; margin-top:0.3rem;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Pipeline Diagram ──────────────────────────────────────────────
    st.markdown('<div class="section-header">🔄 Experimental Pipeline</div>', unsafe_allow_html=True)

    steps = [
        ("📂", "FairCVdb",       "#2dd4bf", "24,000 profiles\n60 columns"),
        ("🧹", "Preprocessing",  "#f59e0b", "Binarize labels\n4 feature settings"),
        ("🤖", "SBERT Encoding", "#8b5cf6", "all-MiniLM-L6-v2\nbio_anonymized → 384d"),
        ("🔀", "Fusion",         "#38bdf8", "Early / Late\nHybrid"),
        ("📊", "Evaluation",     "#22c55e", "F1 · AUC\nDP · EOO · DI"),
        ("⚖️", "Fairness Audit", "#f43f5e", "Gender · Ethnicity\nBias Mitigation"),
    ]

    # interleave 6 steps + 5 arrows = 11 columns
    widths = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    cols = st.columns(widths)

    step_idx = 0
    for i, col in enumerate(cols):
        if i % 2 == 0:                          # step column
            emoji, title, color, subtitle = steps[step_idx]
            step_idx += 1
            with col:
                st.markdown(f"""
                <div style="background:#1c2128; border:1px solid #30363d; border-radius:10px;
                            padding:0.8rem 0.4rem; text-align:center;">
                    <div style="font-size:1.3rem; margin-bottom:4px;">{emoji}</div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.68rem;
                                color:{color}; font-weight:700; line-height:1.3;">{title}</div>
                    <div style="font-size:0.6rem; color:#7d8590; margin-top:3px; line-height:1.4;">
                        {subtitle.replace(chr(10), "<br>")}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:                                   # arrow column
            with col:
                st.markdown(
                    "<div style='text-align:center; color:#7d8590; font-size:1rem; "
                    "padding-top:1.2rem;'>→</div>",
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Research Questions ────────────────────────────────────────────
    st.markdown('<div class="section-header">❓ Research Questions</div>', unsafe_allow_html=True)

    rqs = [
        ("RQ1", "Predictive Performance",
         "Which fusion strategy achieves better predictive performance in resume evaluation?",
         "Evaluated via F1, ROC-AUC across Early, Late, Weighted Hybrid Fusion × LR, RF, MLP."),
        ("RQ2", "Fairness Outcomes",
         "Which fusion strategy produces fairer outcomes across demographic groups?",
         "Measured via Demographic Parity Gap and Equal Opportunity Gap for gender and ethnicity."),
        ("RQ3", "SBERT Contribution",
         "Can Sentence-BERT embeddings improve both fairness and predictive accuracy?",
         "Ablation: No Text (Structured Only) vs SBERT (all-MiniLM-L6-v2) on Early Fusion, RF."),
        ("RQ4", "Bias Mitigation",
         "How do lightweight bias mitigation techniques affect model performance?",
         "Three techniques: sensitive attribute removal, attribute masking (bio_anonymized), sample reweighting."),
        ("RQ5", "Accuracy–Fairness Trade-off",
         "What trade-offs exist between fairness and accuracy in multimodal recruitment systems?",
         "Scatter plot of F1 vs DP Gap across all 12 experiments to map the Pareto frontier."),
    ]

    col1, col2 = st.columns(2)
    for i, (rq_id, rq_title, rq_q, rq_note) in enumerate(rqs):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div class="rq-card">
                <div class="rq-number">{rq_id} · {rq_title}</div>
                <div class="rq-question">{rq_q}</div>
                <div class="rq-answer">{rq_note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Experimental Design Table ─────────────────────────────────────
    st.markdown('<div class="section-header">🧪 Experimental Design</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**Feature Settings (Baseline Phase)**")
        st.markdown("""
        <table class="result-table">
        <thead><tr><th>Setting</th><th>Features</th><th>Purpose</th></tr></thead>
        <tbody>
        <tr><td class="mono">A</td><td>Competency Only (8)</td><td>Merit-based baseline</td></tr>
        <tr><td class="mono">B</td><td>Competency + Demographics</td><td>Proxy bias measurement</td></tr>
        <tr><td class="mono">C</td><td>Competency + Face Emb (20d)</td><td>Face-aware model</td></tr>
        <tr><td class="mono">D</td><td>Competency + Blind Face Emb</td><td>De-biased face model</td></tr>
        </tbody></table>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("**Fusion Experiments (Main Phase)**")
        st.markdown("""
        <table class="result-table">
        <thead><tr><th>Strategy</th><th>Input Dim</th><th>Label</th></tr></thead>
        <tbody>
        <tr><td>Baseline</td><td>8 (structured)</td><td>blind_label</td></tr>
        <tr><td>Early Fusion</td><td>384 + 8 = 392</td><td>blind_label</td></tr>
        <tr><td>Late Fusion</td><td>β·P_text + (1-β)·P_struct</td><td>blind_label</td></tr>
        <tr><td>Weighted Hybrid</td><td>α·F_text + (1-α)·F_struct</td><td>blind_label</td></tr>
        </tbody></table>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Key Finding Preview ───────────────────────────────────────────
    st.markdown('<div class="section-header">🔑 Key Findings Preview</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="insight-box">
            <strong>High Accuracy Achieved</strong><br>
            All three baseline models (LR, RF, MLP) reach F1 ≥ 0.936 and AUC ≥ 0.987
            on the fair blind label — confirming FairCVdb is learnable from competency features alone.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Accuracy ≠ Fairness</strong><br>
            LR achieves the highest AUC (0.997) but also the worst
            Equality of Opportunity gap on the ethnicity-biased label (EOO=0.321),
            demonstrating that accuracy metrics can mask demographic disparities.
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="amber-box">
            <strong>Suitability Dominates</strong><br>
            Both LR (coef=10.446) and RF (Gini=0.2796) confirm Suitability as the
            most influential feature — followed by Recommendation and Language proficiency.
            Availability is consistently least important.
        </div>
        """, unsafe_allow_html=True)
