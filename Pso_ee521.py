import numpy as np
import matplotlib.pyplot as plt

# Simple PV power curve model
def pv_power(duty_cycle):
    return -10 * (duty_cycle - 0.5)**2 + 5

num_particles = 10
max_iterations = 20
w = 0.5
c1 = 1.5
c2 = 1.5

# Initialize particle positions and velocities
particles = np.random.uniform(0, 1, num_particles)
velocities = np.random.uniform(-0.1, 0.1, num_particles)
pbest_positions = particles.copy()
pbest_values = np.array([pv_power(d) for d in particles])
gbest_position = pbest_positions[np.argmax(pbest_values)]
gbest_value = np.max(pbest_values)

gbest_history = [gbest_value]
# Main PSO loop
for iteration in range(max_iterations):
    for i in range(num_particles):
        r1, r2 = np.random.rand(2)
        velocities[i] = (w * velocities[i] +
                         c1 * r1 * (pbest_positions[i] - particles[i]) +
                         c2 * r2 * (gbest_position - particles[i]))
        
        particles[i] += velocities[i]
        particles[i] = np.clip(particles[i], 0, 1)
        
        current_value = pv_power(particles[i])
        
        if current_value > pbest_values[i]:
            pbest_values[i] = current_value
            pbest_positions[i] = particles[i]
        
        if current_value > gbest_value:
            gbest_value = current_value
            gbest_position = particles[i]
    
    gbest_history.append(gbest_value)
    
    print(f"Iteration {iteration + 1}: Best Duty Cycle = {gbest_position:.4f}, Max Power = {gbest_value:.4f}")

# Plot convergence history
plt.plot(gbest_history, marker='o')
plt.xlabel('Iteration')
plt.ylabel('Maximum Power (W)')
plt.title('PSO Convergence in MPPT')
plt.grid(True)
plt.show()