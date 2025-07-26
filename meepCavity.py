import meep as mp
import scipy.constants
import numpy as np
import matplotlib.pyplot as plt

size_x = 16  # Length of the waveguide in the x direction (in micrometers)
size_y = 8 # Width of the waveguide in the y direction (in mic
size_z = 1  
cell = mp.Vector3(size_x,size_y,size_z) #16um length in x dir and 8um in y dir - simulation object cells

# Define the waveguide geometry
# Waveguide block with a width of infinite x 1 x infinite, eps = 12, centered at (0,0)
geometry = [mp.Block(mp.Vector3(mp.inf,1,mp.inf),
            center=mp.Vector3(),
            material=mp.Medium(epsilon=12))]

resonance_frequency_Hz = (scipy.constants.c / 2) * np.sqrt((1/size_x**2)+(1/size_y**2)+(1/size_z**2)) * 1e6
resonance_frequency_meep = resonance_frequency_Hz * 1e-6 / scipy.constants.c

# Creates a source of EMW
# Single point source, centered at (-7,0) with a exp(-iwt) sinusoidal format.
# Frequency of 0.15 means a wavelength of about 6.67um. 
# In vacuum, lambdavac = 1/0.15, for the material, lambda = lambdavac/sqrt(eps)
sources = [mp.Source(mp.ContinuousSource(frequency=resonance_frequency_meep),
                     component=mp.Ez,
                     center=mp.Vector3(0,0))]

# Using perfect conductor boundary conditions (default) - waves will reflect at the edges
# No PML layers needed for resonant cavity

# Discretize what was created above, giving 10 pixels/um
resolution = 10

# Create the simulation object
sim = mp.Simulation(cell_size=cell,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)
sim.plot2D(output_plane=mp.Volume(center=mp.Vector3(), size=mp.Vector3(size_x, size_y,0)))
plt.savefig("cavity_geometry.png")
plt.close()

animate = mp.Animate2D(fields=mp.Ez,  # Field to animate
                        normalize=True,  # Normalize the field values
                        field_parameters={'alpha':0.8, "cmap": "RdBu", 'interpolation': 'none'},
                        boundary_parameters={'hatch':'o', 'linewidth':1.5, 'facecolor':'y', 'edgecolor':'b', 'alpha':0.3},
                        output_plane=mp.Volume(center=mp.Vector3(), size=mp.Vector3(size_x, size_y, 0)),
  )  # Colormap for the field

sim.run(mp.at_every(0.2, animate),  # Run the simulation with the animation every 0.2 time units
        until=200)  # Run for 200 time units

# Save as GIF (doesn't require ffmpeg)
animate.to_mp4(fps=10, filename="cavity_resonance_animation.mp4")
plt.close()  # Close the plot to free up memory