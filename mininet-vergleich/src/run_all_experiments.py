import subprocess
import json
import os
import statistics

UDP_BANDWIDTHS = [1, 5, 10, 15, 20, 25, 30]  # Mbit/s
RESULTS_DIR = './results/summary'
NUM_RUNS = 20
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_experiment(script, udp_bandwidth, protocol, iteration):
    print(f"Starte {protocol}-Experiment mit UDP-Bandbreite {udp_bandwidth} Mbit/s, Iteration {iteration} ...")
    subprocess.run([
        'python3', script,
        '--udp_bandwidth', str(udp_bandwidth),
        '--result_base_path', f'./results/{protocol}',
        '--iteration', str(iteration)
    ], check=True)

def collect_results(protocol, udp_bandwidth, iteration):
    result_path = f'./results/{protocol}/queue_100_duration_30/iteration_{iteration}'
    tcp_json = os.path.join(result_path, 'iperf3_tcp.json')
    udp_json = os.path.join(result_path, 'iperf3_udp.json')
    ping_log = os.path.join(result_path, 'ping_result.log')
    result = {}

    # Durchsatz aus iperf3_tcp.json
    if os.path.exists(tcp_json):
        with open(tcp_json) as f:
            data = json.load(f)
            result['tcp_throughput'] = data['end']['sum_received']['bits_per_second'] / 1e6  # Mbit/s
    else:
        result['tcp_throughput'] = None

    # Latenz aus ping_result.log
    if os.path.exists(ping_log):
        with open(ping_log) as f:
            lines = f.readlines()
            for line in lines:
                if 'rtt min/avg/max/mdev' in line:
                    avg = line.split('=')[1].split('/')[1]
                    result['tcp_latency'] = float(avg)
                    break
    else:
        result['tcp_latency'] = None

    # UDP Paketverlust aus iperf3_udp.json
    if os.path.exists(udp_json):
        with open(udp_json) as f:
            data = json.load(f)
            lost = data['end']['sum']['lost_packets']
            total = data['end']['sum']['packets']
            result['udp_loss_percent'] = 100 * lost / total if total > 0 else None
    else:
        result['udp_loss_percent'] = None

    return result

def save_iteration_result(protocol, udp_bw, iteration, result):
    # Speichere das Ergebnis jeder Iteration einzeln ab
    filename = f'{protocol}_udp{udp_bw}_iter{iteration}.json'
    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(result, f, indent=2)

def main():
    all_results = []
    for udp_bw in UDP_BANDWIDTHS:
        for protocol, script in [('tcp_udp_fairness', 'src/experiments.py'), ('dctcp', 'src/dctcp_experiments.py')]:
            for i in range(1, NUM_RUNS + 1):
                run_experiment(script, udp_bw, protocol, i)
                result = collect_results(protocol, udp_bw, i)
                result['udp_bandwidth'] = udp_bw
                result['protocol'] = protocol
                result['iteration'] = i
                save_iteration_result(protocol, udp_bw, i, result)
                all_results.append(result)
                print(f"Ergebnis für {protocol} bei {udp_bw} Mbit/s, Iteration {i}: {result}")

    # Speichern aller Ergebnisse
    with open(os.path.join(RESULTS_DIR, 'all_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2)
    print("Alle Einzelwerte gespeichert.")

if __name__ == "__main__":
    main()