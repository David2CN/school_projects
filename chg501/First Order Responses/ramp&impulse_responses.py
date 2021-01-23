import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize = (4, 4))
ax, ax1, ax2, ax3 = axes.ravel()


A, k, tau = 2, 1, 5
t = np.arange(0, 21)

#Impulse
ax.plot([0, 0], [0, A])
ax.set_xlabel('t')
ax.set_ylabel('u(t)')
ax.set_title('Impulse Input')

impulse = (A * k / tau) * (np.exp((-1/tau) * t))
ax2.plot(t, impulse)
ax2.set_xlabel('t')
ax2.set_ylabel('y(t)')
ax2.set_title('Impulse Response of First Order')


#Ramp
rampin = A * t
ax1.plot(t, rampin)
ax1.set_xlabel('t')
ax1.set_ylabel('u(t)')
ax1.set_title('Ramp Input')

ramp = A * k * (tau * (np.exp((-1/tau) * t) - 1) + t)
ax3.plot(t, ramp)
ax3.set_xlabel('t')
ax3.set_ylabel('y(t)')
ax3.set_title('Ramp Response of a First Order')


plt.show()


