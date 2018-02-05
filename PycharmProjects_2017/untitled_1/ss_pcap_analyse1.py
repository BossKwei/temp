import numpy as np
import dpkt
import socket
import time
import matplotlib.pyplot as plt


total_len = 0
ss_len = 0
len_serial = []
ss_len_serial = []


for ts, pkt in dpkt.pcap.Reader(open('C:\\Users\\Mr.Trojan\\Desktop\\1.pcap', 'rb')):
    pkt = dpkt.ethernet.Ethernet(pkt)
    if pkt.type == 2048 and (type(pkt.data.data) in (dpkt.tcp.TCP, dpkt.udp.UDP)):  # IPv4
        total_len += 1
        ip_src = socket.inet_ntop(socket.AF_INET, pkt.ip.src)
        ip_dst = socket.inet_ntop(socket.AF_INET, pkt.ip.dst)
        data_len = pkt.data.len
        ss_flag = False
        if type(pkt.data.data) == dpkt.udp.UDP:
        # if ip_src == '107.181.138.120' or ip_dst == '107.181.138.120':
            ss_flag = True
            ss_len += 1
            ss_len_serial.append(data_len)
        len_serial.append(data_len)

print('!')


def frequency_analysis(t, y, Fs, N):
    frequency = np.linspace(0.0, 0.5 * Fs, N // 2)
    yf = np.fft.fft(y)

    def get_amplitude(yf):
        amplitude = np.abs(yf)[0:N // 2] * 2.0 / N
        amplitude[0] = np.real(yf[0]) / N
        return amplitude

    fig, [ax1, ax2, ax3] = plt.subplots(1, 3, figsize=(15, 4))
    ax1.scatter(t, y, marker='.')
    #
    xp = np.linspace(0, 100, N//2)
    yp = get_amplitude(yf)
    xi = np.linspace(0, 100, 100)
    yi = np.interp(xi, xp, yp)
    ax2.plot(xi, yi)
    print("F---------")
    print(yi)
    #
    hist, _ = np.histogram(y, bins=50)
    hist = hist / np.sum(hist)
    ax3.plot(hist)
    print("H---------")
    print(hist)


t = np.linspace(0, total_len, total_len)
y = len_serial
Fs = total_len
N = total_len
# frequency_analysis(t, y, Fs, N)

t = np.linspace(0, ss_len, ss_len)
y = ss_len_serial
Fs = ss_len
N = ss_len
frequency_analysis(t, y, Fs, N)

plt.show()

