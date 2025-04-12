import numpy as np; import matplotlib.pyplot as plt

# Simple PV power curve model
def pv_power(d): return -10 * (d - 0.5)**2 + 5

# PSO parameters
n_particles = 10; max_iter = 20; w = 0.5; c1 = 1.5; c2 = 1.5

# Initialize
particles = np.random.uniform(0, 1, n_particles)
velocities = np.random.uniform(-0.1, 0.1, n_particles)
pbest_pos = particles.copy()
pbest_vals = np.array([pv_power(d) for d in particles])
gbest_pos = pbest_pos[np.argmax(pbest_vals)]
gbest_val = np.max(pbest_vals)
gbest_hist = [gbest_val]

# Main loop
for it in range(max_iter):
    for i in range(n_particles):
        r1, r2 = np.random.rand(2)
        velocities[i] = w*velocities[i] + c1*r1*(pbest_pos[i]-particles[i]) + c2*r2*(gbest_pos-particles[i])
        particles[i] = np.clip(particles[i] + velocities[i], 0, 1)
        curr_val = pv_power(particles[i])
        if curr_val > pbest_vals[i]: pbest_vals[i] = curr_val; pbest_pos[i] = particles[i]
        if curr_val > gbest_val: gbest_val = curr_val; gbest_pos = particles[i]
    gbest_hist.append(gbest_val)
    print(f"Iter {it+1}: DC = {gbest_pos:.4f}, P = {gbest_val:.4f}")

plt.plot(gbest_hist, 'o-'); plt.xlabel('Iteration'); plt.ylabel('Power (W)')
plt.title('PSO MPPT'); plt.grid(True); plt.show()