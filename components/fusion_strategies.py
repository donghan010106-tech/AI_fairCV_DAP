import streamlit as st
import pandas as pd
from pathlib import Path

IMG_DIR  = Path(__file__).parent.parent / "data" / "images"
DATA_DIR = Path(__file__).parent.parent / "data"


def img(name):
    p = IMG_DIR / name
    return str(p) if p.exists() else None


@st.cache_data
def load_fusion():
    return pd.read_csv(DATA_DIR / "fusion_results.csv")

@st.cache_data
def load_ablation():
    return pd.read_csv(DATA_DIR / "ablation_sbert.csv")

@st.cache_data
def load_mitigation():
    df = pd.read_csv(DATA_DIR / "bias_mitigation_results.csv")
    # clean newline chars in Technique column
    df["Technique"] = df["Technique"].str.replace(r"\n", " ", regex=True)
    return df


def _badge(clf):
    m = {"LR": "badge-lr", "RF": "badge-rf", "MLP": "badge-mlp"}
    return f'<span class="model-badge {m.get(clf,"")}">{clf}</span>'


def render_fusion():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Fusion Strategies</div>
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

    # SBERT
    st.markdown('<div class="section-header">Sentence-BERT Text Encoding</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, (title, val, color, desc) in zip([c1,c2,c3], [
        ("Model",      "all-MiniLM-L6-v2", "#8b5cf6", "Lightweight transformer, 22M parameters. CPU-compatible."),
        ("Input Text", "bio_anonymized",   "#38bdf8",  "Gender-neutral biography. Prevents gender proxy leakage."),
        ("Output",     "384-dim embedding","#2dd4bf",  "Dense semantic vector per resume."),
    ]):
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
        <strong>Why bio_anonymized?</strong>
        Using <code style="background:#0d1117;padding:1px 4px;border-radius:3px;">bio_original</code>
        injects gender signals (pronouns) into the SBERT embedding.
        Encoding <code style="background:#0d1117;padding:1px 4px;border-radius:3px;">bio_anonymized</code>
        implements Attribute Masking (Proposal §12.2).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Architecture Cards
    st.markdown('<div class="section-header">Fusion Architectures</div>', unsafe_allow_html=True)
    col_b, col_e, col_l, col_h = st.columns(4)
    for col, css, title, color, subtitle, formula, desc in [
        (col_b,"fusion-base",  "Baseline",        "#7d8590","Structured Only",         "F = Competency (8-dim)",               "8 competency features. Reference point for all fusion comparisons."),
        (col_e,"fusion-early", "Early Fusion",    "#38bdf8","Feature-level concat",    "F_early = [E_text ; E_struct]",        "SBERT 384-dim + structured 8-dim = 392-dim input."),
        (col_l,"fusion-late",  "Late Fusion",     "#f43f5e","Decision-level blend",    "P = beta*P_text + (1-beta)*P_struct",  "Two separate models, outputs averaged (beta=0.5)."),
        (col_h,"fusion-hybrid","Weighted Hybrid", "#22c55e","Feature-level weighted",  "F = alpha*F_text + (1-alpha)*F_struct","Weighted combination before classification."),
    ]:
        with col:
            st.markdown(f"""
            <div class="fusion-card {css}">
                <div class="fusion-title" style="color:{color};">{title}</div>
                <div style="font-size:0.72rem;color:#7d8590;margin-bottom:0.5rem;">{subtitle}</div>
                <div class="fusion-formula">{formula}</div>
                <div style="font-size:0.8rem;color:#7d8590;line-height:1.5;margin-top:0.5rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Load data
    df   = load_fusion()
    abl  = load_ablation()
    mit  = load_mitigation()

    # RQ Tabs
    st.markdown('<div class="section-header">Research Question Findings</div>', unsafe_allow_html=True)
    rq1, rq2, rq3, rq4, rq5 = st.tabs(["RQ1: Performance", "RQ2: Fairness", "RQ3: SBERT Ablation", "RQ4: Bias Mitigation", "RQ5: Trade-off"])

    # ── RQ1 ──────────────────────────────────────────────────────────
    with rq1:
        st.markdown("""
        <div class="rq-card">
            <div class="rq-number">RQ1</div>
            <div class="rq-question">Which fusion strategy achieves better predictive performance?</div>
        </div>
        """, unsafe_allow_html=True)

        rows_html = ""
        for _, row in df.iterrows():
            f1_cls  = "best-val" if row["F1"]      == df["F1"].max()      else "mono"
            auc_cls = "best-val" if row["ROC-AUC"] == df["ROC-AUC"].max() else "mono"
            acc_cls = "best-val" if row["Accuracy"]== df["Accuracy"].max() else "mono"
            rows_html += f"""<tr>
                <td>{row['Fusion Strategy']}</td><td>{_badge(row['Classifier'])}</td>
                <td class="{acc_cls}">{row['Accuracy']:.4f}</td>
                <td class="mono">{row['Precision']:.4f}</td>
                <td class="mono">{row['Recall']:.4f}</td>
                <td class="{f1_cls}">{row['F1']:.4f}</td>
                <td class="{auc_cls}">{row['ROC-AUC']:.4f}</td></tr>"""

        st.markdown(f"""
        <table class="result-table"><thead><tr>
            <th>Strategy</th><th>Classifier</th>
            <th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th><th>ROC-AUC</th>
        </tr></thead><tbody>{rows_html}</tbody></table>
        <div style="font-size:0.72rem;color:#7d8590;margin-top:0.4rem;">Teal = best value per column</div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        base_f1   = df[df["Fusion Strategy"]=="Baseline (Structured Only)"]["F1"].mean()
        early_f1  = df[df["Fusion Strategy"]=="Early Fusion"]["F1"].mean()
        late_f1   = df[df["Fusion Strategy"]=="Late Fusion"]["F1"].mean()
        hybrid_f1 = df[df["Fusion Strategy"]=="Weighted Hybrid Fusion"]["F1"].mean()
        best_row  = df.loc[df["F1"].idxmax()]
        with c1:
            st.markdown(f"""<div class="insight-box">
                <strong>Best F1</strong><br>
                <span style="font-family:'Space Mono',monospace;color:#2dd4bf;">
                {best_row['Fusion Strategy']}<br>{best_row['Classifier']}</span><br>
                F1 = <strong>{best_row['F1']:.4f}</strong> · AUC = <strong>{best_row['ROC-AUC']:.4f}</strong>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="insight-box">
                <strong>Avg F1 by Strategy</strong><br>
                <span style="font-family:'Space Mono',monospace;font-size:0.82rem;">
                Baseline:&nbsp;&nbsp;{base_f1:.4f}<br>
                Early:&nbsp;&nbsp;&nbsp;&nbsp;{early_f1:.4f}<br>
                Late:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{late_f1:.4f}<br>
                Hybrid:&nbsp;&nbsp;&nbsp;{hybrid_f1:.4f}</span>
            </div>""", unsafe_allow_html=True)
        with c3:
            h_min = df[df['Fusion Strategy']=='Weighted Hybrid Fusion']['F1'].min()
            h_max = df[df['Fusion Strategy']=='Weighted Hybrid Fusion']['F1'].max()
            st.markdown(f"""<div class="warning-box">
                <strong>Weighted Hybrid Underperforms</strong><br>
                Hybrid F1 range: {h_min:.4f}–{h_max:.4f}<br>
                Significantly below Baseline ({base_f1:.4f} avg).
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="amber-box" style="margin-top:0.5rem;">
            <strong>RQ1 Answer:</strong> Baseline (Structured Only) + LR achieves the highest F1 (0.9658) and AUC (0.9966).
            Early Fusion LR is competitive (F1=0.9632). Late Fusion LR is close (F1=0.9606).
            Weighted Hybrid Fusion underperforms all other strategies significantly (F1 ~ 0.68–0.70).
            Adding SBERT text does not improve over structured-only — the competency features already capture most predictive signal.
        </div>
        """, unsafe_allow_html=True)

    # ── RQ2 ──────────────────────────────────────────────────────────
    with rq2:
        st.markdown("""
        <div class="rq-card">
            <div class="rq-number">RQ2</div>
            <div class="rq-question">Which fusion strategy produces fairer outcomes across demographic groups?</div>
        </div>
        """, unsafe_allow_html=True)

        rows_html = ""
        for _, row in df.iterrows():
            di_g  = "warn-val" if row["DI_Gender"]    < 0.80 else "mono"
            di_e  = "warn-val" if row["DI_Ethnicity"] < 0.80 else "mono"
            dp_g  = "best-val" if row["DP_Gap_Gender"]     == df["DP_Gap_Gender"].min()     else "mono"
            dp_e  = "best-val" if row["DP_Gap_Ethnicity"]  == df["DP_Gap_Ethnicity"].min()  else "mono"
            eoo_g = "best-val" if row["EOO_Gap_Gender"]    == df["EOO_Gap_Gender"].min()    else "mono"
            eoo_e = "best-val" if row["EOO_Gap_Ethnicity"] == df["EOO_Gap_Ethnicity"].min() else "mono"
            rows_html += f"""<tr>
                <td>{row['Fusion Strategy']}</td><td>{_badge(row['Classifier'])}</td>
                <td class="{dp_g}">{row['DP_Gap_Gender']:.4f}</td>
                <td class="{eoo_g}">{row['EOO_Gap_Gender']:.4f}</td>
                <td class="{di_g}">{row['DI_Gender']:.4f}</td>
                <td class="{dp_e}">{row['DP_Gap_Ethnicity']:.4f}</td>
                <td class="{eoo_e}">{row['EOO_Gap_Ethnicity']:.4f}</td>
                <td class="{di_e}">{row['DI_Ethnicity']:.4f}</td></tr>"""

        st.markdown(f"""
        <table class="result-table"><thead><tr>
            <th>Strategy</th><th>Classifier</th>
            <th>DP Gap (Gender)</th><th>EOO Gap (Gender)</th><th>DI (Gender)</th>
            <th>DP Gap (Ethnicity)</th><th>EOO Gap (Ethnicity)</th><th>DI (Ethnicity)</th>
        </tr></thead><tbody>{rows_html}</tbody></table>
        <div style="font-size:0.72rem;color:#7d8590;margin-top:0.4rem;">
            Teal = best (lowest gap) &nbsp;|&nbsp; Red = DI &lt; 0.80 (EEOC violation)
        </div>
        """, unsafe_allow_html=True)

        violations = df[(df["DI_Gender"] < 0.80) | (df["DI_Ethnicity"] < 0.80)]
        if violations.empty:
            st.markdown("""<div class="green-box" style="margin-top:0.8rem;">
                No EEOC Disparate Impact violations — all DI values >= 0.80.
            </div>""", unsafe_allow_html=True)

        best_dp_g  = df.loc[df["DP_Gap_Gender"].idxmin()]
        best_dp_e  = df.loc[df["DP_Gap_Ethnicity"].idxmin()]
        worst_dp_g = df.loc[df["DP_Gap_Gender"].idxmax()]
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class="insight-box">
                <strong>Fairest — Gender DP</strong><br>
                <span style="font-family:'Space Mono',monospace;color:#2dd4bf;">
                {best_dp_g['Fusion Strategy']}<br>{best_dp_g['Classifier']}</span><br>
                DP Gap = <strong>{best_dp_g['DP_Gap_Gender']:.4f}</strong>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="insight-box">
                <strong>Fairest — Ethnicity DP</strong><br>
                <span style="font-family:'Space Mono',monospace;color:#2dd4bf;">
                {best_dp_e['Fusion Strategy']}<br>{best_dp_e['Classifier']}</span><br>
                DP Gap = <strong>{best_dp_e['DP_Gap_Ethnicity']:.4f}</strong>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="warning-box">
                <strong>Least Fair — Gender DP</strong><br>
                <span style="font-family:'Space Mono',monospace;color:#f43f5e;">
                {worst_dp_g['Fusion Strategy']}<br>{worst_dp_g['Classifier']}</span><br>
                DP Gap = <strong>{worst_dp_g['DP_Gap_Gender']:.4f}</strong>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="amber-box" style="margin-top:0.5rem;">
            <strong>RQ2 Answer:</strong> Late Fusion achieves the most consistently fair outcomes across gender and ethnicity.
            Early Fusion RF achieves the lowest gender DP gap (0.0037) but at cost of lower accuracy (F1=0.82).
            Weighted Hybrid Fusion shows the largest fairness gaps (DP Gap Gender up to 0.0425).
            All experiments pass the EEOC 4/5 Disparate Impact threshold (DI >= 0.80).
        </div>
        """, unsafe_allow_html=True)

    # ── RQ3 ──────────────────────────────────────────────────────────
    with rq3:
        st.markdown("""
        <div class="rq-card">
            <div class="rq-number">RQ3</div>
            <div class="rq-question">Can Sentence-BERT embeddings improve both fairness and predictive accuracy?</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Ablation setup:** Random Forest + Early Fusion. Two conditions compared.")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""<div class="fusion-card fusion-base">
                <div class="fusion-title" style="color:#7d8590;">Condition 1: No Text</div>
                <div style="font-size:0.82rem;color:#7d8590;">Structured Only (Setting A baseline)<br>8 competency features</div>
                <div class="fusion-formula">F = Competency (8-dim)</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div class="fusion-card fusion-early">
                <div class="fusion-title" style="color:#38bdf8;">Condition 2: SBERT</div>
                <div style="font-size:0.82rem;color:#7d8590;">Early Fusion with bio_anonymized<br>384 + 8 = 392-dim</div>
                <div class="fusion-formula">F = [SBERT_384 ; Structured_8]</div>
            </div>""", unsafe_allow_html=True)

        p = img("ablation_sbert_plot.png")
        if p: st.image(p, use_container_width=True)

        # Table from CSV
        rows_html = ""
        for _, row in abl.iterrows():
            f1_cls  = "best-val" if row["F1"]  == abl["F1"].max()  else "mono"
            auc_cls = "best-val" if row["AUC"] == abl["AUC"].max() else "mono"
            dp_cls  = "best-val" if row["DP_Gap_Gender"] == abl["DP_Gap_Gender"].min() else "mono"
            rows_html += f"""<tr>
                <td>{row['Text Representation']}</td>
                <td class="mono">{row.get('Fusion','—') if pd.notna(row.get('Fusion')) else '—'}</td>
                <td class="{f1_cls}">{row['F1']:.4f}</td>
                <td class="{auc_cls}">{row['AUC']:.4f}</td>
                <td class="mono">{row['Accuracy']:.4f}</td>
                <td class="{dp_cls}">{row['DP_Gap_Gender']:.4f}</td>
                <td class="mono">{row['EOO_Gap_Gender']:.4f}</td>
                <td class="mono">{row['DI_Gender']:.4f}</td></tr>"""

        st.markdown(f"""
        <table class="result-table"><thead><tr>
            <th>Text Representation</th><th>Fusion</th>
            <th>F1</th><th>AUC</th><th>Accuracy</th>
            <th>DP Gap (Gender)</th><th>EOO Gap (Gender)</th><th>DI (Gender)</th>
        </tr></thead><tbody>{rows_html}</tbody></table>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="warning-box" style="margin-top:0.8rem;">
            <strong>RQ3 Answer:</strong>
            SBERT does NOT improve predictive performance — F1 drops from 0.9356 (Structured Only) to 0.8198 (SBERT + Early Fusion).
            However, SBERT improves gender fairness: DP_Gap_Gender improves from 0.011 to 0.004,
            and DI_Gender improves from 0.9778 to 0.9932.
            There is a clear accuracy–fairness trade-off: SBERT adds fairness at the cost of accuracy.
        </div>
        """, unsafe_allow_html=True)

    # ── RQ4 ──────────────────────────────────────────────────────────
    with rq4:
        st.markdown("""
        <div class="rq-card">
            <div class="rq-number">RQ4</div>
            <div class="rq-question">How do lightweight bias mitigation techniques affect model performance?</div>
        </div>
        """, unsafe_allow_html=True)

        t1, t2, t3 = st.columns(3)
        for col, t_id, t_name, color, desc in [
            (t1, "T1", "Sensitive Attr. Removal", "#7d8590",
             "Exclude gender/ethnicity from features (Setting A). Simplest approach."),
            (t2, "T2", "Attribute Masking",        "#38bdf8",
             "Use bio_anonymized instead of bio_original for SBERT. Prevents direct gender injection via text."),
            (t3, "T3", "Sample Reweighting",       "#22c55e",
             "Training samples weighted inversely proportional to demographic group frequency. Reduces majority-group dominance."),
        ]:
            with col:
                st.markdown(f"""<div class="fusion-card" style="border-top:3px solid {color};">
                    <div style="font-size:0.68rem;color:{color};font-weight:700;text-transform:uppercase;">{t_id}</div>
                    <div style="font-family:'Space Mono',monospace;font-size:0.88rem;color:#e6edf3;margin:0.3rem 0;">{t_name}</div>
                    <div style="font-size:0.8rem;color:#7d8590;line-height:1.5;">{desc}</div>
                </div>""", unsafe_allow_html=True)

        p = img("bias_mitigation_plot.png")
        if p: st.image(p, use_container_width=True)

        # Table from CSV
        rows_html = ""
        for _, row in mit.iterrows():
            f1_cls = "best-val" if row["F1"]  == mit["F1"].max()  else "mono"
            dp_cls = "best-val" if row["DP_Gap_Gender"] == mit["DP_Gap_Gender"].min() else "mono"
            di_cls = "best-val" if row["DI_Gender"] == mit["DI_Gender"].max() else "mono"
            rows_html += f"""<tr>
                <td>{row['Technique']}</td>
                <td class="{f1_cls}">{row['F1']:.4f}</td>
                <td class="mono">{row['AUC']:.4f}</td>
                <td class="mono">{row['Accuracy']:.4f}</td>
                <td class="{dp_cls}">{row['DP_Gap_Gender']:.4f}</td>
                <td class="mono">{row['EOO_Gap_Gender']:.4f}</td>
                <td class="{di_cls}">{row['DI_Gender']:.4f}</td></tr>"""

        st.markdown(f"""
        <table class="result-table"><thead><tr>
            <th>Technique</th><th>F1</th><th>AUC</th><th>Accuracy</th>
            <th>DP Gap (Gender)</th><th>EOO Gap (Gender)</th><th>DI (Gender)</th>
        </tr></thead><tbody>{rows_html}</tbody></table>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="amber-box" style="margin-top:0.8rem;">
            <strong>RQ4 Answer:</strong>
            All three mitigation techniques reduce gender DP gap relative to T1 baseline (0.011).
            T2 Attribute Masking: DP Gap drops to 0.004, DI improves to 0.993 — at a moderate F1 cost (0.936 to 0.820).
            T3 Sample Reweighting: achieves the lowest DP Gap (0.003) and highest DI (0.994), at similar F1 cost (0.819).
            T1 Sensitive Attribute Removal achieves the best F1 (0.936) but the weakest fairness.
            Fairness improvements come at the cost of predictive performance — consistent with RQ5 findings.
        </div>
        """, unsafe_allow_html=True)

    # ── RQ5 ──────────────────────────────────────────────────────────
    with rq5:
        st.markdown("""
        <div class="rq-card">
            <div class="rq-number">RQ5</div>
            <div class="rq-question">What trade-offs exist between fairness and accuracy in multimodal fusion systems?</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
            Each point = one experiment (strategy + classifier).
            Ideal = top-left (high F1, low DP Gap).
            Dashed line = DP Gap 0.04 practical threshold.
        </div>
        """, unsafe_allow_html=True)

        p = img("tradeoff_plot.png")
        if p: st.image(p, use_container_width=True)

        strategy_colors = {
            "Baseline (Structured Only)": "#7d8590",
            "Early Fusion":               "#38bdf8",
            "Late Fusion":                "#f43f5e",
            "Weighted Hybrid Fusion":     "#22c55e",
        }
        summary_rows = ""
        for _, row in df.iterrows():
            color = strategy_colors.get(row["Fusion Strategy"], "#e6edf3")
            high_f1 = row["F1"] >= 0.93
            low_gap = row["DP_Gap_Gender"] <= 0.01
            if high_f1 and low_gap:   quad = "Best zone"
            elif high_f1:             quad = "High acc, less fair"
            elif low_gap:             quad = "Fair, lower acc"
            else:                     quad = "Avoid"
            summary_rows += f"""<tr>
                <td style="color:{color};font-weight:600;">{row['Fusion Strategy']}</td>
                <td>{_badge(row['Classifier'])}</td>
                <td class="mono">{row['F1']:.4f}</td>
                <td class="mono">{row['DP_Gap_Gender']:.4f}</td>
                <td class="mono">{row['DP_Gap_Ethnicity']:.4f}</td>
                <td style="font-size:0.82rem;">{quad}</td></tr>"""

        st.markdown(f"""
        <table class="result-table"><thead><tr>
            <th>Strategy</th><th>Classifier</th>
            <th>F1</th><th>DP Gap Gender</th><th>DP Gap Ethnicity</th><th>Zone</th>
        </tr></thead><tbody>{summary_rows}</tbody></table>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="warning-box" style="margin-top:1rem;">
            <strong>RQ5 Conclusion:</strong>
            A clear accuracy–fairness trade-off exists. Baseline and Late Fusion (LR/MLP) occupy the best Pareto positions
            — high F1 (>=0.95) with low DP gaps (<=0.009).
            Early Fusion RF achieves the lowest gender DP gap (0.0037) at the cost of F1 dropping to 0.82.
            Weighted Hybrid Fusion sits in the worst zone — lowest accuracy AND higher fairness gaps.
            No single strategy dominates all dimensions simultaneously.
        </div>
        """, unsafe_allow_html=True)
