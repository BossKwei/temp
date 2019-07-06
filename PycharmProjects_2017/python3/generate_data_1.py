import datetime
import numpy as np
import matplotlib.pyplot as plt

start = '2016-01-01'
end = '2017-12-31'

datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')

t = []
while datestart < dateend:
    datestart += datetime.timedelta(days=1)
    t.append((datestart.strftime('%Y%m%d'), datestart.weekday(), datestart.month))
print(len(t))

y = []
y2 = []
time = 0
for date, weekday, month in t:
    x = 200 + 10 * np.random.randn(1) + 0.2 * time + 15 * np.sin(2 * np.pi * (1 / 360) * time)
    if 0 <= weekday < 5:
        x += 8 * np.random.randn(1)
    if month in (1, 2, 3, 7, 8):
        x -= 35
    y.append(x)
    y2.append((date, x))
    time += 1

print(y)
plt.ylim(0, 500)
plt.plot(y)
plt.show()
