# ⚖️ FairCV Research Dashboard

**A Comparative Study of Early and Late Fusion for Fair AI-Based Resume Evaluation**  
Capstone Research Project · Built with Streamlit

---

## 📋 Overview

This dashboard presents the full experimental results of a fairness-aware comparative study of
**Early Fusion**, **Late Fusion**, and **Weighted Hybrid Fusion** strategies for AI-based resume evaluation,
using **Sentence-BERT** (all-MiniLM-L6-v2) text embeddings and three lightweight classifiers (LR, RF, MLP)
on the **FairCVdb** dataset (Peña et al., 2023).

The study is structured around 5 Research Questions (RQ1–RQ5) and evaluates both predictive performance
(F1, ROC-AUC) and fairness (Demographic Parity, Equal Opportunity, Disparate Impact) across gender and ethnicity groups.

---

## 🚀 Quick Start

```bash
# 1. Clone or copy the project
cd fairCV_dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
fairCV_dashboard/
│
├── app.py                           # Main Streamlit entry point + global CSS
├── requirements.txt
├── README.md
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py                   # Navigation + quick stats
│   ├── overview.py                  # Project Overview page
│   ├── dataset_eda.py               # Dataset & EDA page
│   ├── baseline_models.py           # Baseline Models (Setting A) page
│   ├── fusion_strategies.py         # Fusion Strategies + RQ1–RQ5 page
│   ├── fairness_analysis.py         # Fairness Analysis page
│   └── research_context.py          # Research Papers page
│
└── data/
    └── images/                      # Experimental result charts (PNG)
        ├── compare_cm.png           # Confusion matrices — all models × all labels
        ├── compare_fairness.png     # Fairness gaps — all models × all labels
        ├── compare_perf.png         # Performance comparison — all settings
        ├── compare_roc.png          # ROC curves — all models
        ├── fairness_group_cm.png    # Group-wise confusion matrices (RF, gender biased)
        ├── fairness_pos_rate.png    # Positive prediction rate by group
        ├── lr_coef.png              # LR coefficients + confusion matrix
        ├── lr_hyperparam.png        # LR hyperparameter tuning curve
        ├── lr_roc.png               # LR ROC by label type
        ├── mlp_cm.png               # MLP confusion matrices by label
        ├── mlp_loss_curves.png      # MLP training loss curves
        ├── overfitting.png          # CV vs Test F1 overfitting check
        ├── rf_importance.png        # RF feature importance (blind label)
        ├── rf_importance_by_label.png # RF feature importance across label types
        ├── rf_roc.png               # RF ROC curves
        └── tradeoff_plot.png        # RQ5 Accuracy–Fairness trade-off scatter
```

---

## 📊 Dashboard Sections

| Section | Description |
|---------|-------------|
| 🏠 **Project Overview** | Hero banner, KPI cards, pipeline diagram, Research Questions (RQ1–RQ5), key findings preview |
| 🗄️ **Dataset & EDA** | FairCVdb structure, column groups, label system, binarization strategy, demographic balance, occupations |
| 🔬 **Baseline Models** | LR / RF / MLP on Setting A — hyperparameter tuning, coefficients, feature importance, ROC, confusion matrices, overfitting check |
| 🔀 **Fusion Strategies** | SBERT explainer, Early/Late/Hybrid architecture cards, RQ1–RQ5 findings with trade-off plot |
| ⚖️ **Fairness Analysis** | DP / EOO / DI metrics, fairness gap charts, positive prediction rates, group-wise CMs, summary insights |
| 📚 **Research Context** | Paper summaries (Peña 2023, Swati 2024, Wen 2025, Reimers 2019), cross-paper synthesis table |

---

## 🔬 Research Context

### Problem Statement

AI-based hiring systems may unintentionally produce biased outcomes due to demographic correlations in
training data. Existing multimodal recruitment research rarely provides a direct fairness-focused comparison
between fusion strategies. This study fills that gap.

### Dataset — FairCVdb (Peña et al., 2023)

| Property | Value |
|---|---|
| Total profiles | 24,000 (synthetic) |
| Total columns | 60 |
| Train / Test split | 19,200 / 4,800 |
| Occupations | 10 (across 4 sectors) |
| Gender | 0=Male, 1=Female (50/50) |
| Ethnicity | G1, G2, G3 (33/33/33) |
| Labels | blind_label, biased_label_gender, biased_label_ethnicity |
| Binarization | Median of blind_label ≈ 0.413 |

### Methodology

#### 1. Text Encoding — Sentence-BERT

```
Input  : df['bio_anonymized']  (gender-neutral biographies)
Model  : all-MiniLM-L6-v2     (22M parameters, CPU-compatible)
Output : 384-dimensional dense semantic embedding per resume
```

Using `bio_anonymized` instead of `bio_original` implements **Attribute Masking** (Proposal §12.2),
preventing gender proxy leakage via text.

#### 2. Feature Settings (Baseline Phase)

| Setting | Features | Purpose |
|---|---|---|
| A | Competency Only (8 features) | Merit-based baseline |
| B | Competency + Demographics | Proxy bias measurement |
| C | Competency + Face Embedding (20-dim) | Face-aware model |
| D | Competency + Blind Face Embedding | SensitiveNets de-biased |

#### 3. Fusion Strategies (Main Phase)

All fusion experiments use `blind_label` (fair target) and the 8 competency features as the structured stream.

| Strategy | Formula | Input Dim |
|---|---|---|
| Baseline | `F = Competency` | 8 |
| Early Fusion | `F_early = [E_text ; E_struct]` | 384 + 8 = **392** |
| Late Fusion | `P = β·P_text + (1-β)·P_struct` | β = 0.5 |
| Weighted Hybrid | `F = α·F_text + (1-α)·F_struct` | α tuned |

**Total experiments:** 4 strategies × 3 classifiers = **12 experiments**

#### 4. Classifiers

| Classifier | Scaling | Hyperparameter Search |
|---|---|---|
| Logistic Regression | StandardScaler | GridSearch: C ∈ {0.001…100}, 5-fold CV → **Best C=100** |
| Random Forest | None (tree-based) | RandomizedSearch: 20 iter × 3-fold CV |
| MLP | StandardScaler | RandomizedSearch: architecture, alpha, lr → **(32,16) layers** |

#### 5. Fairness Metrics

| Metric | Formula | Threshold |
|---|---|---|
| Demographic Parity Gap | `\|P(ŷ=1\|A=0) - P(ŷ=1\|A=1)\|` | 0 = perfect |
| Equal Opportunity Gap | `\|TPR_group1 - TPR_group2\|` | 0 = perfect |
| Disparate Impact | `min_rate / max_rate` | < 0.8 = EEOC violation |

#### 6. Bias Mitigation Techniques (RQ4)

1. **Sensitive Attribute Removal** — Exclude gender/ethnicity from features (Setting A)
2. **Attribute Masking** — Use `bio_anonymized` for SBERT encoding
3. **Sample Reweighting** — Inverse frequency weighting per demographic group

---

## 📈 Key Results (Baseline — Setting A)

### Predictive Performance (Blind Label)

| Model | F1 | ROC-AUC | CV→Test Gap |
|---|---|---|---|
| **LR** | **0.966** | **0.997** | 0.006 |
| RF | 0.936 | 0.987 | 0.005 |
| MLP | 0.965 | 0.996 | 0.005 |

### Fairness (Setting A, Blind Label)

| Model | DP Gap (Gender) | EOO Gap (Gender) | DP Gap (Ethnicity) | EOO Gap (Ethnicity) |
|---|---|---|---|---|
| LR | 0.005 | 0.001 | 0.023 | 0.007 |
| RF | 0.011 | 0.004 | 0.022 | 0.004 |
| **MLP** | **0.004** | **0.001** | **0.020** | 0.005 |

### Critical Finding — Accuracy ≠ Fairness

| Model | AUC (Blind) | EOO Gap — Ethnicity Biased Label |
|---|---|---|
| LR | **0.997** (best) | **0.321** (worst) |
| RF | 0.987 | 0.259 |
| MLP | 0.996 | 0.252 |

LR achieves the highest accuracy yet the worst ethnicity fairness when trained on a biased label —
demonstrating that accuracy metrics can completely mask demographic discrimination.

### Feature Importance (LR Coefficient / RF Gini — Setting A)

| Rank | Feature | LR Coefficient | RF Gini Importance |
|---|---|---|---|
| 1 | Suitability | 10.446 | 0.2796 |
| 2 | Recommendation | 9.878 | 0.1168 |
| 3 | Language 1 | 6.402 | 0.1164 |
| 4 | Language 3 | 6.307 | 0.1151 |
| 5 | Language 2 | 6.267 | 0.1147 |
| 6 | Experience | 5.918 | 0.1033 |
| 7 | Education | 5.554 | 0.0965 |
| 8 | Availability | 4.043 | 0.0576 |

---

## 📚 Papers Integrated

1. **Peña et al. (2023)** — FairCVdb dataset & FairCVtest framework *(Springer Nature Computer Science)*
2. **Swati et al. (2024)** — Fusion techniques in multimodal AI recruitment *(EWAF'24)*
3. **Wen et al. (2025)** — FAIRE: LLM bias benchmark for resume evaluations *(arXiv:2504.01420)*
4. **Reimers & Gurevych (2019)** — Sentence-BERT text encoder *(EMNLP 2019)*

---

## 🛠️ Development Notes

- All charts in `data/images/` are generated by `FairCV_Models.ipynb` and `FairCV_EDA.ipynb`
- Dashboard uses pre-computed images (no live model loading required)
- Font: Space Mono (headers/mono) + DM Sans (body) via Google Fonts CDN
- Dark theme: `#0d1117` background, `#2dd4bf` accent

---

## 📝 Citation

```
Peña A, Serna I, Morales A, Fierrez J, et al.
Human-Centric Multimodal Machine Learning: Recent Advances and Testbed on AI-Based Recruitment.
SN Computer Science 4:434 (2023).
https://doi.org/10.1007/s42979-023-01733-0
```
