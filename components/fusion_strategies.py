import streamlit as st
from pathlib import Path

IMG_DIR = Path(__file__).parent.parent / "data" / "images"


def img(name: str):
    p = IMG_DIR / name
    return str(p) if p.exists() else None


def render_fusion():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🔀 Fusion Strategies</div>
        <p class="hero-sub">
            Comparing Early, Late, and Weighted Hybrid Fusion using Sentence-BERT embeddings
            on FairCVdb — addressing RQ1 through RQ5 of the research proposal.
        </p>
        <div style="margin-top:0.8rem;">
            <span class="tag tag-violet">Sentence-BERT</span>
            <span class="tag tag-sky">Early Fusion</span>
            <span class="tag tag-rose">Late Fusion</span>
            <span class="tag tag-green">Weighted Hybrid</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SBERT Explainer ───────────────────────────────────────────────
    st.markdown('<div class="section-header">🤖 Sentence-BERT Text Encoding</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    sbert_info = [
        ("Model", "all-MiniLM-L6-v2", "#8b5cf6",
         "Lightweight transformer, 22M parameters. Fast CPU-compatible inference."),
        ("Input Text", "bio_anonymized", "#38bdf8",
         "Gender-neutral biography (pronouns removed). Prevents gender proxy leakage via text."),
        ("Output", "384-dim embedding", "#2dd4bf",
         "Dense semantic vector per resume. Captures contextual meaning beyond keyword matching."),
    ]
    for col, (title, val, color, desc) in zip([c1, c2, c3], sbert_info):
        with col:
            st.markdown(f"""
            <div class="fusion-card" style="border-top:3px solid {color};">
                <div style="font-size:0.7rem;color:#7d8590;text-transform:uppercase;letter-spacing:1px;">{title}</div>
                <div style="font-family:'Space Mono',monospace;font-size:1rem;color:{color};font-weight:700;margin:0.3rem 0;">{val}</div>
                <div style="font-size:0.82rem;color:#7d8590;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="violet-box">
        <strong>Why bio_anonymized?</strong> Using the original biography (<code style="background:#0d1117;padding:1px 4px;border-radius:3px;">bio_original</code>) would inject gender signals
        (pronouns like "he/she") directly into the SBERT embedding — defeating the purpose of demographic attribute removal.
        Encoding <code style="background:#0d1117;padding:1px 4px;border-radius:3px;">bio_anonymized</code> implements <strong>Technique 2: Attribute Masking</strong> (Proposal §12.2).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Fusion Architectures ──────────────────────────────────────────
    st.markdown('<div class="section-header">🏗️ Fusion Architectures</div>', unsafe_allow_html=True)

    col_b, col_e, col_l, col_h = st.columns(4)
    fusion_cards = [
        (col_b, "fusion-base", "Baseline", "#7d8590",
         "Structured Only",
         "F_struct = Competency (8-dim)",
         "Setting A from baseline phase. 8 competency features only. Trained on blind_label. Reference point for all fusion comparisons."),
        (col_e, "fusion-early", "Early Fusion", "#38bdf8",
         "Feature-level concatenation",
         "F_early = [E_text ; E_struct]",
         "SBERT embeddings (384-dim) concatenated with structured features (8-dim) → 392-dim input vector. Single classifier sees all features jointly."),
        (col_l, "fusion-late", "Late Fusion", "#f43f5e",
         "Decision-level combination",
         "P = β·P_text + (1-β)·P_struct  (β=0.5)",
         "Two separate models — one on text, one on structured features. Final prediction is a weighted average of their outputs. More modular, easier to interpret."),
        (col_h, "fusion-hybrid", "Weighted Hybrid", "#22c55e",
         "Feature-level weighted mix",
         "F = α·F_text + (1-α)·F_struct",
         "Weighted combination of text and structured feature representations before the classifier. Alpha (α) tuned to balance modality contributions."),
    ]
    for col, css_class, title, color, subtitle, formula, desc in fusion_cards:
        with col:
            st.markdown(f"""
            <div class="fusion-card {css_class}">
                <div class="fusion-title" style="color:{color};">{title}</div>
                <div style="font-size:0.72rem;color:#7d8590;margin-bottom:0.5rem;">{subtitle}</div>
                <div class="fusion-formula">{formula}</div>
                <div style="font-size:0.8rem;color:#7d8590;line-height:1.5;margin-top:0.5rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── RQ Tabs ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">❓ Research Question Findings</div>', unsafe_allow_html=True)

    rq1, rq2, rq3, rq4, rq5 = st.tabs(["RQ1: Performance", "RQ2: Fairness", "RQ3: SBERT Ablation", "RQ4: Bias Mitigation", "RQ5: Trade-off"])

    # ── RQ1 ───────────────────────────────────────────────────────────
    with rq1:
        st.markdown("""
        <div class="rq-card">
            <div class="rq-number">RQ1</div>
            <div class="rq-question">Which fusion strategy achieves better predictive performance in resume evaluation?</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="amber-box">
            <strong>📌 Fusion results pending full upload.</strong>
            The baseline performance values below are confirmed from experimental images.
            Fusion strategy F1/AUC numbers (fusion_master_df) will be added when result tables are uploaded.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Confirmed Baseline (Structured Only) — Reference for RQ1**")
        st.markdown("""
        <table class="result-table">
        <thead><tr><th>Classifier</th><th>F1 (Blind)</th><th>AUC (Blind)</th><th>Notes</th></tr></thead>
        <tbody>
        <tr><td><span class="model-badge badge-lr">LR</span></td>
            <td class="best-val">0.966</td><td class="best-val">0.997</td>
            <td style="color:#7d8590;font-size:0.82rem;">Best C=100, 5-fold CV F1=0.971</td></tr>
        <tr><td><span class="model-badge badge-rf">RF</span></td>
            <td class="mono">0.936</td><td class="mono">0.987</td>
            <td style="color:#7d8590;font-size:0.82rem;">RandomizedSearch, 20 iter × 3-fold CV</td></tr>
        <tr><td><span class="model-badge badge-mlp">MLP</span></td>
            <td class="mono">0.965</td><td class="mono">0.996</td>
            <td style="color:#7d8590;font-size:0.82rem;">Architecture: (32,16), best epoch=24</td></tr>
        </tbody></table>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box" style="margin-top:1rem;">
            <strong>Expected pattern from literature:</strong>
            Early Fusion typically achieves competitive predictive performance because the classifier
            sees richer multimodal interactions. Late Fusion trades some accuracy for modularity.
            The actual fusion numbers from <code style="background:#0d1117;padding:1px 4px;border-radius:3px;">fusion_master_df</code>
            will confirm or refine this expectation.
        </div>
        """, unsafe_allow_html=True)

    # ── RQ2 ───────────────────────────────────────────────────────────
    with rq2:
        st.markdown("""
        <div class="rq-card">
            <div class="rq-number">RQ2</div>
            <div class="rq-question">Which fusion strategy produces fairer outcomes across demographic groups?</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="amber-box">
            <strong>📌 Full fairness comparison table (fusion_master_df) pending upload.</strong>
            The fairness metrics below are confirmed baseline values from Setting A experiments.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Baseline Fairness Reference (Setting A, Blind Label)**")
        st.markdown("""
        <table class="result-table">
        <thead>
            <tr>
                <th>Model</th>
                <th>DP Gap (Gender)</th>
                <th>EOO Gap (Gender)</th>
                <th>DP Gap (Ethnicity)</th>
                <th>EOO Gap (Ethnicity)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="model-badge badge-lr">LR</span></td>
                <td class="mono">0.005</td>
                <td class="mono">0.001</td>
                <td class="mono">0.023</td>
                <td class="mono">0.007</td>
            </tr>
            <tr>
                <td><span class="model-badge badge-rf">RF</span></td>
                <td class="mono">0.011</td>
                <td class="mono">0.004</td>
                <td class="mono">0.022</td>
                <td class="mono">0.004</td>
            </tr>
            <tr>
                <td><span class="model-badge badge-mlp">MLP</span></td>
                <td class="best-val">0.004</td>
                <td class="best-val">0.001</td>
                <td class="best-val">0.020</td>
                <td class="best-val">0.005</td>
            </tr>
        </tbody>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box" style="margin-top:1rem;">
            <strong>On the blind label</strong>, all models achieve very small DP and EOO gaps for gender
            (all below 0.011) — confirming that when trained on the fair label using only competency features,
            models naturally produce near-equal treatment across genders.
            Ethnicity gaps are slightly larger (up to 0.023) but still small.
        </div>
        <div class="warning-box">
            <strong>Critical finding:</strong> When trained on <em>biased</em> labels, gaps explode.
            LR reaches EOO Gap (Gender) = 0.321 on the ethnicity-biased label —
            while RF (0.259) and MLP (0.252) show slightly better fairness.
            See the Fairness Analysis page for the full breakdown.
        </div>
        """, unsafe_allow_html=True)

    # ── RQ3 ───────────────────────────────────────────────────────────
    with rq3:
        st.markdown("""
        <div class="rq-card">
            <div class="rq-number">RQ3</div>
            <div class="rq-question">Can Sentence-BERT embeddings improve both fairness and predictive accuracy?</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
            <strong>Ablation setup:</strong> Random Forest + Early Fusion is used as the representative
            classifier (typically best performer in tree-based multimodal fusion).
            Two conditions are compared:
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="fusion-card fusion-base">
                <div class="fusion-title" style="color:#7d8590;">Condition 1: No Text</div>
                <div style="font-size:0.82rem;color:#7d8590;">Structured Only (Setting A baseline)<br>8 competency features</div>
                <div class="fusion-formula">F = Competency (8-dim)</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="fusion-card fusion-early">
                <div class="fusion-title" style="color:#38bdf8;">Condition 2: SBERT</div>
                <div style="font-size:0.82rem;color:#7d8590;">Early Fusion with bio_anonymized<br>384 + 8 = 392-dim</div>
                <div class="fusion-formula">F = [SBERT_384 ; Structured_8]</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="amber-box">
            <strong>📌 Ablation result table (ablation_df) pending upload.</strong>
            Metrics: F1, AUC, DP_Gap_Gender, EOO_Gap_Gender, DI_Gender, DP_Gap_Ethnicity, DI_Ethnicity.
            Will be populated when result screenshots are provided.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
            <strong>What to look for:</strong> If SBERT improves F1 → the biography text contains
            merit signals not captured by the 8 structured competency features.
            If SBERT reduces DP/EOO gap → anonymized text encoding actively reduces demographic proxy leakage.
            If SBERT increases DP/EOO gap → the embedding still encodes latent demographic signals
            despite bio_anonymized preprocessing.
        </div>
        """, unsafe_allow_html=True)

    # ── RQ4 ───────────────────────────────────────────────────────────
    with rq4:
        st.markdown("""
        <div class="rq-card">
            <div class="rq-number">RQ4</div>
            <div class="rq-question">How do lightweight bias mitigation techniques affect model performance?</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Three Mitigation Techniques (Proposal §12)**")

        t1, t2, t3 = st.columns(3)
        techniques = [
            (t1, "Technique 1", "Sensitive Attribute Removal", "#7d8590",
             "Setting A baseline: gender and ethnicity columns are excluded from all feature sets. The simplest and most common approach — but does not prevent proxy leakage through correlated features."),
            (t2, "Technique 2", "Attribute Masking", "#38bdf8",
             "Using bio_anonymized instead of bio_original for SBERT encoding. Gender pronouns and identifiers are masked/removed. Prevents direct gender signal injection via text modality."),
            (t3, "Technique 3", "Sample Reweighting", "#22c55e",
             "Training samples weighted inversely proportional to their demographic group frequency. Computed as: w = total / (n_groups × count_per_group). Normalized to mean=1. Reduces majority-group dominance."),
        ]
        for col, t_id, t_name, color, desc in techniques:
            with col:
                st.markdown(f"""
                <div class="fusion-card" style="border-top:3px solid {color};">
                    <div style="font-size:0.68rem;color:{color};font-weight:700;text-transform:uppercase;">{t_id}</div>
                    <div style="font-family:'Space Mono',monospace;font-size:0.88rem;color:#e6edf3;margin:0.3rem 0;">{t_name}</div>
                    <div style="font-size:0.8rem;color:#7d8590;line-height:1.5;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div class="amber-box" style="margin-top:1rem;">
            <strong>📌 Mitigation comparison table (mitigation_df) pending upload.</strong>
            Columns: Technique, F1, AUC, DP_Gap_Gender, DI_Gender.
            Shows No Mitigation (bio_original) vs Attr. Masking (bio_anonymized) vs Sample Reweighting.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
            <strong>Expected trade-off:</strong> Bias mitigation techniques generally improve fairness metrics
            (lower DP Gap, DI closer to 1.0) at a small cost to predictive performance (F1/AUC).
            Sample reweighting may produce the largest fairness improvement but also the largest accuracy cost.
            Attribute masking typically has minimal accuracy impact.
        </div>
        """, unsafe_allow_html=True)

    # ── RQ5 ───────────────────────────────────────────────────────────
    with rq5:
        st.markdown("""
        <div class="rq-card">
            <div class="rq-number">RQ5</div>
            <div class="rq-question">What trade-offs exist between fairness and accuracy in multimodal fusion systems?</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
            <strong>Reading the trade-off plot:</strong>
            Each point represents one experiment (strategy + classifier).
            The <strong>ideal region is the top-left corner</strong> — high F1 AND low DP Gap.
            Points further right are less fair; points further down have lower accuracy.
            The dashed vertical line marks DP Gap = 0.05 (practical threshold).
        </div>
        """, unsafe_allow_html=True)

        p = img("tradeoff_plot.png")
        if p:
            st.image(p, use_container_width=True)

        st.markdown("""
        <div style="margin-top:1rem;">
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="insight-box">
                <strong>Gender DP Gap (left plot):</strong><br>
                Baseline and Late Fusion LR/MLP cluster in the top-left — best balance of F1 (~0.96) and low DP Gap (~0.005-0.010).
                Early Fusion RF shows low DP Gap but reduced F1 (~0.82).
                Hybrid Fusion RF is the furthest outlier (low F1, moderate gap).
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="insight-box">
                <strong>Ethnicity DP Gap (right plot):</strong><br>
                Similar pattern — Late Fusion LR/MLP remain competitive.
                LR Late Fusion approaches the 0.05 threshold on ethnicity DP Gap.
                RF-based Early Fusion shows the lowest ethnicity DP Gap among fusion strategies
                but at a cost of ~14% lower F1.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="warning-box">
            <strong>RQ5 Conclusion:</strong> A strict accuracy–fairness trade-off exists across fusion strategies.
            Late Fusion with LR or MLP occupies the best Pareto positions — achieving near-baseline accuracy
            with competitive fairness. Early Fusion RF demonstrates that text features can reduce demographic gaps
            but at a notable accuracy cost. No single strategy dominates both dimensions simultaneously.
        </div>
        """, unsafe_allow_html=True)
