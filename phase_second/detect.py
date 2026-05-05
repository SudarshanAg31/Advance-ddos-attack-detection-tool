from scapy.all import rdpcap
import pandas as pd
import joblib
import sys

# ===============================
# INPUT FILE
# ===============================
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    print("Usage: python detect.py <pcap_file>")
    exit()

# ===============================
# LOAD MODEL
# ===============================
model = joblib.load("model.pkl")

# ===============================
# READ PCAP
# ===============================
packets = rdpcap(file_path)

total_packets = len(packets)

# ===============================
# FEATURE EXTRACTION
# ===============================
syn_count = 0
ack_count = 0
src_ips = set()

for pkt in packets:
    if pkt.haslayer("IP"):
        src_ips.add(pkt["IP"].src)

    if pkt.haslayer("TCP"):
        flags = pkt["TCP"].flags
        if flags & 0x02:  # SYN
            syn_count += 1
        if flags & 0x10:  # ACK
            ack_count += 1

# Duration
if total_packets > 1:
    duration = packets[-1].time - packets[0].time
else:
    duration = 1

# Rate
rate = total_packets / duration if duration > 0 else 1

# SYN/ACK ratio
syn_ack_ratio = syn_count / (ack_count + 1)

# Unique IPs
unique_ips = len(src_ips)

# ===============================
# PRINT FEATURES
# ===============================
print(f"Packets: {total_packets}")
print(f"Duration: {duration:.4f}")
print(f"Rate: {rate:.2f}")
print(f"SYN Count: {syn_count}")
print(f"ACK Count: {ack_count}")
print(f"SYN/ACK Ratio: {syn_ack_ratio:.2f}")
print(f"Unique IPs: {unique_ips}")

# ===============================
# ML PREDICTION (basic features)
# ===============================
df = pd.DataFrame([[duration, total_packets, rate]],
                  columns=["Flow Duration", "Total Packets", "Flow Pkts/s"])

ml_prediction = model.predict(df)[0]

# ===============================
# RULE-BASED DETECTION
# ===============================
rule_attack = False

if rate > 10000:
    rule_attack = True

if syn_ack_ratio > 3:
    rule_attack = True

if unique_ips > 50:
    rule_attack = True

# ===============================
# FINAL DECISION
# ===============================
print("\n===== RESULT =====")

if ml_prediction == 1 or rule_attack:
    print("🚨 DDoS Attack Detected")
else:
    print("✅ Normal Traffic")