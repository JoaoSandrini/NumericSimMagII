import meep as mp
import numpy as np
import matplotlib.pyplot as plt

size_x = 16  # Length of the waveguide in the x direction (in micrometers)
size_y = 8   # Width of the waveguide in the y direction (in mic
cell = mp.Vector3(size_x,size_y,0) #16um length in x dir and 8um in y dir - simulation object cells

# Define the waveguide geometry
# Waveguide block with a width of infinite x 1 x infinite, eps = 12, centered at (0,0)
geometry = [mp.Block(mp.Vector3(mp.inf,1,mp.inf),
            center=mp.Vector3(),
            material=mp.Medium(epsilon=12))]

# Creates a source of EMW
# Single point source, centered at (-7,0) with a exp(-iwt) sinusoidal format.
# Frequency of 0.15 means a wavelength of about 6.67um. 
# In vacuum, lambdavac = 1/0.15, for the material, lambda = lambdavac/sqrt(eps)
sources = [mp.Source(mp.ContinuousSource(frequency=0.15),
                     component=mp.Ez,
                     center=mp.Vector3(-7,0))]

#This deals with boundary conditions, in this casem absorbs all waves at the edges.
pml_layers = [mp.PML(1.0)]

# Discretize what was created above, giving 10 pixels/um
resolution = 10

# Create the simulation object
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)
"""
sim.plot2D(output_plane=mp.Volume(center=mp.Vector3(), size=mp.Vector3(size_x, size_y,0)))
plt.savefig("sim.png")
plt.close()

animate = mp.Animate2D(fields=mp.Ez,  # Field to animate
                        normalize=True,  # Normalize the field values
                        field_parameters={'alpha':0.8, "cmap": "RdBu", 'interpolation': 'none'},
                        boundary_parameters={'hatch':'o', 'linewidth':1.5, 'facecolor':'y', 'edgecolor':'b', 'alpha':0.3},
                        output_plane=mp.Volume(center=mp.Vector3(), size=mp.Vector3(size_x, size_y, 0)),
  )  # Colormap for the field

sim.run(mp.at_every(0.2, animate),  # Run the simulation with the animation every 0.2 time units
        until=200)  # Run for 200 time units

# Save as MP4
animate.to_mp4(fps=10, filename="waveguide_animation.mp4")  # Save the animation to a GIF file
plt.close()  # Close the plot to free up memory
"""


# Runs the simulation for 200 time units
sim.run(mp.at_beginning(mp.output_epsilon),
        mp.to_appended("ez", mp.at_every(0.6, mp.output_efield_z)),
        until=200)
"""# Plotting the results
# Get a slice of the electric field data and display the results
eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.axis('off')
plt.show()

# Plot the scalar electric field Ez. Dark red - negative, white - zero, dark blue - positive
ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.show()
"""