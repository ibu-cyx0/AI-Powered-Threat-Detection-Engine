"""
SOC Alert Dataset Generator
Generates realistic labeled alert data for ML training
Author: Mohamed Ibrahim H
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def generate_dataset(n_samples=2000):
    records = []
    n_tp = n_samples // 2

    # Brute Force SSH
    for _ in range(n_tp // 4):
        records.append({"duration_sec":np.random.uniform(0.1,2.0),"src_bytes":np.random.randint(200,800),"dst_bytes":np.random.randint(100,400),"packet_count":np.random.randint(20,80),"failed_logins":np.random.randint(10,50),"distinct_dst_ports":np.random.randint(1,3),"connection_rate":np.random.uniform(8.0,30.0),"alert_priority":np.random.choice([1,2]),"protocol":0,"time_of_day":np.random.randint(0,24),"alert_type":"brute_force","label":1})

    # Port Scan
    for _ in range(n_tp // 4):
        records.append({"duration_sec":np.random.uniform(0.01,0.5),"src_bytes":np.random.randint(40,200),"dst_bytes":np.random.randint(0,100),"packet_count":np.random.randint(1,10),"failed_logins":0,"distinct_dst_ports":np.random.randint(50,1024),"connection_rate":np.random.uniform(20.0,100.0),"alert_priority":np.random.choice([1,2]),"protocol":0,"time_of_day":np.random.randint(0,24),"alert_type":"port_scan","label":1})

    # C2 Beaconing
    for _ in range(n_tp // 4):
        records.append({"duration_sec":np.random.uniform(30.0,300.0),"src_bytes":np.random.randint(500,2000),"dst_bytes":np.random.randint(500,2000),"packet_count":np.random.randint(50,200),"failed_logins":0,"distinct_dst_ports":np.random.randint(1,3),"connection_rate":np.random.uniform(0.1,1.0),"alert_priority":np.random.choice([1,2]),"protocol":np.random.choice([0,1]),"time_of_day":np.random.randint(0,24),"alert_type":"c2_beacon","label":1})

    # Data Exfil
    for _ in range(n_tp // 4):
        records.append({"duration_sec":np.random.uniform(10.0,600.0),"src_bytes":np.random.randint(50000,500000),"dst_bytes":np.random.randint(100,1000),"packet_count":np.random.randint(200,2000),"failed_logins":0,"distinct_dst_ports":np.random.randint(1,5),"connection_rate":np.random.uniform(1.0,10.0),"alert_priority":1,"protocol":np.random.choice([0,1]),"time_of_day":np.random.randint(0,24),"alert_type":"data_exfil","label":1})

    n_fp = n_samples - n_tp

    # Normal web
    for _ in range(n_fp // 3):
        records.append({"duration_sec":np.random.uniform(1.0,30.0),"src_bytes":np.random.randint(200,5000),"dst_bytes":np.random.randint(1000,100000),"packet_count":np.random.randint(10,100),"failed_logins":0,"distinct_dst_ports":np.random.randint(1,5),"connection_rate":np.random.uniform(0.5,5.0),"alert_priority":np.random.choice([3,4]),"protocol":np.random.choice([0,1]),"time_of_day":np.random.randint(8,20),"alert_type":"normal_http","label":0})

    # Admin tools
    for _ in range(n_fp // 3):
        records.append({"duration_sec":np.random.uniform(0.5,10.0),"src_bytes":np.random.randint(100,2000),"dst_bytes":np.random.randint(100,2000),"packet_count":np.random.randint(5,50),"failed_logins":np.random.randint(0,3),"distinct_dst_ports":np.random.randint(3,20),"connection_rate":np.random.uniform(1.0,8.0),"alert_priority":np.random.choice([2,3]),"protocol":0,"time_of_day":np.random.randint(7,19),"alert_type":"admin_tool","label":0})

    # Misconfig
    for _ in range(n_fp - 2*(n_fp//3)):
        records.append({"duration_sec":np.random.uniform(0.1,5.0),"src_bytes":np.random.randint(50,500),"dst_bytes":np.random.randint(50,500),"packet_count":np.random.randint(2,20),"failed_logins":np.random.randint(1,5),"distinct_dst_ports":np.random.randint(1,10),"connection_rate":np.random.uniform(0.2,3.0),"alert_priority":np.random.choice([3,4]),"protocol":np.random.choice([0,1,2]),"time_of_day":np.random.randint(0,24),"alert_type":"misconfig","label":0})

    df = pd.DataFrame(records).sample(frac=1,random_state=42).reset_index(drop=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(os.path.join(OUTPUT_DIR,"alerts_dataset.csv"), index=False)
    print(f"[+] Dataset: {len(df)} samples | TP: {df['label'].sum()} | FP: {(df['label']==0).sum()}")
    return df

if __name__ == "__main__":
    generate_dataset()
