import numpy as np
import matplotlib.pyplot as plt
import pcap


sniffer = pcap.pcap(name=None, promisc=True, immediate=True, timeout_ms=50)
for ts, pkt in sniffer:
    print(pkt)