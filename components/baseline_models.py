import streamlit as st
from pathlib import Path

IMG_DIR = Path(__file__).parent.parent / "data" / "images"

def img(name):
    p = IMG_DIR / name
    return str(p) if p.exists() else None

def render_baseline():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Baseline Models — Setting A</div>
        <p class="hero-sub">
            Three classifiers (LR, RF, MLP) trained on 8 competency features across 4 feature settings
            and 3 label types. Results form the reference point for fusion strategy evaluation.
        </p>
        <div style="margin-top:0.8rem;">
            <span class="tag tag-sky">Logistic Regression</span>
            <span class="tag tag-green">Random Forest</span>
            <span class="tag tag-amber">MLP</span>
            <span class="tag tag-teal">Setting A: Competency Only</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Baseline Performance Summary (Blind Label)</div>', unsafe_allow_html=True)

    st.markdown("""
    <table class="result-table">
    <thead><tr><th>Model</th><th>Setting</th><th>F1 (Blind)</th><th>AUC (Blind)</th>
    <th>AUC (Gender Bias)</th><th>AUC (Eth Bias)</th></tr></thead>
    <tbody>
    <tr><td><span class="model-badge badge-lr">LR</span></td><td class="mono">A</td>
        <td class="best-val">0.966</td><td class="best-val">0.997</td>
        <td class="mono">0.957</td><td class="mono">0.918</td></tr>
    <tr><td><span class="model-badge badge-rf">RF</span></td><td class="mono">A</td>
        <td class="mono">0.936</td><td class="mono">0.987</td>
        <td class="mono">0.935</td><td class="mono">0.888</td></tr>
    <tr><td><span class="model-badge badge-mlp">MLP</span></td><td class="mono">A</td>
        <td class="mono">0.965</td><td class="mono">0.996</td>
        <td class="mono">—</td><td class="mono">—</td></tr>
    </tbody></table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box" style="margin-top:1rem;">
        LR and MLP achieve near-identical F1 (~0.966/0.965) and AUC (~0.997/0.996) on the fair blind label.
        RF is ~3% lower in F1 but remains competitive. CV vs Test F1 gap is at most 0.006 — no overfitting.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_lr, tab_rf, tab_mlp, tab_cross = st.tabs(["Logistic Regression", "Random Forest", "MLP", "Cross-Model"])

    with tab_lr:
        st.markdown('<div class="section-header">Logistic Regression</div>', unsafe_allow_html=True)
        col_info, col_badge = st.columns([3, 1])
        with col_info:
            st.markdown("""
            <div class="insight-box">
                Linear baseline with directly interpretable coefficients.
                Regularization via L2 (C parameter tuned via GridSearch, 5-fold CV).
            </div>
            """, unsafe_allow_html=True)
        with col_badge:
            st.markdown("""
            <div style="background:#1c2128;border:1px solid #30363d;border-radius:10px;padding:1rem;text-align:center;">
                <div style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#7d8590;margin-bottom:0.3rem;">BEST C</div>
                <div style="font-family:'Space Mono',monospace;font-size:2rem;color:#38bdf8;font-weight:700;">100</div>
                <div style="font-size:0.68rem;color:#7d8590;">5-fold CV F1 = 0.971</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("**Hyperparameter Tuning — C Selection**")
        p = img("lr_hyperparam.png")
        if p: st.image(p, use_container_width=True)

        st.markdown("**Feature Coefficients & Confusion Matrix**")
        p = img("lr_coef.png")
        if p: st.image(p, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            Suitability (10.446) > Recommendation (9.878) > Language 1 (6.402) ~ Language 3 (6.307) ~ Language 2 (6.267) > Experience (5.918) > Education (5.554) > Availability (4.043).
            All coefficients are positive — every feature pushes toward Recommended when higher.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**ROC Curves by Label Type**")
        p = img("lr_roc.png")
        if p: st.image(p, use_container_width=True)

        st.markdown("""
        <div class="warning-box">
            LR AUC drops from 0.997 (blind) to 0.957 (gender biased) to 0.918 (ethnicity biased).
            The ethnicity-biased label is hardest to learn and exposes the largest fairness gaps.
        </div>
        """, unsafe_allow_html=True)

    with tab_rf:
        st.markdown('<div class="section-header">Random Forest</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-box">
            Ensemble of decision trees, scale-invariant. Feature importance via Gini impurity decrease.
            Hyperparameters tuned via RandomizedSearch (20 iterations, 3-fold CV).
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Feature Importance (Setting A, Blind Label)**")
        p = img("rf_importance.png")
        if p: st.image(p, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            Suitability (0.2796) is dominant — nearly 2.4x the next feature.
            Recommendation (0.1168), Language 1-3 (0.116/0.115/0.115) are roughly equal.
            This ranking matches LR coefficients exactly, confirming feature ordering is robust across model types.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Feature Importance by Label Type**")
        p = img("rf_importance_by_label.png")
        if p: st.image(p, use_container_width=True)

        st.markdown("""
        <div class="amber-box">
            Under gender-biased label, Recommendation rises in relative importance.
            Under ethnicity-biased label, Language features overtake Recommendation.
            Biased labels cause the model to reweight features that correlate with demographics — a proxy bias mechanism.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**ROC Curves — Feature Settings & Label Types**")
        p = img("rf_roc.png")
        if p: st.image(p, use_container_width=True)

    with tab_mlp:
        st.markdown('<div class="section-header">Multi-Layer Perceptron</div>', unsafe_allow_html=True)
        col_arch, col_params = st.columns(2)
        with col_arch:
            st.markdown("""
            <div class="fusion-card">
                <div class="fusion-title">Architecture</div>
                <div style="font-family:'Space Mono',monospace;font-size:0.85rem;color:#f59e0b;">
                    Input (8) → 32 → 16 → Output (1)
                </div>
                <div style="font-size:0.82rem;color:#7d8590;margin-top:0.5rem;">
                    Selected by RandomizedSearch (hidden_layer_sizes: (32,16))<br>
                    L2 regularization, Adam optimizer, early stopping
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_params:
            st.markdown("""
            <div class="fusion-card">
                <div class="fusion-title">Training Details</div>
                <div style="font-size:0.85rem;line-height:1.8;color:#e6edf3;">
                    Best epoch (Blind): <span style="color:#2dd4bf;font-family:'Space Mono',monospace;">24</span><br>
                    Best epoch (Gender): <span style="color:#f43f5e;font-family:'Space Mono',monospace;">23</span><br>
                    Best epoch (Ethnicity): <span style="color:#f59e0b;font-family:'Space Mono',monospace;">53</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("**Training Loss Curves**")
        p = img("mlp_loss_curves.png")
        if p: st.image(p, use_container_width=True)

        st.markdown("**Confusion Matrices by Label Type**")
        p = img("mlp_cm.png")
        if p: st.image(p, use_container_width=True)

    with tab_cross:
        st.markdown('<div class="section-header">Cross-Model Comparison</div>', unsafe_allow_html=True)

        st.markdown("**Performance Comparison — All Settings, Blind Label**")
        p = img("compare_perf.png")
        if p: st.image(p, use_container_width=True)

        st.markdown("**ROC Curves — All Models, Setting A, Blind Label**")
        p = img("compare_roc.png")
        if p: st.image(p, use_container_width=True)

        st.markdown("**Confusion Matrices — All Models x All Labels**")
        p = img("compare_cm.png")
        if p: st.image(p, use_container_width=True)

        st.markdown("**Overfitting Check — CV vs Test F1**")
        p = img("overfitting.png")
        if p: st.image(p, use_container_width=True)

        st.markdown("""
        <div class="green-box">
            CV-to-Test F1 gap: LR=0.006, RF=0.005, MLP=0.005.
            All three models generalize reliably — no overfitting confirmed.
        </div>
        """, unsafe_allow_html=True)
