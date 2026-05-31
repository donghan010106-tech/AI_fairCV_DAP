import streamlit as st


def render_dataset():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🗄️ Dataset & EDA</div>
        <p class="hero-sub">FairCVdb — 24,000 synthetic resume profiles designed for fairness-aware recruitment research.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Dataset Overview ───────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Dataset Overview</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value">24,000</div>
            <div class="kpi-label">Total Profiles</div>
            <div style="font-size:0.68rem;color:#7d8590;margin-top:0.3rem;">19,200 train / 4,800 test</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value">60</div>
            <div class="kpi-label">Total Columns</div>
            <div style="font-size:0.68rem;color:#7d8590;margin-top:0.3rem;">demographics, competency, embeddings, text, labels</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value">10</div>
            <div class="kpi-label">Occupations</div>
            <div style="font-size:0.68rem;color:#7d8590;margin-top:0.3rem;">across 4 sectors</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Column Groups ──────────────────────────────────────────────────
    st.markdown('<div class="section-header">📦 Column Groups</div>', unsafe_allow_html=True)

    groups = [
        ("Demographics", ["gender (0=Male, 1=Female)", "ethnicity (G1, G2, G3)"],
         "#f43f5e", "Sensitive attributes used only for fairness evaluation"),
        ("Occupation", ["occupation_id, occupation_name", "suitability (0.25/0.5/0.75/1.0)", "sector (Healthcare/Media/Education/Legal)"],
         "#f59e0b", "10 occupations balanced across 4 sectors"),
        ("Competency (8 features)", ["educ_attainment, prev_experience", "recommendation, availability", "lang_prof_1, lang_prof_2, lang_prof_3"],
         "#2dd4bf", "Primary inputs for all models — Setting A features"),
        ("Face Embeddings", ["face_emb_0…19 (20-dim, original)", "blind_face_emb_0…19 (20-dim, SensitiveNets)"],
         "#8b5cf6", "Settings C & D. blind_face_emb has near-zero variance"),
        ("Text", ["bio_original (with gender indicators)", "bio_anonymized (gender-neutral, used for SBERT)"],
         "#38bdf8", "SBERT encodes bio_anonymized to avoid gender proxy leakage"),
        ("Labels (3)", ["blind_label — fair score, no demographic penalty", "biased_label_gender — female penalized ~25%", "biased_label_ethnicity — G1 & G3 penalized"],
         "#22c55e", "Continuous → binary via median(blind_label) ≈ 0.413"),
    ]

    for name, items, color, note in groups:
        with st.expander(name, expanded=False):
            st.markdown(f"""
            <div style="border-left:3px solid {color}; padding-left:1rem;">
                <div style="font-size:0.8rem; color:{color}; font-style:italic; margin-bottom:0.5rem;">{note}</div>
                <ul style="margin:0; padding-left:1rem; color:#e6edf3; font-size:0.88rem; line-height:1.8;">
                {"".join(f"<li>{i}</li>" for i in items)}
                </ul>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Label System ───────────────────────────────────────────────────
    st.markdown('<div class="section-header">🏷️ Label System & Binarization</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    label_data = [
        ("blind_label", "Fair Target", "#22c55e",
         "Score based purely on competency and suitability — no demographic penalty. Used as the primary training target for all fusion experiments."),
        ("biased_label_gender", "Gender-Biased", "#f43f5e",
         "Female candidates penalized by ~25% relative to equivalent male candidates. Used to measure how models learn gender discrimination from biased data."),
        ("biased_label_ethnicity", "Ethnicity-Biased", "#f59e0b",
         "Groups G1 and G3 are penalized relative to G2. Produces the largest fairness gaps — EOO gaps up to 0.321 on LR."),
    ]
    for col, (name, label, color, desc) in zip([c1, c2, c3], label_data):
        with col:
            st.markdown(f"""
            <div class="fusion-card" style="border-top:3px solid {color};">
                <div class="fusion-title" style="color:{color};">{name}</div>
                <div style="font-size:0.78rem; color:#7d8590; margin-bottom:0.6rem;">{label}</div>
                <div style="font-size:0.85rem; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="amber-box">
        <strong>Binarization Strategy:</strong> All three continuous labels are converted to binary classification
        using the median of <code style="background:#0d1117;padding:1px 4px;border-radius:3px;">blind_label</code> as threshold (~0.413).
        This ensures a balanced 50/50 class distribution, which is required for fair F1 and AUC evaluation.
        The same threshold is applied to all three labels to ensure comparability.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Demographic Balance ────────────────────────────────────────────
    st.markdown('<div class="section-header">👥 Demographic Balance</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <strong>Design-controlled balance:</strong> FairCVdb is intentionally constructed with balanced demographics —
        ~50/50 gender split and ~33/33/33 ethnicity split (G1/G2/G3). This controlled balance enables reliable
        fairness metric computation. Any score gaps between groups therefore cannot be attributed to class imbalance,
        making them clear evidence of bias in the label or model.
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
        <table class="result-table">
        <thead><tr><th>Group</th><th>Type</th><th>Count (approx)</th><th>%</th></tr></thead>
        <tbody>
        <tr><td>Male</td><td>Gender</td><td>12,000</td><td>50%</td></tr>
        <tr><td>Female</td><td>Gender</td><td>12,000</td><td>50%</td></tr>
        <tr><td>G1</td><td>Ethnicity</td><td>8,000</td><td>33.3%</td></tr>
        <tr><td>G2</td><td>Ethnicity</td><td>8,000</td><td>33.3%</td></tr>
        <tr><td>G3</td><td>Ethnicity</td><td>8,000</td><td>33.3%</td></tr>
        </tbody></table>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <table class="result-table">
        <thead><tr><th>Sector</th><th>Occupations</th><th>Suitability Score</th></tr></thead>
        <tbody>
        <tr><td>Healthcare</td><td>Nurse, Surgeon, Physician</td><td>0.75</td></tr>
        <tr><td>Media</td><td>Journalist, Photographer, Filmmaker</td><td>0.25</td></tr>
        <tr><td>Education</td><td>Teacher, Professor</td><td>1.00</td></tr>
        <tr><td>Legal/Finance</td><td>Attorney, Accountant</td><td>0.50</td></tr>
        </tbody></table>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Competency Features ────────────────────────────────────────────
    st.markdown('<div class="section-header">📐 Competency Features (Setting A)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">
        The 8 competency features form Setting A — the merit-based baseline. All are numerical scores,
        scaled via StandardScaler (fit on training set only to prevent data leakage).
        These features are the sole inputs for the fair blind label training and are consistently
        used as the structured component in all fusion architectures.
    </div>
    """, unsafe_allow_html=True)

    feats = [
        ("suitability", "Job-category match score (0.25/0.5/0.75/1.0)", "Encodes sector fit — directly linked to blind_label"),
        ("educ_attainment", "Education level score", "Numerical, normalized"),
        ("prev_experience", "Prior work experience score", ""),
        ("recommendation", "Recommendation letter quality score", ""),
        ("availability", "Candidate availability score", "Lowest importance in both LR and RF"),
        ("lang_prof_1/2/3", "Three language proficiency scores", "All three carry similar, high weight in LR (coef ~6.3)"),
    ]
    st.markdown("""
    <table class="result-table">
    <thead><tr><th>Feature</th><th>Description</th><th>Note</th></tr></thead>
    <tbody>
    """ + "".join(f"<tr><td class='mono'>{n}</td><td>{d}</td><td style='color:#7d8590;font-size:0.8rem;'>{note}</td></tr>" for n, d, note in feats) + """
    </tbody></table>
    """, unsafe_allow_html=True)
