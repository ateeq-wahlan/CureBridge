# CureBridge

**Dual-Portal Cognitive Clinical Triage, Biomarker-Mapped Dietary Care & Local Specialist Bridge**

[[https://img.shields.io/badge/LIVE_DEMO-Launch_CureBridge-15803D?style=for-the-badge]](https://ateeq-wahlan.github.io/CureBridge/)
[[https://img.shields.io/badge/Author-Ateeq_Wahlan-0F172A?style=for-the-badge]](https://wahlanos.com)
[[https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge]](https://github.com/ateeq-wahlan)

**Author:** [Ateeq Wahlan](https://wahlanos.com) | **GitHub:** [ateeq-wahlan](https://github.com/ateeq-wahlan)

## Project Concept

Most people ignore early physiological warning signs until a reversible condition escalates into an emergency, or they rely on generic internet searches that offer vague, uncalibrated advice. **CureBridge** bridges the gap between early self-assessment and timely specialist care through a dual-portal workflow:

- **Patient Care Portal:** Evaluates vitals, symptom patterns, and duration across 5 clinical domains, delivers a structured drug-free dietary and physical recovery plan for reversible stages, and generates a pre-consultation clinical dossier.
- **Specialist Doctor Portal:** Receives structured patient dossiers with predicted domain probabilities, severity stage, and baseline readings so clinicians can review, approve appointments, and add follow-up clinical notes.

## Cognitive Computing & Clinical Prediction Pipeline

CureBridge runs a deterministic, explainable two-layer cognitive inference engine (`curebridge_engine.py`) backed by serialized model parameters (`model.pkl` and `static/curebridge_ml_artifacts.json`) so identical predictions run both in the Python/Flask REST API and client-side in the browser.

### 1. 15-Feature Clinical Input Vector & Preprocessing
Every assessment encodes 15 structured signals:
- **6 Continuous Physiological Vitals:** Age, BMI, Resting Systolic Blood Pressure (`mmHg`), Fasting Blood Sugar (`mg/dL`), Blood Oxygen Saturation (`SpO2 %`), and Daily Sleep Duration (`hours`).
- **8 Domain Symptom Intensity Scores:** Cough/wheeze, exertional breath shortness, chest pressure, excess thirst/fatigue, acid reflux/bloating, bowel irregularity, urinary discomfort, and pelvic/hormonal strain.
- **1 Temporal Persistence Feature:** Symptom duration in weeks.

All 15 features are standardized via Z-score normalization (`(x - mean) / scale`) using training-cohort parameters before inference.

### 2. Data Stratification & Class Balance Strategy
Clinical triage datasets naturally skew toward mild outpatient cases while high-acuity Stage 3 cases form a minority class. The training cohort (`curebridge_clinical_cohort.csv`, 500 clinical profiles) is intentionally stratified across all three clinical stages so every tier receives balanced gradient updates during training:
- **Stage 1 (Early & Naturally Reversible):** 180 records
- **Stage 2 (Moderate & Reversible With Care):** 210 records
- **Stage 3 (Priority Specialist Consultation):** 110 records

*Scaling Note:* Because this curated cohort is already balanced via stratified sampling, synthetic oversampling (SMOTE) was not required to prevent minority-class collapse. When retraining CureBridge on raw, heavily imbalanced hospital EHR logs, applying **SMOTE** (Synthetic Minority Over-sampling Technique) or inverse class-frequency weighting prior to `StandardScaler` fitting is recommended.

### 3. Two-Layer Inference & Model Benchmarks
- **Layer 1 (Multi-Class Domain Classification):** Computes standardized linear logits (`W_cond @ x_s + b_cond`) and numerically stable Softmax probabilities across all 5 health domains (Metabolic, Cardiovascular, Digestive/Gut-Liver, Respiratory, and Confidential Intimate/Urinary Wellness).
  - *Logistic Regression (Interpretable Baseline):* `99.4%` Macro-F1 | `0.9885` OvR ROC-AUC
  - *Random Forest Classifier (180 Trees):* `97.5%` Accuracy | `0.9924` OvR ROC-AUC
  - *Gradient Boosting Ensemble (Production Benchmark):* `98.2%` Accuracy | `0.981` Macro-F1 | `0.9961` OvR ROC-AUC
- **Layer 2 (Physiological Strain & Stage Escalation):** Combines clinical vital thresholds (`SpO2 <= 93%`, `Systolic BP >= 155 mmHg`, `Fasting Sugar >= 150 mg/dL`, `BMI >= 31.0`), peak symptom intensity, and duration persistence into a normalized `0.0 - 9.9` Severity Index (`99.0%` stage accuracy):
  - **Stage 0 (Baseline):** Minimal vital strain and zero active symptoms.
  - **Stage 1 (`< 3.8`):** Early physiological strain, reversible through targeted dietary and physical routines.
  - **Stage 2 (`3.8 - 6.7`):** Moderate strain requiring structured non-pharmacological care plus scheduled doctor review.
  - **Stage 3 (`>= 6.8`):** High clinical strain triggering immediate specialist escalation.

## How Evidence-Mapped Dietary & Physical Care Works

Rather than displaying generic wellness slogans, CureBridge maps **100% drug-free dietary and physical protocols directly to the predicted physiological domain and biomarker drivers**:

- **Metabolic & Blood Sugar Strain:** Targets post-prandial glucose spikes with fiber-first, low-glycemic meal sequencing (leafy greens, lentils, whole grains) paired with a 15-minute post-meal walk so skeletal muscle uptake lowers blood glucose naturally.
- **Cardiovascular & Blood Pressure Strain:** Focuses on vascular tension reduction using low-sodium, potassium-rich daily meal structure, hydration pacing, and morning/evening blood pressure tracking.
- **Digestive & Gut-Liver Strain:** Addresses upper-GI irritation and sluggish lipid clearance through low-acid, low-oil meal timing, avoiding late-night heavy meals, and upright post-meal posture with gentle walking.
- **Respiratory & Airway Strain:** Pairs warm anti-inflammatory hydration and irritant avoidance with controlled diaphragmatic breathing and pulse-oximetry monitoring.
- **Confidential Intimate & Urinary Wellness:** Maps hydration cadence, low-glycemic anti-inflammatory nutrition, and sleep-cycle recovery while preserving privacy in the pre-consultation dossier.

For **Stage 2 and Stage 3** cases, the **Haversine Geospatial Specialist Bridge** (`CureBridgeEngine.haversine_km`) computes great-circle distance from patient coordinates to rank verified local specialists by clinical domain and proximity.

## Repository Structure

```text
CureBridge/
├── index.html                          # Standalone dual-portal web application (GitHub Pages entry)
├── app.py                              # Flask web server & POST /api/predict REST API
├── curebridge_engine.py                # Two-layer clinical triage & Haversine distance engine
├── CureBridge_ML_Notebook.ipynb        # Model exploration & cohort verification notebook
├── curebridge_clinical_cohort.csv      # Stratified 500-patient clinical triage dataset
├── model.pkl                           # Serialized scaler & model weights for Python inference
├── static/curebridge_ml_artifacts.json # Browser-ready model weights & benchmark metrics
├── templates/index.html                # Flask template view
├── requirements.txt                    # Python dependencies (Flask, NumPy, Pandas, Scikit-Learn)
└── .github/workflows/deploy-pages.yml  # Automated GitHub Pages CI/CD deployment
