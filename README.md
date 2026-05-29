# ⚖️ FairCV Research Dashboard

**AI Resume Screening & Fairness Audit System**  
Capstone / Research Project Dashboard built with Streamlit

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

Open http://localhost:8501 in your browser.

---

## 📁 Project Structure

```
fairCV_dashboard/
│
├── app.py                          # Main Streamlit entry point
├── requirements.txt
├── README.md
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py                  # Navigation sidebar
│   ├── overview.py                 # Project Overview page
│   ├── progress_tracker.py         # Progress Tracker page
│   ├── dataset_analysis.py         # Dataset Analysis page
│   ├── model_analysis.py           # Model Development page
│   ├── paper_review.py             # Research Papers page
│   └── roadmap.py                  # Improvement Roadmap page
│
├── data/
│   ├── raw/                        # Place FairCVdb.csv here
│   ├── processed/                  # Preprocessed splits
│   └── metrics/                    # Saved evaluation metrics
│
├── models/
│   ├── trained_models/             # Saved .pkl model files
│   └── evaluation/                 # Evaluation results JSON
│
├── pipeline/
│   ├── preprocessing.py            # Data preprocessing utilities
│   ├── feature_engineering.py      # Feature engineering helpers
│   └── evaluation.py               # Fairness evaluation metrics
│
└── inference/
    ├── predictor.py                # Resume scoring predictor
    └── utils.py                    # Utility functions
```

---

## 📊 Dashboard Sections

| Section | Description |
|---------|-------------|
| 🏠 Project Overview | Hero section, KPIs, pipeline diagram, system architecture |
| 📊 Progress Tracker | Gantt chart, stage-by-stage status with issues noted |
| 🗄️ Dataset Analysis | EDA insights, label distributions, bias analysis, dataset limitations |
| 🤖 Model Development | Performance comparison, fairness gaps, feature importance, per-model deep-dives |
| 📚 Research Papers | Summaries, key ideas, applicability, and cross-paper synthesis for 3 papers |
| 🚀 Improvement Roadmap | Prioritized improvements (Easy/Medium/Advanced), priority matrix, radar chart |

---

## 🔬 Research Context

**Dataset:** FairCVdb (Peña et al., 2023) — 24,000 synthetic resume profiles  
**Task:** Binary classification: Recommended vs Not Recommended  
**Models:** Logistic Regression, Random Forest, MLP  
**Fairness Metrics:** Demographic Parity Gap, Equality of Opportunity Gap  

### Papers Integrated
1. **Peña et al. (2023)** — Human-Centric Multimodal ML & FairCVtest framework *(SN Computer Science)*
2. **Swati et al. (2024)** — Early vs Late Fusion in Multimodal AI Recruitment *(EWAF'24)*
3. **Wen et al. (2025)** — FAIRE: LLM Bias Benchmark for Resume Evaluations *(arXiv:2504.01420)*

---

## 📈 Key Results

| Model | F1 (Blind) | AUC (Blind) | Max EO Gap (Ethnicity) |
|-------|------------|-------------|------------------------|
| **LR** | **0.966** | **0.997** | 0.321 ⚠️ |
| **RF** | 0.936 | 0.987 | 0.259 |
| **MLP** | 0.965 | 0.996 | 0.252 |

**Critical finding:** LR achieves best accuracy yet worst ethnicity fairness — demonstrating that accuracy ≠ fairness.

---

## 🛠️ Development Notes

- All charts use `plotly` with a dark theme matching the dashboard aesthetic
- The dashboard uses pre-computed metrics from the uploaded experiment charts (no live model loading required)
- To add live model inference, place trained `.pkl` files in `models/trained_models/` and extend `inference/predictor.py`
- Font: Space Mono (headers) + DM Sans (body) via Google Fonts CDN

---

## 📝 Citation

If using FairCVdb in your work:

```
Peña A, Serna I, Morales A, Fierrez J, et al.
Human-Centric Multimodal Machine Learning: Recent Advances and Testbed on AI-Based Recruitment.
SN Computer Science 4:434 (2023). https://doi.org/10.1007/s42979-023-01733-0
```
