"""
Alert Triage Predictor
Real-time alert classification using trained ML model
Author: Mohamed Ibrahim H
"""
import pickle, json, os
import pandas as pd
from datetime import datetime, timezone

MODEL_DIR = os.path.dirname(__file__)
DATA_DIR = MODEL_DIR

FEATURES = ["duration_sec","src_bytes","dst_bytes","packet_count",
            "failed_logins","distinct_dst_ports","connection_rate",
            "alert_priority","protocol","time_of_day"]

def load_model():
    with open(os.path.join(MODEL_DIR,"model.pkl"),"rb") as f: clf = pickle.load(f)
    with open(os.path.join(MODEL_DIR,"scaler.pkl"),"rb") as f: scaler = pickle.load(f)
    return clf, scaler

def predict_alert(alert: dict, clf, scaler):
    """Classify a single alert as TP or FP with confidence score."""
    df = pd.DataFrame([alert])[FEATURES]
    scaled = scaler.transform(df)
    pred   = clf.predict(scaled)[0]
    prob   = clf.predict_proba(scaled)[0]

    confidence = round(float(max(prob)) * 100, 1)
    label      = "TRUE POSITIVE"  if pred == 1 else "FALSE POSITIVE"
    severity   = "CRITICAL" if prob[1] > 0.85 else "HIGH" if prob[1] > 0.65 else "MEDIUM" if prob[1] > 0.4 else "LOW"
    action     = "ESCALATE → SOC Tier 2" if pred == 1 else "AUTO-CLOSE → No action needed"

    return {
        "label":      label,
        "confidence": confidence,
        "tp_prob":    round(float(prob[1])*100, 1),
        "fp_prob":    round(float(prob[0])*100, 1),
        "severity":   severity,
        "action":     action,
        "timestamp":  datetime.now(timezone.utc).isoformat()
    }

def batch_predict(alerts: list, clf, scaler):
    return [{"alert": a, "result": predict_alert(a, clf, scaler)} for a in alerts]

# Demo alerts for testing
DEMO_ALERTS = [
    {"duration_sec":0.3,"src_bytes":150,"dst_bytes":80,"packet_count":5,"failed_logins":25,"distinct_dst_ports":1,"connection_rate":18.5,"alert_priority":1,"protocol":0,"time_of_day":3,  "desc":"SSH Brute Force at 3AM"},
    {"duration_sec":180,"src_bytes":1200,"dst_bytes":1100,"packet_count":80,"failed_logins":0,"distinct_dst_ports":1,"connection_rate":0.4,"alert_priority":2,"protocol":0,"time_of_day":14,"desc":"C2 Beaconing"},
    {"duration_sec":8.0,"src_bytes":800,"dst_bytes":900,"packet_count":20,"failed_logins":1,"distinct_dst_ports":8,"connection_rate":2.5,"alert_priority":3,"protocol":0,"time_of_day":10, "desc":"Admin tool (FP)"},
    {"duration_sec":0.1,"src_bytes":60,"dst_bytes":20,"packet_count":2,"failed_logins":0,"distinct_dst_ports":600,"connection_rate":55.0,"alert_priority":1,"protocol":0,"time_of_day":2,  "desc":"Port Scan"},
    {"duration_sec":200000,"src_bytes":450000,"dst_bytes":300,"packet_count":1500,"failed_logins":0,"distinct_dst_ports":1,"connection_rate":7.5,"alert_priority":1,"protocol":0,"time_of_day":23,"desc":"Data Exfiltration"},
    {"duration_sec":15.0,"src_bytes":2000,"dst_bytes":50000,"packet_count":40,"failed_logins":0,"distinct_dst_ports":2,"connection_rate":1.5,"alert_priority":4,"protocol":1,"time_of_day":11,"desc":"Normal browsing (FP)"},
]

if __name__ == "__main__":
    clf, scaler = load_model()
    print("\n── Live Alert Triage ─────────────────────────────────")
    for a in DEMO_ALERTS:
        r = predict_alert(a, clf, scaler)
        icon = "🔴" if r["label"] == "TRUE POSITIVE" else "✅"
        print(f"\n  {icon} [{r['severity']:<8}] {a['desc']}")
        print(f"     → {r['label']} ({r['confidence']}% confidence)")
        print(f"     → {r['action']}")
