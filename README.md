# 🤖 AI-Powered SOC Alert Triage System

> **ML-Based False Positive Reduction for SOC Analysts**  
> *Random Forest · scikit-learn · Auto-Escalation · Live Dashboard*

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)
![Accuracy](https://img.shields.io/badge/Accuracy-100%25-brightgreen)
![ROC--AUC](https://img.shields.io/badge/ROC--AUC-1.0000-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

SOC analysts waste **60-80% of their time** on false positive alerts. This system uses a **Random Forest ML model** trained on realistic alert features to automatically classify alerts as **True Positive (escalate)** or **False Positive (auto-close)** — reducing analyst workload and response time.

**Key Result:** 100% accuracy on test data · 1.0000 ROC-AUC · Real-time triage dashboard

---

## 🎯 Features

| Feature | Description |
|---|---|
| 🌲 Random Forest Classifier | 100-estimator ensemble trained on 2000 labeled alerts |
| ⚡ Real-time Triage | Classifies alerts in milliseconds with confidence score |
| 📊 Live Dashboard | Streams alerts with verdict, severity, and confidence bar |
| 🔍 Feature Importance | Shows which features drive each prediction |
| 📈 Confusion Matrix | Visual TP/FP/TN/FN breakdown |
| 🔄 Auto-Escalation | Routes CRITICAL/HIGH TPs directly to Tier 2 queue |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│            ALERT TRIAGE PIPELINE                │
├─────────────┬───────────────┬───────────────────┤
│  Raw Alerts │  Feature Ext  │  ML Classifier    │
│  (SIEM/IDS) │  (10 features)│  (Random Forest)  │
└──────┬──────┴───────┬───────┴────────┬──────────┘
       │              │                │
       ▼              ▼                ▼
  Log Source    Feature Vector    Prediction
  (Splunk/      [duration,        0 = FALSE POS
   Wazuh)        src_bytes,       1 = TRUE POS
                 failed_logins,   + Confidence %
                 conn_rate...]
                                       │
                    ┌──────────────────┴──────────────┐
                    │                                 │
                    ▼                                 ▼
              TRUE POSITIVE                    FALSE POSITIVE
           → Escalate Tier 2               → Auto-Close Alert
           → Create incident               → Log suppression
           → Page on-call analyst          → No action needed
```

---

## 📁 Project Structure

```
ml-alert-triage/
├── data/
│   ├── generate_dataset.py      # Synthetic alert dataset generator
│   ├── alerts_dataset.csv       # 2000 labeled alert samples
│   └── model_metrics.json       # Training results & feature importance
├── model/
│   ├── train.py                 # Model training + evaluation
│   ├── predict.py               # Real-time alert classification
│   ├── model.pkl                # Trained Random Forest model
│   └── scaler.pkl               # StandardScaler for normalization
├── dashboard/
│   └── index.html               # Live alert triage dashboard
├── main.py                      # Main orchestrator
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

```bash
git clone https://github.com/ibu-cyx0/ml-alert-triage
cd ml-alert-triage
pip install -r requirements.txt
python main.py
# Open dashboard/index.html in browser
```

---

## 🔍 Feature Engineering

| Feature | Description | Why It Matters |
|---|---|---|
| `duration_sec` | Connection duration | C2 beacons have long, regular durations |
| `src_bytes` | Bytes sent by source | Exfil = high src_bytes |
| `dst_bytes` | Bytes received | Normal browsing = high dst_bytes |
| `packet_count` | Total packets | Scans = low; exfil = high |
| `failed_logins` | Auth failures | Brute force indicator |
| `distinct_dst_ports` | Unique ports contacted | Port scan = very high |
| `connection_rate` | Connections per second | Scanners = very high |
| `alert_priority` | SIEM-assigned priority | High priority = likely TP |
| `protocol` | TCP/UDP/ICMP | Protocol anomalies matter |
| `time_of_day` | Hour of alert | 3AM alerts more suspicious |

---

## 📊 Model Performance

```
              precision    recall  f1-score   support
False Positive     1.00      1.00      1.00       200
 True Positive     1.00      1.00      1.00       200

      accuracy                          1.00       400
     macro avg     1.00      1.00      1.00       400
  weighted avg     1.00      1.00      1.00       400

ROC-AUC Score  : 1.0000
CV AUC (5-fold): 1.0000 ± 0.0000
FP Reduction   : 100%
```

### Top Feature Importances
```
alert_priority       ████████████████  0.334
connection_rate      ██████████        0.242
duration_sec         ████████          0.194
packet_count         ████              0.089
distinct_dst_ports   ██                0.048
```

---

## 🛠️ Tech Stack

- **Python** — ML pipeline, data generation, prediction engine
- **scikit-learn** — Random Forest, StandardScaler, cross-validation
- **pandas / numpy** — Feature engineering and dataset management
- **HTML/CSS/JS** — Real-time dashboard with streaming alert feed

---

## 🗺️ Roadmap

- [ ] LSTM model for sequence-based anomaly detection
- [ ] Integration with Splunk alert webhook
- [ ] SHAP explainability for each prediction
- [ ] REST API endpoint for live alert ingestion
- [ ] Email/Slack alert routing

---

## 👤 Author

**Mohamed Ibrahim H**  
EC-Council Certified SOC Analyst (CSA) | Splunk Core Certified User | Cisco Cyber Ops Associate

- GitHub: [@ibu-cyx0](https://github.com/ibu-cyx0)
- TryHackMe: [@IbrahimCyb3r4](https://tryhackme.com/p/IbrahimCyb3r4)
- Email: ibrahim.cybrx@gmail.com

---

## 📄 License

MIT License
