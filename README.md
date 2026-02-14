# Advance-ddos-attack-detection-tool
🌐 <h3>Overview</h3>

This project is a real-time DDoS Detection Tool that monitors live network traffic and detects suspicious flooding activity using threshold-based anomaly detection.

The system acts as a Host-Based Intrusion Detection System (IDS) and continuously analyzes packets captured from a network interface.

It detects:

🔥 TCP SYN Flood

🌊 UDP Flood

📡 ICMP Flood

🚨 High traffic from a single IP

🌍 Possible Distributed DDoS attacks

<h3>🧠 How It Works</h3>

Live Traffic → Packet Capture → Protocol Analysis → Threshold Check → Alert Generation

1️⃣ Captures packets using Scapy
2️⃣ Extracts source IP & protocol type
3️⃣ Tracks traffic in a 10-second time window
4️⃣ Compares counts with predefined thresholds
5️⃣ Prints alerts if abnormal activity is detected
6️⃣ Resets counters and continues monitoring
<br>
<h3>Project Objectives</h3>

✔ Understand DDoS attack patterns

✔ Implement real-time packet inspection

✔ Apply threshold-based anomaly detection

✔ Learn protocol-level security monitoring

✔ Build a practical cybersecurity project

<h3>🗓️ Development Timeline</h3>
📌 Week 1

Studied DDoS attack types

Learned TCP/IP & ICMP fundamentals

Researched IDS architectures

📌 Week 2

Implemented packet sniffing

Built IP-based counters

Developed protocol detection logic

📌 Week 3

Integrated threshold-based alerts

Added time-window analysis

Conducted stress testing

📌 Week 4

Debugging & optimization

Documentation

Final validation
