import streamlit as st
from pathlib import Path

IMG_DIR = Path(__file__).parent.parent / "data" / "images"

def img(name):
    p = IMG_DIR / name
    return str(p) if p.exists() else None

def render_fairness():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Fairness Analysis</div>
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

    st.markdown('<div class="section-header">Fairness Metrics Explained</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, (title, color, formula, gap, desc) in zip([c1,c2,c3], [
        ("Demographic Parity (DP)", "#2dd4bf",
         "P(y_hat=1|A=0) = P(y_hat=1|A=1)",
         "DP Gap = |pos_rate_g1 - pos_rate_g2|",
         "Equal positive prediction rate across groups. Gap of 0 = perfect parity."),
        ("Equal Opportunity (EOO)", "#8b5cf6",
         "P(y_hat=1|Y=1,A=0) = P(y_hat=1|Y=1,A=1)",
         "EOO Gap = |TPR_g1 - TPR_g2|",
         "Qualified candidates from all groups equally likely to be recommended."),
        ("Disparate Impact (DI)", "#f59e0b",
         "DI = min_group_rate / max_group_rate",
         "EEOC 4/5 rule: DI < 0.8 = violation",
         "Ratio of positive rates. Below 0.8 triggers EEOC four-fifths rule."),
    ]):
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
    st.markdown('<div class="section-header">Fairness Gaps — All Models x All Labels</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        Lower bars = fairer model. Each panel shows DP Gap or EOO Gap for gender (top) and ethnicity (bottom)
        across three label types. The blind label is the fair training target.
    </div>
    """, unsafe_allow_html=True)

    p = img("compare_fairness.png")
    if p: st.image(p, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Key Numbers from Chart**")
    st.markdown("""
    <table class="result-table">
    <thead><tr>
        <th>Model</th><th>Label</th>
        <th>DP Gap (Gender)</th><th>EOO Gap (Gender)</th>
        <th>DP Gap (Ethnicity)</th><th>EOO Gap (Ethnicity)</th>
    </tr></thead>
    <tbody>
    <tr><td><span class="model-badge badge-lr">LR</span></td><td>Blind</td>
        <td class="mono">0.005</td><td class="mono">0.001</td><td class="mono">0.023</td><td class="mono">0.007</td></tr>
    <tr><td><span class="model-badge badge-rf">RF</span></td><td>Blind</td>
        <td class="mono">0.011</td><td class="mono">0.004</td><td class="mono">0.022</td><td class="mono">0.004</td></tr>
    <tr><td><span class="model-badge badge-mlp">MLP</span></td><td>Blind</td>
        <td class="best-val">0.004</td><td class="best-val">0.001</td><td class="best-val">0.020</td><td class="mono">0.005</td></tr>
    <tr style="border-top:2px solid #30363d;">
    <td><span class="model-badge badge-lr">LR</span></td><td>Gender Bias</td>
        <td class="mono">0.003</td><td class="mono">0.011</td><td class="mono">0.116</td><td class="mono">0.278</td></tr>
    <tr><td><span class="model-badge badge-rf">RF</span></td><td>Gender Bias</td>
        <td class="mono">0.004</td><td class="mono">0.016</td><td class="mono">0.119</td><td class="mono">0.247</td></tr>
    <tr><td><span class="model-badge badge-mlp">MLP</span></td><td>Gender Bias</td>
        <td class="mono">0.011</td><td class="best-val">0.001</td><td class="mono">0.136</td><td class="mono">0.273</td></tr>
    <tr style="border-top:2px solid #30363d;">
    <td><span class="model-badge badge-lr">LR</span></td><td>Eth. Bias</td>
        <td class="mono">0.004</td><td class="warn-val">0.321</td><td class="mono">0.017</td><td class="mono">0.020</td></tr>
    <tr><td><span class="model-badge badge-rf">RF</span></td><td>Eth. Bias</td>
        <td class="mono">0.004</td><td class="mono">0.259</td><td class="mono">0.023</td><td class="mono">0.054</td></tr>
    <tr><td><span class="model-badge badge-mlp">MLP</span></td><td>Eth. Bias</td>
        <td class="mono">0.007</td><td class="mono">0.252</td><td class="mono">0.014</td><td class="mono">0.026</td></tr>
    </tbody></table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box" style="margin-top:1rem;">
        <strong>Accuracy does not equal Fairness:</strong>
        LR achieves the best AUC (0.997) on the blind label but produces the worst
        EOO Gap on the ethnicity-biased label (0.321) — more than 10x larger than its blind-label EOO gap (0.001).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Demographic Parity — Positive Prediction Rates</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        Demographic Parity requires all bars to be equal height.
        The red dashed line at 50% is the parity target (balanced 50/50 dataset).
    </div>
    """, unsafe_allow_html=True)
    p = img("fairness_pos_rate.png")
    if p: st.image(p, use_container_width=True)

    st.markdown("""
    <div class="green-box">
        All models predict close to 50% for both genders and all three ethnicity groups on the blind label.
        This confirms that training on the fair label with balanced data naturally produces near-fair outcomes.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Group-wise Confusion Matrices (RF, Gender Biased Label)</div>', unsafe_allow_html=True)

    p = img("fairness_group_cm.png")
    if p: st.image(p, use_container_width=True)

    st.markdown("""
    <div class="warning-box">
        Male (n=2,437): TP=843, FN=367. Female (n=2,363): TP=518, FN=24 — model recommends fewer females due to biased label.
        G3 (n=1,617): FP=375 is very high — proxy bias from correlated competency features despite label not directly targeting G3.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Fairness Summary Insights</div>', unsafe_allow_html=True)

    insights = [
        ("Blind Label produces Near-Fair outcomes",
         "All three models on blind_label produce very small fairness gaps (DP Gap < 0.023, EOO Gap < 0.007). Training on a fair label with balanced data naturally produces fair outcomes when using only competency features."),
        ("Biased Labels amplify gaps",
         "Gender-biased label: EOO Gap (Ethnicity) reaches 0.278 for LR. Ethnicity-biased label: EOO Gap (Gender) reaches 0.321 for LR. The model learns and amplifies the discrimination embedded in the training labels."),
        ("Ethnicity Bias is harder to learn",
         "Ethnicity-biased label produces lower AUC (RF: 0.888 vs 0.987 for blind). The model struggles with inconsistent penalties, causing more feature importance shift."),
        ("MLP shows best fairness on Blind Label",
         "MLP achieves the lowest DP Gap (Gender: 0.004, Ethnicity: 0.020) while maintaining competitive accuracy (F1=0.965) — best accuracy-fairness balance among baseline models."),
        ("Proxy Bias risk remains",
         "Even when gender/ethnicity are excluded (Setting A), biased labels cause models to reweight features (language skills, recommendation) that correlate with demographics."),
    ]

    for title, desc in insights:
        st.markdown(f"""
        <div class="rq-card" style="margin-bottom:0.6rem;">
            <div style="font-weight:600;margin-bottom:0.3rem;">{title}</div>
            <div style="font-size:0.85rem;color:#7d8590;line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
