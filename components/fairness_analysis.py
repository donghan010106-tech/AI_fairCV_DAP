import streamlit as st
from pathlib import Path

IMG_DIR = Path(__file__).parent.parent / "data" / "images"


def img(name: str):
    p = IMG_DIR / name
    return str(p) if p.exists() else None


def render_fairness():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">⚖️ Fairness Analysis</div>
        <p class="hero-sub">
            Demographic Parity, Equality of Opportunity, and Disparate Impact analysis
            across gender and ethnicity groups — for all models trained on all three label types.
        </p>
        <div style="margin-top:0.8rem;">
            <span class="tag tag-teal">Demographic Parity</span>
            <span class="tag tag-violet">Equal Opportunity</span>
            <span class="tag tag-rose">Disparate Impact</span>
            <span class="tag tag-amber">Gender · Ethnicity</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric Explainer ──────────────────────────────────────────────
    st.markdown('<div class="section-header">📐 Fairness Metrics Explained</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    metrics_info = [
        ("Demographic Parity (DP)", "#2dd4bf",
         "P(ŷ=1 | A=0) = P(ŷ=1 | A=1)",
         "DP Gap = |pos_rate_group1 - pos_rate_group2|",
         "Measures whether the positive prediction rate is equal across groups. A gap of 0 = perfect parity. Sensitive to class imbalance."),
        ("Equal Opportunity (EOO)", "#8b5cf6",
         "P(ŷ=1|Y=1, A=0) = P(ŷ=1|Y=1, A=1)",
         "EOO Gap = |TPR_group1 - TPR_group2|",
         "Measures whether qualified candidates from all groups are equally likely to be recommended. Focuses only on true positives."),
        ("Disparate Impact (DI)", "#f59e0b",
         "DI = min_group_rate / max_group_rate",
         "EEOC 4/5 rule: DI < 0.8 = violation",
         "Ratio of positive rates between groups. Below 0.8 triggers the EEOC four-fifths rule — legal standard for hiring discrimination."),
    ]
    for col, (title, color, formula, gap, desc) in zip([c1, c2, c3], metrics_info):
        with col:
            st.markdown(f"""
            <div class="fusion-card" style="border-top:3px solid {color};">
                <div style="font-family:'Space Mono',monospace;font-size:0.85rem;font-weight:700;color:{color};margin-bottom:0.5rem;">{title}</div>
                <div style="background:#0d1117;border-radius:6px;padding:0.4rem 0.8rem;font-family:'Space Mono',monospace;font-size:0.72rem;color:#f59e0b;margin-bottom:0.4rem;">{formula}</div>
                <div style="background:#1c2128;border-radius:6px;padding:0.4rem 0.8rem;font-family:'Space Mono',monospace;font-size:0.72rem;color:#7d8590;margin-bottom:0.6rem;">{gap}</div>
                <div style="font-size:0.8rem;color:#7d8590;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Fairness Gaps All Models ───────────────────────────────────────
    st.markdown('<div class="section-header">📊 Fairness Gaps — All Models × All Labels</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <strong>Reading the chart:</strong> Lower bars = fairer model. Each panel shows DP Gap or EOO Gap
        for gender (top) and ethnicity (bottom) across three label types (Blind/Gender Bias/Ethnicity Bias).
        The blind label represents the fair training target; biased labels show how models amplify discrimination.
    </div>
    """, unsafe_allow_html=True)

    p = img("compare_fairness.png")
    if p:
        st.image(p, use_container_width=True)

    # Key numbers extracted from the image
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Key Numbers Extracted from Chart**")

    st.markdown("""
    <table class="result-table">
    <thead>
        <tr>
            <th>Model</th>
            <th>Label</th>
            <th>DP Gap (Gender)</th>
            <th>EOO Gap (Gender)</th>
            <th>DP Gap (Ethnicity)</th>
            <th>EOO Gap (Ethnicity)</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><span class="model-badge badge-lr">LR</span></td><td>Blind</td>
            <td class="mono">0.005</td><td class="mono">0.001</td>
            <td class="mono">0.023</td><td class="mono">0.007</td></tr>
        <tr><td><span class="model-badge badge-rf">RF</span></td><td>Blind</td>
            <td class="mono">0.011</td><td class="mono">0.004</td>
            <td class="mono">0.022</td><td class="mono">0.004</td></tr>
        <tr><td><span class="model-badge badge-mlp">MLP</span></td><td>Blind</td>
            <td class="best-val">0.004</td><td class="best-val">0.001</td>
            <td class="best-val">0.020</td><td class="mono">0.005</td></tr>
        <tr style="border-top:2px solid #30363d;">
            <td><span class="model-badge badge-lr">LR</span></td><td>Gender Bias</td>
            <td class="mono">0.003</td><td class="mono">0.011</td>
            <td class="mono">0.116</td><td class="mono">0.278</td></tr>
        <tr><td><span class="model-badge badge-rf">RF</span></td><td>Gender Bias</td>
            <td class="mono">0.004</td><td class="mono">0.016</td>
            <td class="mono">0.119</td><td class="mono">0.247</td></tr>
        <tr><td><span class="model-badge badge-mlp">MLP</span></td><td>Gender Bias</td>
            <td class="mono">0.011</td><td class="best-val">0.001</td>
            <td class="mono">0.136</td><td class="best-val">0.273</td></tr>
        <tr style="border-top:2px solid #30363d;">
            <td><span class="model-badge badge-lr">LR</span></td><td>Eth. Bias</td>
            <td class="mono">0.004</td><td class="mono">0.321</td>
            <td class="mono">0.017</td><td class="mono">0.020</td></tr>
        <tr><td><span class="model-badge badge-rf">RF</span></td><td>Eth. Bias</td>
            <td class="mono">0.004</td><td class="mono">0.259</td>
            <td class="mono">0.023</td><td class="mono">0.054</td></tr>
        <tr><td><span class="model-badge badge-mlp">MLP</span></td><td>Eth. Bias</td>
            <td class="mono">0.007</td><td class="warn-val">0.252</td>
            <td class="mono">0.014</td><td class="mono">0.026</td></tr>
    </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box" style="margin-top:1rem;">
        <strong>⚠️ Critical finding — Accuracy ≠ Fairness:</strong>
        LR achieves the best AUC (0.997) on the blind label but produces the worst
        EOO Gap on the ethnicity-biased label (0.321) — more than 10× larger than its blind-label EOO gap (0.001).
        This dramatic difference demonstrates that high accuracy metrics can completely mask
        discriminatory behavior when label bias is present.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Positive Prediction Rate ───────────────────────────────────────
    st.markdown('<div class="section-header">📈 Demographic Parity — Positive Prediction Rates</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <strong>Demographic Parity requires all bars to be equal height.</strong>
        The red dashed line at 50% is the parity target (since the dataset is balanced 50/50).
        Bars near 50% and close together indicate fair treatment;
        bars far apart indicate demographic parity violation.
    </div>
    """, unsafe_allow_html=True)

    p = img("fairness_pos_rate.png")
    if p:
        st.image(p, use_container_width=True)

    st.markdown("""
    <div class="green-box">
        <strong>Blind label result:</strong> All models predict close to 50% for both genders and all three ethnicity groups.
        The largest gap is RF on gender (0.499 Male vs 0.488 Female = 0.011).
        This confirms that <em>when trained on the fair label</em>, competency-only models are naturally near-fair
        because the dataset is designed to be balanced and the fair label does not encode demographic penalties.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Group-wise Confusion Matrices ─────────────────────────────────
    st.markdown('<div class="section-header">🔍 Group-wise Confusion Matrices (RF, Gender Biased Label)</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <strong>Why RF on gender-biased label?</strong> This combination reveals how a model trained on
        gender-discriminatory data performs differently for male vs female candidates —
        and how ethnicity groups are affected despite the label not targeting ethnicity directly (proxy bias).
    </div>
    """, unsafe_allow_html=True)

    p = img("fairness_group_cm.png")
    if p:
        st.image(p, use_container_width=True)

    st.markdown("""
    <div class="warning-box">
        <strong>Group-wise disparities:</strong>
        Male candidates (n=2,437): TP=843, FN=367 — positive rate driven by biased label.
        Female candidates (n=2,363): TP=518, FN=24 — fewer true positives in biased label → model recommends fewer females.
        G2 (n=1,588): high TN=709, strong classification.
        G3 (n=1,617): FP=375 is very high — model over-recommends G3 despite bias not directly targeting them,
        suggesting proxy effects from correlated competency features.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Summary Insights ──────────────────────────────────────────────
    st.markdown('<div class="section-header">💡 Fairness Summary Insights</div>', unsafe_allow_html=True)

    insights = [
        ("🟢", "Blind Label → Near-Fair",
         "All three models on blind_label produce very small fairness gaps (DP Gap < 0.023, EOO Gap < 0.007). Training on a fair label with balanced data naturally produces fair outcomes when using only competency features."),
        ("🔴", "Biased Labels → Amplified Gaps",
         "Gender-biased label: EOO Gap (Ethnicity) reaches up to 0.278 for LR. Ethnicity-biased label: EOO Gap (Gender) reaches 0.321 for LR. The model effectively learns and amplifies the discrimination embedded in the training labels."),
        ("🟡", "Ethnicity Bias Is Harder to Learn",
         "Ethnicity-biased label produces lower AUC (RF: 0.888 vs 0.987 for blind) — the model struggles because G1 and G3 are penalized inconsistently relative to competency. This also means ethnicity bias causes more feature importance shift."),
        ("🔵", "MLP Shows Best Fairness on Blind Label",
         "MLP achieves the lowest DP Gap (Gender: 0.004, Ethnicity: 0.020) while maintaining competitive accuracy (F1=0.965). It represents the best accuracy–fairness balance among baseline models."),
        ("⚪", "Proxy Bias Risk",
         "Even when gender/ethnicity are excluded from features (Setting A), biased labels cause models to reweight other features (language skills, recommendation) that correlate with demographics — a classic proxy bias mechanism."),
    ]

    for emoji, title, desc in insights:
        st.markdown(f"""
        <div class="rq-card" style="margin-bottom:0.6rem;">
            <div style="display:flex;gap:0.8rem;align-items:flex-start;">
                <div style="font-size:1.2rem;flex-shrink:0;">{emoji}</div>
                <div>
                    <div style="font-weight:600;margin-bottom:0.3rem;">{title}</div>
                    <div style="font-size:0.85rem;color:#7d8590;line-height:1.5;">{desc}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
