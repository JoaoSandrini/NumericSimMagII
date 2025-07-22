import numpy as np  #needed for numerical operations
import scipy.constants as const # Helps with writing physical constants
import matplotlib.pyplot as plt # For plotting
import matplotlib.animation as animation  # For creating animations

#EMW Source
def signal(time, pulse_width, pulse_delay, omega0, amplitude = 1):
    return amplitude * np.exp(-((time - pulse_delay)/pulse_width) ** 2) * np.sin(omega0 * time)

imp0 = np.sqrt(const.mu_0/const.epsilon_0)  # Impedance of free space

simulation_size = 20e-6 # Size of the simulation box in meters
step_size = 5e-9 # Step size for the simulation in meters (dy)
N_spaces_cells = int(simulation_size / step_size) # Number of discrete spaces in the simulation (jmax)

dt = step_size/const.c # Time step based on the speed of light
simulation_time = 1e-12 # Total simulation time in seconds
N_time_steps = int(simulation_time / dt) # Number of time steps in the simulation

Ex = np.zeros(N_spaces_cells)
Hz = np.zeros(N_spaces_cells)
eps = np.ones(N_spaces_cells)  # Permittivity

refractive_index = np.sqrt(eps)  # Calculate the refractive index

h_coeff = dt / (const.mu_0 * step_size) # Defined here for optimization
e_coeff = dt / (const.epsilon_0 * eps * step_size)  # Electric field update coefficient

# Boundary Conditions
c = const.c/refractive_index[0]
c_ =  const.c/refractive_index[-1]
a = (c * dt - step_size) / (c * dt + step_size)
a_ = (c_ * dt - step_size) / (c_ * dt + step_size)

# Pulse parameters
center_frequency = 1550e-9  # Center frequency in Hz
omega0 = 2 * np.pi * const.c / center_frequency
pulse_width = 10e-15
pulse_delay = 4 * pulse_width

time = np.linspace(0, simulation_time, N_time_steps)
pulse = signal(time, pulse_width, pulse_delay, omega0)
# See the pulse shape
#plt.plot(time, pulse)
#plt.show()

j_source = 10  # Source position in the middle of the simulation box
t_offset = refractive_index[j_source] * step_size / (2 * const.c)  # Time offset for the source
Z = imp0 / refractive_index[j_source]

E_movie = []

# FDTD
for n in range(N_time_steps):
    Hz_prev = Hz.copy()  # Store previous values of Hz
    Ex_prev = Ex.copy()  # Store previous values of Ex

    # Update magnetic field, same thing as the for loop
    Hz[:N_spaces_cells - 1] = Hz_prev[:N_spaces_cells - 1] + h_coeff * (Ex[1:] - Ex[0:N_spaces_cells-1])  
    #for j in range(0, N_spaces_cells - 1):
    #    Hz[j] = Hz_prev[j] * h_coeff * (Ex[j + 1] - Ex[j])
    
    # H source
    Hz[j_source-1] = Hz[j_source-1] - signal((n + 0.5)*dt - t_offset, pulse_width, pulse_delay, omega0) / Z
    
    # Update electric field, same thing as the for loop
    Ex[1:N_spaces_cells-1] = Ex_prev[1:N_spaces_cells-1] + e_coeff[1:N_spaces_cells-1] * (Hz[1:N_spaces_cells-1] - Hz[:N_spaces_cells - 2]) # Update electric field at n+1
    #for j in range(0, N_spaces_cells - 1):
    #   Ex[j] = Ex_prev[j] * e_coeff[j] * (Hz[j] - Hz[j-1])

    # E Source
    Ex[j_source] = Ex[j_source] + signal((n + 1)*dt, pulse_width, pulse_delay, omega0)

    # Apply boundary conditions - makes the EMW not be reflected at the boundaries
    Ex[0] = Ex_prev[1] + a * (Ex[1] - Ex_prev[0])
    Ex[-1] = Ex_prev[-2] + a_ * (Ex[-2] - Ex_prev[-1])

    if n % 10 == 0:  # Plot every 100 time steps
        print(n)
        print(np.min(Ex), np.max(Ex))
        E_movie.append(Ex.copy())

frames = [] # for storing the generated images
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

for i in range(len(E_movie)):
    im, = ax.plot(E_movie[i],color = 'red')
    frames.append([im])
ani = animation.ArtistAnimation(fig, frames, interval=20, blit=True, repeat_delay=1000)
plt.show()