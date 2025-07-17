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
            # Prüfe, ob mindestens ein Ping erfolgreich war
            latency_found = False
            for line in lines:
                if 'rtt min/avg/max/mdev' in line:
                    avg = line.split('=')[1].split('/')[1]
                    result['tcp_latency'] = float(avg)
                    latency_found = True
                    break
            if not latency_found:
                result['tcp_latency'] = None
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
    summary_results = []
    for udp_bw in UDP_BANDWIDTHS:
        for protocol, script in [('tcp_udp_fairness', 'src/experiments.py')]:
            latencies = []
            throughputs = []
            udp_losses = []
            for i in range(1, NUM_RUNS + 1):
                run_experiment(script, udp_bw, protocol, i)
                result = collect_results(protocol, udp_bw, i)
                if result['tcp_latency'] is not None:
                    latencies.append(result['tcp_latency'])
                if result['tcp_throughput'] is not None:
                    throughputs.append(result['tcp_throughput'])
                if result['udp_loss_percent'] is not None:
                    udp_losses.append(result['udp_loss_percent'])
            avg_latency = statistics.mean(latencies) if latencies else None
            avg_throughput = statistics.mean(throughputs) if throughputs else None
            avg_udp_loss = statistics.mean(udp_losses) if udp_losses else None
            summary = {
                'udp_bandwidth': udp_bw,
                'protocol': protocol,
                'avg_latency': avg_latency,
                'avg_throughput': avg_throughput,
                'avg_udp_loss_percent': avg_udp_loss,
                'num_iterations': NUM_RUNS
            }
            summary_results.append(summary)
            print(f"Durchschnitt für {protocol} bei {udp_bw} Mbit/s: {summary}")
            print(f"Durchschnittslatenz für UDP-Bandbreite {udp_bw}: {avg_latency} ms")

        # Nach jedem UDP-Bandbreiten-Durchlauf Plot generieren
        subprocess.run(['python3', 'src/plot_results.py'])

    # Speichern der Durchschnittswerte
    with open(os.path.join(RESULTS_DIR, 'summary_results.json'), 'w') as f:
        json.dump(summary_results, f, indent=2)
    print("Alle Durchschnittswerte gespeichert.")

if __name__ == "__main__":
    main()