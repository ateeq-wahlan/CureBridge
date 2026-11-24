# CureBridge: Dual-Portal Healthcare Stage Assessment, Natural Dietary Care & Specialist Bridge

**Author:** [Ateeq Wahlan](https://wahlanos.com) ([GitHub](https://github.com/ateeq-wahlan))

CureBridge is a dual-portal clinical triage, natural dietary recovery, and local specialist bridge platform. It helps patients understand early physiological strain across 5 health domains, provides **100% non-pharmacological dietary and physical care routines** for reversible early stages, and connects patients with verified nearby doctors using Haversine geospatial distance filtering.

## Key Architectural Highlights

1. **Strict Two-Color Portal Palettes (Dark & Light Mode Ready)**:
   - **Patient Care Portal**: Forest Green (`#15803D` / `#22C55E`) and Warm Cream (`#F5F2EA` / `#0F1712`).
   - **Specialist Doctor Portal**: Dusky Purple (`#634B82` / `#9D84C7`) and Charcoal (`#131218` / `#F2F0F6`).
2. **Minimalist Two-Color Biometric Canvas**:
   - Features 5 organ/vital indicators (`O2`, `HEART`, `BP`, `LUNGS`, `LIVER`) and 2 top/upper-middle ECG pulse waves that smoothly transition direction and palette when toggling between Patient and Doctor portals without intrusive pop-ups.
3. **Compact Classical Official Login & Adaptive Sticky Header**:
   - Validates Full Name and Official Email Address before entry, displaying an inline error banner if required fields are missing.
   - Once logged in, the portal switcher vanishes and the header freezes at the top with `CureBridge` on the left and Theme Toggle, Active User Session, and Logout on the right.
4. **Flexible Collapsible Sidebar & Locked vs. Live Predictor Modes**:
   - Includes a collapsible left sidebar (`248px` expanded to `68px` compact rail).
   - Locks baseline clinical inputs on verified existing patient profiles (`CB-101` to `CB-105` spanning Stage 1, Stage 2, and Stage 3) while providing a 1-click **New Patient Predictor** mode that unlocks all 15 inputs for live inference.

## Trusted Global Public Clinical Datasets Referenced

| Clinical Domain | Public Benchmark Dataset & Repository | Key Biomarkers & Clinical Features | Verified Reference |
| :--- | :--- | :--- | :--- |
| **Metabolic & Blood Sugar Balance** | NIDDK Pima Indians Diabetes & UCI Early-Stage Diabetes Risk Prediction Dataset (ESDRPD) | Fasting Blood Sugar (mg/dL), BMI, Age, Excess Thirst (Polydipsia), Daytime Fatigue | [JPMS / UCI Benchmark Study](https://jpmsonline.com/article/a-differentiable-hybrid-classical-quantum-circuit-with-pca-feature-compression-for-medical-disease-classification-in-healthcare-datasets-1205/) |
| **Cardiovascular & Blood Pressure** | UCI Cleveland Heart Disease & Heart Failure Clinical Records Dataset | Resting Systolic Blood Pressure (mmHg), Chest Tightness/Pressure, Exertional Dyspnea, Age | [NIH PMC / UCI Heart Disease Benchmark](https://pmc.ncbi.nlm.nih.gov/articles/PMC12614364/) |
| **Digestive & Gut-Liver Health** | UCI Indian Liver Patient Dataset (ILPD - 583 Clinical Records) | Acid Reflux & Post-Meal Bloating, Bowel Irregularity, BMI, Symptom Persistence | [Frontiers in Medicine ILPD Analysis](https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2025.1502749/full) |
| **Respiratory & Airway Health** | UCI Pulmonary & Clinical Pulse Oximetry Triage Cohort | Blood Oxygen Saturation (SpO2 %), Persistent Cough/Wheeze, Breath Shortness, Symptom Weeks | [CMES Biomedical Benchmark Profiling](https://www.sciopen.com/article/10.32604/cmes.2026.082841) |
| **Confidential Intimate & Urinary Wellness** | UCI Urological & Outpatient Reproductive-Endocrine Triage Criteria | Urinary Frequency or Discomfort, Pelvic/Hormonal Strain, Sleep Quality, Symptom Duration | [IJEAIS Clinical Dataset Survey](http://ijeais.org/wp-content/uploads/2026/7/IJEAIS260708.pdf) |

## Quick Start

- **Zero-Server Browser Mode**: Open `index.html` (or `CureBridge_Healthcare_System.html`) directly in any modern browser.
- **Flask API Mode**:
  ```bash
  pip install -r requirements.txt
  python3 app.py
  ```
