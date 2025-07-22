import numpy as np  #needed for numerical operations
import scipy.constants as const # Helps with writing physical constants
import matplotlib.pyplot as plt # For plotting

simulation_size = 10e-2 # Size of the simulation box in meters
step_size = 10e-5 # Step size for the simulation in meters (dy)
N_spaces_cells = int(simulation_size / step_size) # Number of discrete spaces in the simulation (jmax)

dt = step_size/const.c # Time step based on the speed of light
simulation_time = 10e-9 # Total simulation time in seconds
N_time_steps = int(simulation_time / dt) # Number of time steps in the simulation

Ex = np.zeros(N_spaces_cells)
Hz = np.zeros(N_spaces_cells)
eps = np.ones(N_spaces_cells)  # Permittivity

h_coeff = dt / (const.mu_0 * step_size) # Defined here for optimization
e_coeff = dt / (const.epsilon_0 * eps * step_size)  # Electric field update coefficient

# FDTD
for n in range(N_time_steps):
    Hz_prev = Hz.copy()  # Store previous values of Hz
    Ex_prev = Ex.copy()  # Store previous values of Ex

    # Update magnetic field at n+1/2


    Hz[:N_spaces_cells - 1] = Hz_prev[:N_spaces_cells - 1] + h_coeff * (Ex[1:] - Ex[0:N_spaces_cells-1])  # Update magnetic field, same thing as the for loop
    #for j in range(0, N_spaces_cells - 1):
    #    Hz[j] = Hz_prev[j] * h_coeff * (Ex[j + 1] - Ex[j])
    

    Ex[1:N_spaces_cells-1] = Ex_prev[1:N_spaces_cells-1] + e_coeff[1:N_spaces_cells-1] * (Hz[1:N_spaces_cells-1] - Hz[:N_spaces_cells - 2]) # Update electric field at n+1
    #for j in range(0, N_spaces_cells - 1):
    #    Ex[j] = Ex_prev[j] * e_coeff[j] * (Hz[j] - Hz[j-1])
    
    if n % 100 == 0:  # Plot every 100 time steps
        print(n)
        print(np.min(Ex), np.max(Ex))
    
