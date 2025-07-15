import json
import matplotlib.pyplot as plt
import os

RESULTS_FILE = './results/summary/all_results.json'
PLOT_DIR = './plots'
os.makedirs(PLOT_DIR, exist_ok=True)

with open(RESULTS_FILE) as f:
    data = json.load(f)

udp_bandwidths = sorted(set(d['udp_bandwidth'] for d in data))
tcp_throughput = [d['tcp_throughput'] for d in data if d['protocol'] == 'tcp_udp_fairness']
dctcp_throughput = [d['tcp_throughput'] for d in data if d['protocol'] == 'dctcp']
tcp_latency = [d['tcp_latency'] for d in data if d['protocol'] == 'tcp_udp_fairness']
dctcp_latency = [d['tcp_latency'] for d in data if d['protocol'] == 'dctcp']

plt.figure()
plt.plot(udp_bandwidths, tcp_throughput, 'o-', label='TCP Durchsatz')
plt.plot(udp_bandwidths, dctcp_throughput, 's-', label='DCTCP Durchsatz')
plt.xlabel('UDP-Bandbreite [Mbit/s]')
plt.ylabel('TCP/DCTCP Durchsatz [Mbit/s]')
plt.legend()
plt.title('Durchsatzvergleich TCP vs. DCTCP')
plt.savefig(os.path.join(PLOT_DIR, 'throughput_comparison.png'))

plt.figure()
plt.plot(udp_bandwidths, tcp_latency, 'o-', label='TCP Latenz')
plt.plot(udp_bandwidths, dctcp_latency, 's-', label='DCTCP Latenz')
plt.xlabel('UDP-Bandbreite [Mbit/s]')
plt.ylabel('TCP/DCTCP Latenz [ms]')
plt.legend()
plt.title('Latenzvergleich TCP vs. DCTCP')
plt.savefig(os.path.join(PLOT_DIR, 'latency_comparison.png'))

print("Plots gespeichert in", PLOT_DIR)