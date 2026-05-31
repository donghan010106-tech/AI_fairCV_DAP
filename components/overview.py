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

    st.markdown("""
    <div style="background:#161b22; border:1px solid #30363d; border-radius:12px; padding:1.5rem 2rem; overflow-x:auto;">
        <div style="display:flex; align-items:center; gap:0; min-width:700px; justify-content:center;">

            <div style="text-align:center; flex:1;">
                <div style="background:#1c2128; border:1px solid #30363d; border-radius:10px; padding:0.8rem 0.5rem;">
                    <div style="font-size:1.4rem; margin-bottom:4px;">📂</div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#2dd4bf; font-weight:700;">FairCVdb</div>
                    <div style="font-size:0.65rem; color:#7d8590; margin-top:2px;">24,000 profiles<br>60 columns</div>
                </div>
            </div>

            <div style="color:#30363d; font-size:1.2rem; padding:0 0.3rem; flex:0;">→</div>

            <div style="text-align:center; flex:1;">
                <div style="background:#1c2128; border:1px solid #30363d; border-radius:10px; padding:0.8rem 0.5rem;">
                    <div style="font-size:1.4rem; margin-bottom:4px;">🧹</div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#f59e0b; font-weight:700;">Preprocessing</div>
                    <div style="font-size:0.65rem; color:#7d8590; margin-top:2px;">Binarize labels<br>4 feature settings</div>
                </div>
            </div>

            <div style="color:#30363d; font-size:1.2rem; padding:0 0.3rem; flex:0;">→</div>

            <div style="text-align:center; flex:1;">
                <div style="background:#1c2128; border:1px solid #30363d; border-radius:10px; padding:0.8rem 0.5rem;">
                    <div style="font-size:1.4rem; margin-bottom:4px;">🤖</div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#8b5cf6; font-weight:700;">SBERT Encoding</div>
                    <div style="font-size:0.65rem; color:#7d8590; margin-top:2px;">all-MiniLM-L6-v2<br>bio_anonymized → 384d</div>
                </div>
            </div>

            <div style="color:#30363d; font-size:1.2rem; padding:0 0.3rem; flex:0;">→</div>

            <div style="text-align:center; flex:1;">
                <div style="background:#1c2128; border:1px solid #30363d; border-radius:10px; padding:0.8rem 0.5rem;">
                    <div style="font-size:1.4rem; margin-bottom:4px;">🔀</div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#38bdf8; font-weight:700;">Fusion</div>
                    <div style="font-size:0.65rem; color:#7d8590; margin-top:2px;">Early / Late<br>Hybrid</div>
                </div>
            </div>

            <div style="color:#30363d; font-size:1.2rem; padding:0 0.3rem; flex:0;">→</div>

            <div style="text-align:center; flex:1;">
                <div style="background:#1c2128; border:1px solid #30363d; border-radius:10px; padding:0.8rem 0.5rem;">
                    <div style="font-size:1.4rem; margin-bottom:4px;">📊</div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#22c55e; font-weight:700;">Evaluation</div>
                    <div style="font-size:0.65rem; color:#7d8590; margin-top:2px;">F1 · AUC<br>DP · EOO · DI</div>
                </div>
            </div>

            <div style="color:#30363d; font-size:1.2rem; padding:0 0.3rem; flex:0;">→</div>

            <div style="text-align:center; flex:1;">
                <div style="background:#1c2128; border:1px solid #30363d; border-radius:10px; padding:0.8rem 0.5rem;">
                    <div style="font-size:1.4rem; margin-bottom:4px;">⚖️</div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#f43f5e; font-weight:700;">Fairness Audit</div>
                    <div style="font-size:0.65rem; color:#7d8590; margin-top:2px;">Gender · Ethnicity<br>Bias Mitigation</div>
                </div>
            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)

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
