from iris import load_cube
import iris.plot as iplt
import numpy as np
import matplotlib.pyplot as plt
from os.path import exists
from time import sleep
from matplotlib.animation import FuncAnimation
import cartopy.crs as ccrs

# Define animation function (takes frame number as input)
def animate(num):
    # Don't proceed until this file exists
    while not exists('ICMSHh3b6+{:06d}.nc'.format(num)):
        sleep(1)

    print('Displaying ICMSHh3b6+{:06d}.nc'.format(num))

    # Load temperature data
    cube = load_cube('ICMSHh3b6+{:06d}.nc'.format(num), 'Temperature')[0,0,:,:]

    # If not first frame, clear previous contours
    if num != 0:
        ax.collections = []

    # Plot and set title
    iplt.contourf(cube, 20, levels=np.linspace(220.0, 275.0, 30), axes=ax)
    plt.title('{:06d}'.format(num))

# Set up figure
fig = plt.figure(figsize=(16,8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()
anim = FuncAnimation(fig, animate, interval=100)
plt.draw()
plt.show()
