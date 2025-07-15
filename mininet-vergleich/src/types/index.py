class ExperimentResult:
    def __init__(self, throughput, latency, packet_loss):
        self.throughput = throughput
        self.latency = latency
        self.packet_loss = packet_loss

    def __repr__(self):
        return (f"ExperimentResult(throughput={self.throughput}, "
                f"latency={self.latency}, packet_loss={self.packet_loss})")

class ExperimentConfig:
    def __init__(self, queue_size, udp_bandwidth, test_duration):
        self.queue_size = queue_size
        self.udp_bandwidth = udp_bandwidth
        self.test_duration = test_duration

    def __repr__(self):
        return (f"ExperimentConfig(queue_size={self.queue_size}, "
                f"udp_bandwidth={self.udp_bandwidth}, "
                f"test_duration={self.test_duration})")