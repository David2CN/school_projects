import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize = (4, 4))
ax, ax1, ax2, ax3 = axes.ravel()


A, k, tau = 2, 1, 5
t = np.arange(-5, 21)

#Step
step1 = [0 for i in range(len(t[t < 0]))]
step2 = step1 + [A for i in range(len(t[t >= 0]))]
ax.plot(t, step2)
ax.set_xlabel('t')
ax.set_ylabel('u(t)')
ax.set_title('Step Input')
step = A * k * (1 - np.exp((-1/tau) * t))

ax2.plot(t, step)
ax2.set_xlabel('t')
ax2.set_ylabel('y(t)')
ax2.set_title('Step Response of First Order')


#Pulse
T = 5
mask = (t < 0)
mask2 = (t > T)
mask3 = (t >= 0) & (t <= T)
pulsein1 = [0 for i in range(len(t[mask]))]
pulsein2 = [A for i in range(len(t[mask3]))]
pulsein3 = [0 for i in range(len(t[mask2]))]
pulsein = pulsein1 + pulsein2 + pulsein3
ax1.plot(t, pulsein)
ax1.set_xlabel('t')
ax1.set_ylabel('u(t)')
ax1.set_title('Pulse Input')

pulse1 = A * k * ((1 - np.exp((-1/tau) * t)))
pulse2 =  pulse1[t > T] - (A * k * (1 - np.exp((-1/tau) * (t[t > T] - T))))
pulse = np.hstack([pulse1[t <= T], pulse2])

ax3.plot(t, pulse)
ax3.set_xlabel('t')
ax3.set_ylabel('y(t)')
ax3.set_title('Pulse Response of a First Order')


plt.show()


