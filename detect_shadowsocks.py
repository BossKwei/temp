import time
import dpkt
import socket
import struct
import numpy as np
import matplotlib.pyplot as plt

F = np.array([549.85092876, 1.84631161, 7.24625686, 5.0383797, 6.99853457,
              1.50255445, 4.36626127, 4.95866935, 3.45665574, 4.55042411,
              2.32397034, 3.42282341, 1.97602002, 3.23253569, 3.45725634,
              3.71534851, 4.62689791, 3.8438733, 1.74597793, 1.36485671,
              4.27549965, 1.29409605, 3.6081702, 2.18414709, 0.80476456,
              2.22344187, 3.6635435, 0.66864245, 3.01349593, 1.60893295,
              1.93159699, 3.60502456, 1.51572153, 3.20920403, 2.96585503,
              0.59570594, 3.6369488, 1.91328589, 2.45297406, 2.87422478,
              3.62653438, 2.61505699, 0.93285202, 2.61087341, 1.0433738,
              2.81240329, 2.69193529, 2.7447757, 3.50277366, 1.91170636,
              1.89645859, 3.37464325, 3.87443489, 2.88008518, 3.09536179,
              4.17115956, 2.26157271, 4.12317685, 2.33176768, 3.05101856,
              3.93357842, 2.7372064, 8.06253887, 3.46319319, 2.9656001,
              1.70803287, 0.67326659, 6.17000221, 3.37711465, 4.16827182,
              4.22913834, 3.33330792, 1.6061819, 3.9014807, 2.45484721,
              3.18764991, 4.50298305, 4.84597927, 3.87708731, 1.43924832,
              5.53988964, 5.20902506, 3.43908033, 5.42388361, 5.51823775,
              2.60303553, 2.68981832, 1.97306915, 4.75873684, 4.62081544,
              7.77197192, 7.52523643, 4.95305522, 5.05568544, 3.79383539,
              10.80279768, 12.90162243, 15.52545897, 7.25273777, 6.2725986])

H = np.array([4.75563571e-01, 8.88488127e-03, 5.70964833e-02, 1.67959122e-02,
              8.80072137e-03, 9.87075443e-03, 5.63871356e-03, 1.19747520e-02,
              5.84310189e-03, 3.06582507e-03, 7.08145476e-03, 8.71656147e-03,
              4.09978960e-03, 3.22212203e-03, 3.07784791e-03, 2.93357379e-03,
              3.78719567e-03, 2.39254584e-03, 2.18815750e-03, 3.00571085e-03,
              1.64712955e-03, 1.13014728e-03, 5.56657650e-03, 1.55094680e-03,
              4.97745717e-03, 1.05801022e-03, 1.10610159e-03, 1.25037571e-03,
              1.51487827e-03, 1.63510670e-03, 7.09347761e-04, 1.21430718e-03,
              1.53892396e-03, 1.03396453e-03, 1.03396453e-03, 8.65644725e-04,
              8.89690412e-04, 1.50285543e-03, 1.35858130e-03, 6.25187857e-04,
              8.17553351e-04, 6.37210700e-04, 9.73850316e-04, 6.97324917e-04,
              3.96753832e-04, 1.09407875e-03, 5.77096483e-04, 2.88548242e-04,
              1.26239856e-03, 3.17006312e-01])

batch_flag = {}
batch_amplitude = {}
local_ip = '0.0.0.0'


def check_flag_hint(payload):
    if len(payload) < 8:
        return False
    if payload[0] == 0x14 and payload[1] == 0x03:  # TLS cipher
        return True
    elif payload[0] == 0x15 and payload[1] == 0x03:  # unknow
        return True
    elif payload[0] == 0x16 and payload[1] == 0x03:  # TLS hello
        return True
    elif payload[0] == 0x17 and payload[1] == 0x03:  # app data
        return True
    elif payload[0] == 0x48 and payload[1] == 0x54 and payload[2] == 0x54 and payload[3] == 0x50:  # HTTP
        return True
    else:
        return False


for ts, pkt in dpkt.pcap.Reader(open('path/to/xxx.pcap', 'rb')):
    pkt = dpkt.ethernet.Ethernet(pkt)
    if pkt.type == 2048 and (type(pkt.data.data) in (dpkt.tcp.TCP, dpkt.udp.UDP)):  # IPv4
        ip_src = socket.inet_ntop(socket.AF_INET, pkt.ip.src)
        ip_dst = socket.inet_ntop(socket.AF_INET, pkt.ip.dst)
        data_len = pkt.data.len
        # save current ip and data
        ip = ip_dst if ip_src == local_ip else ip_src
        if batch_amplitude.get(ip, None) is None:
            batch_amplitude[ip] = list()
            batch_flag[ip] = [0, 0]  # (num_package, num_hint)
        # sum num_package and num_hint for current ip
        payload = pkt.data.data.data
        batch_flag[ip][0] += 1  # num_package
        if check_flag_hint(payload):
            batch_flag[ip][1] += 1  # num_hint
        batch_amplitude[ip].append(data_len)

print('load finish')


def frequency_analysis(y, Fs, N):
    frequency = np.linspace(0.0, 0.5 * Fs, N // 2)
    yf = np.fft.fft(y)

    def get_amplitude(yf):
        amplitude = np.abs(yf)[0:N // 2] * 2.0 / N
        amplitude[0] = np.real(yf[0]) / N
        return amplitude

    # freq feature
    xp = np.linspace(0, 100, N // 2)
    yp = get_amplitude(yf)
    xi = np.linspace(0, 100, 100)
    yi = np.interp(xi, xp, yp)
    # hist feature
    hist, _ = np.histogram(y, bins=50)
    hist = hist / np.sum(hist)
    #
    return yi, hist


max_loss, min_loss = 0, 9999
results = []
for ip in batch_amplitude:
    (num_package, num_hint) = batch_flag[ip]
    if num_package < 500:
        continue
    amplitude = batch_amplitude[ip]
    lena = len(amplitude)
    freq_feature, hist_feature = frequency_analysis(amplitude, lena, lena)
    # looks like a webserver
    square_loss_freq = np.abs(freq_feature - F)
    loss_1 = np.sum(square_loss_freq) / np.sum(F)
    square_loss_hist = np.abs(hist_feature - H)
    loss_2 = np.sum(square_loss_hist) * 100.0
    loss = loss_1 + loss_2
    max_loss = max_loss if loss < max_loss else loss
    min_loss = min_loss if loss > min_loss else loss
    results.append([ip, num_package, num_hint, loss, loss_1, loss_2])

results = sorted(results, key=lambda value: value[2])

for ip, num_package, num_hint, loss, loss_1, loss_2 in results:
    confidence = 1.0 - (loss - min_loss) / (max_loss - min_loss)
    print('ip: ', ip, ' num_package: ', num_package, ' confidence: ', 100 * confidence, '%')
