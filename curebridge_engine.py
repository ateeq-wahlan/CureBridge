"""
CureBridge Clinical Stage Triage, Non-Pharmacological Care & Specialist Bridge Engine
Author: Ateeq Wahlan (https://wahlanos.com | https://github.com/ateeq-wahlan)
"""
import math
import pickle
import numpy as np


class CureBridgeEngine:
    def __init__(self, model_path="model.pkl"):
        with open(model_path, "rb") as f:
            self.artifacts = pickle.load(f)
        self.mean = np.array(self.artifacts["scaler_mean"], dtype=float)
        self.scale = np.array(self.artifacts["scaler_scale"], dtype=float)
        self.W_cond = np.array(self.artifacts["cond_weights"], dtype=float)
        self.b_cond = np.array(self.artifacts["cond_intercepts"], dtype=float)
        self.conditions = self.artifacts["conditions"]

    @staticmethod
    def _softmax(z):
        e = np.exp(z - np.max(z))
        return e / np.sum(e)

    def predict_profile(self, feature_vector):
        x = np.array(feature_vector, dtype=float)
        x_s = (x - self.mean) / self.scale
        logits = self.W_cond @ x_s + self.b_cond
        probs = self._softmax(logits)
        primary_idx = int(np.argmax(probs))

        age, bmi, bp, sugar, spo2, sleep = x[:6]
        symptoms = x[6:14]
        weeks = x[14]

        symptom_sum = float(np.sum(symptoms))
        max_sym = float(np.max(symptoms))

        vital_strain = 0.0
        if spo2 <= 93:
            vital_strain += 3.2
        elif spo2 <= 95:
            vital_strain += 1.4
        if bp >= 155:
            vital_strain += 3.0
        elif bp >= 136:
            vital_strain += 1.4
        if sugar >= 150:
            vital_strain += 2.8
        elif sugar >= 122:
            vital_strain += 1.5
        if bmi >= 31.0:
            vital_strain += 1.2
        elif bmi >= 27.5:
            vital_strain += 0.7

        duration_strain = min(2.2, max(0.0, (weeks - 2.0) * 0.25))
        symptom_strain = (max_sym * 1.15) + (max(0.0, symptom_sum - max_sym) * 0.45)
        norm_sev = min(9.9, round(vital_strain + duration_strain + symptom_strain, 1))

        if symptom_sum == 0 and vital_strain < 0.8:
            stage_id = 0
            norm_sev = 0.4
        elif norm_sev < 3.8:
            stage_id = 1
        elif norm_sev < 6.8:
            stage_id = 2
        else:
            stage_id = 3

        return {
            "primary_domain_index": primary_idx,
            "primary_domain": self.conditions[primary_idx],
            "stage_id": stage_id,
            "severity_index": norm_sev,
            "probabilities": {
                self.conditions[i]: round(float(probs[i]), 4) for i in range(len(self.conditions))
            }
        }

    @staticmethod
    def haversine_km(lat1, lon1, lat2, lon2):
        r = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        return round(r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)
