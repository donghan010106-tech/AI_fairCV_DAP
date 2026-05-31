import streamlit as st


def render_research():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">📚 Research Context</div>
        <p class="hero-sub">
            Three key papers informing the FairCV research framework — covering the dataset,
            fusion methodology, and LLM bias benchmarking.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Paper 1 ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📄 Paper 1 — Dataset & Problem Foundation</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="paper-card">
        <div class="paper-title">Human-Centric Multimodal Machine Learning: Recent Advances and Testbed on AI-Based Recruitment</div>
        <div class="paper-meta">Peña A, Serna I, Morales A, Fierrez J, et al. · SN Computer Science, Vol. 4, n. 434, 2023 · Springer Nature</div>
        <div style="font-size:0.88rem;line-height:1.7;color:#e6edf3;">
            <strong style="color:#38bdf8;">What it is:</strong> The source paper for FairCVdb — introduces the dataset and the FairCVtest benchmark framework
            for evaluating human-centric fairness in AI-based recruitment systems.<br><br>
            <strong style="color:#38bdf8;">Key contributions:</strong><br>
            • 24,000 synthetic resume profiles with controlled demographic balance and multiple label types<br>
            • Three label conditions: blind (fair), gender-biased, ethnicity-biased — enabling controlled bias experiments<br>
            • Face embeddings (original and SensitiveNets-anonymized) as a multimodal component<br>
            • Establishes the 80/20 train/test split (19,200 / 4,800) used in our experiments<br><br>
            <strong style="color:#38bdf8;">How it informs our work:</strong> Defines all feature settings (A/B/C/D), label binarization strategy,
            and the demographic evaluation framework. Our baseline experiments directly replicate their setup.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔗 Citation"):
        st.code("""Peña A, Serna I, Morales A, Fierrez J, et al.
Human-Centric Multimodal Machine Learning: Recent Advances and Testbed on AI-Based Recruitment.
SN Computer Science 4:434 (2023).
https://doi.org/10.1007/s42979-023-01733-0""", language="text")

    # ── Paper 2 ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📄 Paper 2 — Fusion Methodology</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="paper-card">
        <div class="paper-title">Exploring Fusion Techniques in Multimodal AI-Based Recruitment: Insights from FairCVdb</div>
        <div class="paper-meta">Swati S, Roy A, Ntoutsi E · Proceedings of the European Workshop on Algorithmic Fairness (EWAF'24), 2024</div>
        <div style="font-size:0.88rem;line-height:1.7;color:#e6edf3;">
            <strong style="color:#f43f5e;">What it is:</strong> The primary related work for our fusion comparison study.
            Investigates multimodal fusion methods using FairCVdb, analyzing how different fusion strategies
            affect recruitment prediction performance.<br><br>
            <strong style="color:#f43f5e;">Key contributions:</strong><br>
            • Systematic comparison of Early Fusion and Late Fusion on FairCVdb<br>
            • Demonstrates that fusion strategy choice meaningfully impacts both accuracy and fairness<br>
            • Identifies limitations: fairness evaluation in the original paper remains relatively limited<br><br>
            <strong style="color:#f43f5e;">How it informs our work:</strong> Directly motivates our research gap.
            We extend their work by (1) adding Weighted Hybrid Fusion, (2) incorporating SBERT text embeddings
            (they used simpler text representations), (3) adding Disparate Impact as a third fairness metric,
            and (4) structuring the evaluation around 5 explicit Research Questions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔗 Citation"):
        st.code("""Swati S, Roy A, Ntoutsi E.
Exploring Fusion Techniques in Multimodal AI-Based Recruitment: Insights from FairCVdb.
In: Proceedings of the European Workshop on Algorithmic Fairness (EWAF'24), 2024.""", language="text")

    # ── Paper 3 ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📄 Paper 3 — LLM Bias Benchmarking</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="paper-card">
        <div class="paper-title">FAIRE: Assessing Racial and Gender Bias in AI-Driven Resume Evaluations</div>
        <div class="paper-meta">Wen et al. · arXiv:2504.01420, 2025</div>
        <div style="font-size:0.88rem;line-height:1.7;color:#e6edf3;">
            <strong style="color:#22c55e;">What it is:</strong> A benchmark for evaluating demographic bias in AI-based resume screening,
            specifically targeting LLM-based evaluation systems using counterfactual resume pairs.<br><br>
            <strong style="color:#22c55e;">Key contributions:</strong><br>
            • Counterfactual fairness evaluation: modifies demographic indicators (names, pronouns) while keeping qualifications identical<br>
            • Reveals racial and gender bias in state-of-the-art LLMs when used for resume evaluation<br>
            • Provides an independent benchmark dataset complementary to FairCVdb<br><br>
            <strong style="color:#22c55e;">How it informs our work:</strong> Contextualizes our findings within the broader trend of bias in AI hiring.
            Our structured-feature approach (competency scores) is less susceptible to name-based bias than LLM evaluation,
            but text embedding via SBERT introduces similar counterfactual risks.
            FAIRE motivates using bio_anonymized (attribute masking) as Technique 2 in our bias mitigation experiments (RQ4).
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔗 Citation"):
        st.code("""Wen et al.
FAIRE: Assessing Racial and Gender Bias in AI-Driven Resume Evaluations.
arXiv:2504.01420, 2025.""", language="text")

    # ── Cross-Paper Synthesis ─────────────────────────────────────────
    st.markdown('<div class="section-header">🔗 Cross-Paper Synthesis</div>', unsafe_allow_html=True)

    st.markdown("""
    <table class="result-table">
    <thead>
        <tr>
            <th>Aspect</th>
            <th>Peña et al. (2023)</th>
            <th>Swati et al. (2024)</th>
            <th>Wen et al. (2025)</th>
            <th>Our Work</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Dataset</td>
            <td>FairCVdb (introduced)</td>
            <td>FairCVdb</td>
            <td>FAIRE benchmark</td>
            <td>FairCVdb</td>
        </tr>
        <tr>
            <td>Text Encoding</td>
            <td>None / image features</td>
            <td>Basic text features</td>
            <td>LLM prompting</td>
            <td>SBERT (all-MiniLM-L6-v2)</td>
        </tr>
        <tr>
            <td>Fusion</td>
            <td>Feature concatenation</td>
            <td>Early + Late</td>
            <td>N/A (LLM-based)</td>
            <td>Early + Late + Hybrid</td>
        </tr>
        <tr>
            <td>Fairness Metrics</td>
            <td>DP, EOO</td>
            <td>Limited</td>
            <td>Counterfactual fairness</td>
            <td>DP + EOO + Disparate Impact</td>
        </tr>
        <tr>
            <td>Bias Mitigation</td>
            <td>SensitiveNets face anonymization</td>
            <td>Not addressed</td>
            <td>Not addressed</td>
            <td>3 lightweight techniques (RQ4)</td>
        </tr>
        <tr>
            <td>Research Questions</td>
            <td>None explicit</td>
            <td>Informal</td>
            <td>Bias detection only</td>
            <td>5 explicit RQs (RQ1–RQ5)</td>
        </tr>
    </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box" style="margin-top:1.2rem;">
        <strong>Research gap addressed:</strong> No prior work systematically compares Early, Late, AND Weighted Hybrid Fusion
        on FairCVdb using SBERT text embeddings with explicit fairness-aware evaluation across 5 Research Questions
        and lightweight bias mitigation. Our study fills this gap with a reproducible, undergraduate-accessible framework.
    </div>
    """, unsafe_allow_html=True)
