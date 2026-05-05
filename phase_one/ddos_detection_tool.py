from scapy.all import sniff, IP
from collections import defaultdict
import time

# -------- CONFIG --------
WINDOW = 10  # seconds
SUBNET_PACKET_THRESHOLD = 3000
SUBNET_IP_THRESHOLD = 8
GLOBAL_PACKET_THRESHOLD = 6000
GLOBAL_IP_THRESHOLD = 20
# ------------------------

start_time = time.time()

subnet_packets = defaultdict(int)
subnet_ips = defaultdict(set)
global_packets = 0
global_ips = set()

def get_subnet(ip):
    parts = ip.split(".")
    return ".".join(parts[:3]) + ".0/24"

def detect(packet):
    global start_time, global_packets

    if IP in packet:
        src_ip = packet[IP].src
        subnet = get_subnet(src_ip)

        # Update counters
        subnet_packets[subnet] += 1
        subnet_ips[subnet].add(src_ip)

        global_packets += 1
        global_ips.add(src_ip)

    # ---- Check every WINDOW seconds ----
    if time.time() - start_time >= WINDOW:
        print("\n--- Analysis Window ---")

        # SAME NETWORK + DIFFERENT IPs
        for subnet in subnet_packets:
            if (subnet_packets[subnet] > SUBNET_PACKET_THRESHOLD and
                len(subnet_ips[subnet]) > SUBNET_IP_THRESHOLD):
                print(f"[ALERT] Same-Network DDoS detected → {subnet}")
                print(f"IPs: {len(subnet_ips[subnet])}, Packets: {subnet_packets[subnet]}")

        # DIFFERENT NETWORKS + DIFFERENT IPs
        if (global_packets > GLOBAL_PACKET_THRESHOLD and
            len(global_ips) > GLOBAL_IP_THRESHOLD):
            print("[ALERT] Distributed DDoS detected")
            print(f"IPs: {len(global_ips)}, Packets: {global_packets}")

        # Reset window
        subnet_packets.clear()
        subnet_ips.clear()
        global_packets = 0
        global_ips.clear()
        start_time = time.time()

# Start sniffing
sniff(iface="Wi-Fi",prn=detect, store=False)
