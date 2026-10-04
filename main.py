"""
ML Alert Triage Platform - Main Runner
Author: Mohamed Ibrahim H
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from train import train
from predict import load_model, batch_predict, DEMO_ALERTS
def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║     AI-POWERED SOC ALERT TRIAGE SYSTEM  v1.0                ║
║     ML-Based False Positive Reduction | Mohamed Ibrahim H    ║
╚══════════════════════════════════════════════════════════════╝
    """)
    clf, scaler, metrics = train()
    print("\n► Running live alert predictions...")
    clf2, scaler2 = load_model()
    results = batch_predict(DEMO_ALERTS, clf2, scaler2)
    tp = sum(1 for r in results if r["result"]["label"]=="TRUE POSITIVE")
    fp = sum(1 for r in results if r["result"]["label"]=="FALSE POSITIVE")
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ✓  Model Accuracy   : {metrics['accuracy']}%                          ║
║  ✓  ROC-AUC Score    : {metrics['roc_auc']}                         ║
║  ✓  FP Reduction     : {metrics['fp_reduced_pct']}%                          ║
║  ✓  Alerts Triaged   : {len(results)} (TP:{tp} | FP:{fp})                   ║
║  ✓  Dashboard        : /index.html                 ║
╚══════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()
