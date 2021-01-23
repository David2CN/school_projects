import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize = (4, 4))
ax1, ax2, ax3 = axes.ravel()

A, k, tau, w = 1, 1, 1, 4
t = np.linspace(0, 10, 100)

#Ramp
sinin = A * (np.sin(w * t))
ax1.plot(t, sinin)
ax1.set_xlabel('t')
ax1.set_ylabel('u(t)')
ax1.set_title('Sine Input')

sine = A * k / (1 + ((tau ** 2) * (w ** 2))) * ((tau * w * (np.exp((-1/tau) * t))) - (tau * w * np.cos(w * t)) + np.sin(w * t))
ax2.plot(t, sine)
ax2.set_xlabel('t')
ax2.set_ylabel('y(t)')
ax2.set_title('Sine Response for First Order')

ax3.plot(t, sinin)
ax3.plot(t, sine)
ax3.set_xlabel('t')
ax3.set_ylabel('y(t)')
ax3.set_title('Sine input & response for  First Order')

plt.show()


