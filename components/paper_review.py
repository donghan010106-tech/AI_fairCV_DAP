"""Research Paper Integration page."""

import streamlit as st
import plotly.graph_objects as go


PAPERS = [
    {
        "id": "P1",
        "title": "Human-Centric Multimodal Machine Learning: Recent Advances and Testbed on AI-Based Recruitment",
        "authors": "Peña, Serna, Morales, Fierrez, Ortega et al. (UAM)",
        "venue": "SN Computer Science, vol. 4:434, 2023",
        "doi": "10.1007/s42979-023-01733-0",
        "color": "#2dd4bf",
        "badge": "badge-lr",
        "summary": (
            "The foundational paper for this project. Introduces <strong>FairCVdb</strong> — "
            "24,000 synthetic resume profiles with image, text, and tabular data, plus intentional "
            "gender/ethnicity biases. Proposes the <strong>FairCVtest</strong> framework: a multimodal "
            "neural network (ResNet-50 for faces + BiLSTM for text + FC for tabular) trained under "
            "Neutral, Biased, and Agnostic scenarios. Uses SensitiveNets to remove demographic information "
            "from face embeddings. Evaluates with KL divergence and demographic parity."
        ),
        "key_ideas": [
            "FairCVdb: first public dataset with image + text + tabular for fairness research in hiring",
            "Bias enters through target function (labels), not just training data imbalance",
            "Agnostic scenario (SensitiveNets + blinded bios) reduces gender KL from 0.320 → 0.026",
            "Even without explicit demographics, models learn proxy patterns from face embeddings",
            "Human-centric AI requires 4 pillars: utility, privacy, transparency, fairness",
        ],
        "applicability": [
            "Our project uses FairCVdb directly — all our experiments are a subset of this framework",
            "We replicate Setting A (competency-only) with classical ML instead of deep learning",
            "The multimodal architecture (ResNet + BiLSTM) is our primary deep-learning upgrade target",
            "SensitiveNets can be applied to face embeddings in Settings C/D to test agnostic scenario",
            "Demographic parity and p% score are our gold-standard fairness benchmarks",
        ],
        "gap": "Our project only uses classical ML on tabular features. The full multimodal pipeline remains as future work.",
    },
    {
        "id": "P2",
        "title": "Exploring Fusion Techniques in Multimodal AI-Based Recruitment: Insights from FairCVdb",
        "authors": "Swati Swati, Arjun Roy, Eirini Ntoutsi (University of Bundeswehr Munich)",
        "venue": "EWAF'24: European Workshop on Algorithmic Fairness, July 2024",
        "doi": "arXiv:2407.16892",
        "color": "#8b5cf6",
        "badge": "badge-violet",
        "summary": (
            "Extends FairCVtest by adding <strong>early-fusion and late-fusion</strong> strategies "
            "to compare against individual modalities (tabular, textual, visual). Uses MAE and "
            "KL-divergence to measure accuracy and demographic bias. Key finding: "
            "<strong>early-fusion achieves lowest MAE</strong> while closely tracking ground-truth "
            "score distributions. Late-fusion over-generalizes (higher MAE) due to averaging across "
            "modalities, especially being dragged by the visual modality's narrow score concentration."
        ),
        "key_ideas": [
            "Early-fusion (concatenate all modalities early) = lowest MAE + best fairness tracking",
            "Late-fusion (combine modality outputs at end) = over-generalized mean, higher MAE",
            "Visual modality alone over-concentrates scores in [0.39–0.44] — extreme over-generalization",
            "Textual modality shows bimodal distribution — effectively separates high/low candidates",
            "Tabular modality consistently underestimates scores (negatively skewed distribution)",
            "Mid-fusion strategies (future work) may balance accuracy and fairness",
        ],
        "applicability": [
            "Motivates implementing early-fusion in our Settings C/D (when face embeddings are added)",
            "Confirms tabular-only approach (Setting A) is a valid baseline — tabular is well-calibrated",
            "MAE as complementary metric to our binary F1/AUC — relevant if we switch to regression task",
            "Late-fusion failure explains why naive concatenation of face embeddings hurts RF in our experiments",
            "Mid-fusion: select top-performing modalities rather than blindly combining all",
        ],
        "gap": "This paper uses regression; our project uses binary classification. Results partially transfer but threshold choice matters.",
    },
    {
        "id": "P3",
        "title": "FAIRE: Assessing Racial and Gender Bias in AI-Driven Resume Evaluations",
        "authors": "Athena Wen, Tanush Patil, Ansh Saxena, Yicheng Fu, Sean O'Brien, Kevin Zhu (Algoverse AI Research)",
        "venue": "arXiv:2504.01420, April 2025",
        "doi": "arXiv:2504.01420",
        "color": "#f59e0b",
        "badge": "badge-mlp",
        "summary": (
            "Introduces the <strong>FAIRE benchmark</strong> for evaluating racial and gender bias "
            "in LLM-based resume screening (GPT-4o, GPT-4o-mini, Claude 3.5 Sonnet/Haiku, Llama 3.3 70B). "
            "Two methods: <strong>Direct Scoring</strong> (LLM scores each resume on 5 dimensions) and "
            "<strong>Ranking</strong> (LLM ranks 5 resumes head-to-head). Tests perturbations: "
            "racially suggestive names and explicit racial experience descriptions. "
            "Finding: GPT-4o strongly favors Asian resumes (+0.29 bias gap); Llama 3.3 70B shows "
            "largest overall bias (-0.36 for Asian). Claude 3.5 Haiku is most balanced."
        ),
        "key_ideas": [
            "LLM bias in hiring is real and measurable via controlled name/experience perturbations",
            "Cultural Fit dimension shows highest bias gap (subjective = more biased)",
            "GPT-4o favors Asian resumes (+0.80 cultural fit gap); Llama severely penalizes them (-0.50)",
            "Ranking task reveals more extreme bias than direct scoring (comparison amplifies stereotypes)",
            "Claude 3.5 Haiku is the most consistent and least biased model tested",
            "Gender bias: most models rate female candidates slightly lower overall",
        ],
        "applicability": [
            "Motivates using LLMs as a scoring upgrade over our classical ML baseline",
            "FAIRE methodology (name perturbation + score comparison) can validate our model's fairness",
            "Suggests Claude Haiku as a fair LLM-based scoring layer for our pipeline",
            "The 5-dimension scoring rubric (Relevance, Skill, Achievement, Cultural Fit, Impact) is a richer output than binary classification",
            "Reveals that LLM-based scoring still has significant bias — our classical approach is simpler but more auditable",
        ],
        "gap": "FAIRE uses real resumes; FairCVdb is synthetic. LLM scoring is expensive; our approach is efficient at scale.",
    },
]


def render_papers():
    st.markdown("""
    <div class="hero-banner" style="padding:1.8rem 2.5rem;">
        <div class="hero-title" style="font-size:1.7rem;">📚 Research Paper Integration</div>
        <p class="hero-sub">Three peer-reviewed papers ground this project in current fairness-in-AI research. 
        Each paper is analyzed for direct applicability to our pipeline.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick comparison matrix ─────────────────────────────────────────────
    st.markdown('<div class="section-header">🗺️ Paper Landscape Overview</div>', unsafe_allow_html=True)
    _render_comparison_matrix()

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Individual paper cards ─────────────────────────────────────────────
    st.markdown('<div class="section-header">📄 Paper Deep-Dives</div>', unsafe_allow_html=True)

    for paper in PAPERS:
        _render_paper_card(paper)

    # ── Cross-paper synthesis ──────────────────────────────────────────────
    st.markdown('<div class="section-header">🔗 Cross-Paper Synthesis</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### What the Papers Agree On")
        agreements = [
            "Bias in AI hiring systems is real, measurable, and consequential",
            "Demographic information (direct or proxy) leaks into model decisions",
            "High accuracy ≠ fairness — separate metrics required",
            "Tabular competency features are the 'fairest' input modality",
            "Ethnicity bias is harder to remove than gender bias",
            "Explainability and transparency are ethical requirements, not optional",
        ]
        for a in agreements:
            st.markdown(f"""
            <div style="display:flex; align-items:flex-start; gap:8px; margin-bottom:6px;">
                <span style="color:#22c55e; flex-shrink:0;">✅</span>
                <span style="font-size:0.88rem; color:#e6edf3;">{a}</span>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        st.markdown("#### Gaps / Open Questions for Our Project")
        gaps = [
            ("P1 → Our work", "Full multimodal pipeline (ResNet + BiLSTM) not yet implemented"),
            ("P2 → Our work", "Fusion strategies (early/late) not yet tested with our models"),
            ("P3 → Our work", "LLM-based scoring layer not yet compared against our ML models"),
            ("All papers", "No fairness mitigation applied yet — only measurement done"),
            ("All papers", "No formal test set — all evaluation is on validation split"),
            ("P1 + P2", "Regression formulation not explored — only binary classification"),
        ]
        for src, detail in gaps:
            st.markdown(f"""
            <div class="warning-box" style="margin-bottom:4px;">
                <strong style="font-size:0.78rem; color:#f59e0b;">{src}:</strong>
                <span style="font-size:0.82rem;"> {detail}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Research roadmap derived from papers ──────────────────────────────
    st.markdown('<div class="section-header">🗺️ Research Directions from Papers</div>', unsafe_allow_html=True)

    directions = [
        ("📐 From P1", "#2dd4bf", "Implement SensitiveNets",
         "Apply adversarial regularizer to remove gender/ethnicity info from face embeddings (Settings C/D)"),
        ("🔀 From P2", "#8b5cf6", "Early-Fusion Multimodal",
         "Concatenate [competency + face + text] features early → train single classifier on combined representation"),
        ("🤖 From P3", "#f59e0b", "LLM Scoring Layer",
         "Add Claude Haiku as a scoring API → compare against our LR baseline on same candidates"),
        ("📊 From All", "#22c55e", "Fairness Mitigation",
         "Apply Reweighing (pre-process), Adversarial Debiasing (in-process), Threshold Calibration (post-process)"),
        ("🔬 From P1+P2", "#38bdf8", "Regression Formulation",
         "Switch from binary classification to score regression → use MAE + KL divergence as P1/P2 do"),
    ]

    for icon_src, color, title, detail in directions:
        st.markdown(f"""
        <div class="roadmap-card" style="border-left: 4px solid {color};">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
                <span style="font-size:0.72rem; color:{color}; text-transform:uppercase; letter-spacing:1px;">{icon_src}</span>
                <strong style="color:{color}; font-family:'Space Mono',monospace; font-size:0.9rem;">{title}</strong>
            </div>
            <div style="font-size:0.85rem; color:#7d8590;">{detail}</div>
        </div>
        """, unsafe_allow_html=True)


def _render_comparison_matrix():
    categories = ["Dataset", "Task", "Modalities", "Models", "Fairness Metric", "Key Finding"]
    p1 = ["FairCVdb (24K)", "Regression + Classification", "Image + Text + Tabular",
          "ResNet + BiLSTM + FC", "KL Div + Demo. Parity", "Agnostic face embeddings fix fairness"]
    p2 = ["FairCVdb (24K)", "Regression (score prediction)", "Image + Text + Tabular",
          "Early & Late Fusion NNs", "MAE + KL Divergence", "Early-fusion best accuracy & fairness"]
    p3 = ["Real resumes (Kaggle)", "LLM Scoring/Ranking", "Text only",
          "GPT-4o/mini, Claude, Llama", "Score gap + rank bias", "Claude Haiku fairest; GPT-4o Asian bias"]

    data = [categories, p1, p2, p3]
    header_labels = ["Dimension", "P1: Peña 2023", "P2: Swati 2024", "P3: FAIRE 2025"]
    colors_header = ["#30363d", "#1c3a4a", "#271d45", "#3a2d14"]
    colors_body   = [["#161b22"]*6, ["#0d1f2d"]*6, ["#1a1528"]*6, ["#201a0e"]*6]

    fig = go.Figure(go.Table(
        header=dict(
            values=[f"<b>{h}</b>" for h in header_labels],
            fill_color=["#30363d", "#1a3a4a", "#2a1e4a", "#3a2c10"],
            font=dict(color=["#e6edf3", "#2dd4bf", "#8b5cf6", "#f59e0b"], size=11, family="Space Mono"),
            align="left", height=32,
        ),
        cells=dict(
            values=data,
            fill_color=[["#161b22"]*6, ["#0d1f2d"]*6, ["#1a1528"]*6, ["#201a0e"]*6],
            font=dict(color=["#7d8590", "#e6edf3", "#e6edf3", "#e6edf3"], size=10),
            align="left", height=28,
        ),
    ))
    fig.update_layout(height=260, margin=dict(l=0, r=0, t=0, b=0),
                      paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_paper_card(paper: dict):
    with st.expander(f"[{paper['id']}] {paper['title']}", expanded=False):
        c1, c2 = st.columns([1.8, 1])

        with c1:
            st.markdown(f"""
            <div class="paper-meta">
                <strong>{paper['authors']}</strong><br/>
                {paper['venue']} · <code style="color:{paper['color']};">{paper['doi']}</code>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="insight-box">
                <strong>Abstract Summary:</strong><br/>
                {paper['summary']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**🔑 Key Ideas:**")
            for idea in paper["key_ideas"]:
                st.markdown(f'<div style="display:flex;gap:8px;margin-bottom:4px;"><span style="color:{paper["color"]};flex-shrink:0;">▸</span><span style="font-size:0.86rem;">{idea}</span></div>', unsafe_allow_html=True)

        with c2:
            st.markdown(f"**🔗 Applicability to Our Project:**")
            for app in paper["applicability"]:
                st.markdown(f"""
                <div style="background:rgba(0,0,0,0.2); border-left:2px solid {paper['color']}; 
                     padding:4px 8px; margin-bottom:4px; font-size:0.82rem; border-radius:0 4px 4px 0;">
                     {app}
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="amber-box" style="margin-top:0.6rem;">
                <strong>⚠️ Gap / Limitation:</strong><br/>
                <span style="font-size:0.82rem;">{paper['gap']}</span>
            </div>
            """, unsafe_allow_html=True)
