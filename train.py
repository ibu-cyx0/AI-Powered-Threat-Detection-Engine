"""
ML Alert Triage Model
Trains Random Forest classifier to auto-triage SOC alerts
True Positive vs False Positive classification
Author: Mohamed Ibrahim H
"""
import pandas as pd
import numpy as np
import json, os, sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score, roc_auc_score)
import pickle

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.generate_dataset import generate_dataset

DATA_DIR  = os.path.join(os.path.dirname(__file__), "..", "data")
MODEL_DIR = os.path.dirname(__file__)

FEATURES = ["duration_sec","src_bytes","dst_bytes","packet_count",
            "failed_logins","distinct_dst_ports","connection_rate",
            "alert_priority","protocol","time_of_day"]

def train():
    print("\n" + "="*55)
    print("  ML ALERT TRIAGE  |  Mohamed Ibrahim H")
    print("="*55)

    # Load or generate data
    csv_path = os.path.join(DATA_DIR, "alerts_dataset.csv")
    if not os.path.exists(csv_path):
        df = generate_dataset()
    else:
        df = pd.read_csv(csv_path)
        print(f"[+] Loaded dataset: {len(df)} samples")

    X = df[FEATURES]
    y = df["label"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    # Scale
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    # Train Random Forest
    print("\n[*] Training Random Forest Classifier...")
    clf = RandomForestClassifier(
        n_estimators=100, max_depth=12,
        class_weight="balanced", random_state=42, n_jobs=-1)
    clf.fit(X_train_s, y_train)

    # Evaluate
    y_pred = clf.predict(X_test_s)
    y_prob = clf.predict_proba(X_test_s)[:,1]
    acc    = accuracy_score(y_test, y_pred)
    auc    = roc_auc_score(y_test, y_prob)
    cv     = cross_val_score(clf, X_train_s, y_train, cv=5, scoring="roc_auc")

    print(f"\n── Model Performance ─────────────────────")
    print(f"  Accuracy       : {acc*100:.2f}%")
    print(f"  ROC-AUC Score  : {auc:.4f}")
    print(f"  CV AUC (5-fold): {cv.mean():.4f} ± {cv.std():.4f}")
    print(f"\n{classification_report(y_test, y_pred, target_names=['False Positive','True Positive'])}")

    # Feature importance
    importances = dict(zip(FEATURES, clf.feature_importances_.tolist()))
    top = sorted(importances.items(), key=lambda x: x[1], reverse=True)
    print("── Top Features ──────────────────────────")
    for feat, imp in top[:5]:
        bar = "█" * int(imp * 40)
        print(f"  {feat:<22} {bar} {imp:.3f}")

    # Save model + scaler
    with open(os.path.join(MODEL_DIR, "model.pkl"), "wb") as f:
        pickle.dump(clf, f)
    with open(os.path.join(MODEL_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    # Save metrics for dashboard
    metrics = {
        "accuracy": round(acc*100, 2),
        "roc_auc":  round(auc, 4),
        "cv_auc":   round(cv.mean(), 4),
        "cv_std":   round(cv.std(), 4),
        "feature_importance": importances,
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "fp_reduced_pct": round((1 - y_pred[y_test==0].mean()) * 100, 1)
    }
    with open(os.path.join(DATA_DIR, "model_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\n[✓] Model saved → model/model.pkl")
    print(f"[✓] FP Reduction: {metrics['fp_reduced_pct']}%")
    return clf, scaler, metrics

if __name__ == "__main__":
    train()
