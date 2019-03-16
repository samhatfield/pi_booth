from iris import load_cube
import iris.plot as iplt
from iris.analysis import Linear
import numpy as np
import matplotlib.pyplot as plt
from os.path import exists
from time import sleep
from matplotlib.animation import FuncAnimation
import cartopy.crs as ccrs
from datetime import datetime, timedelta

expid="h467"

inferno = plt.get_cmap("inferno")

startdate = datetime(2017,1,1)

abingdon = (-1.29,51.67)
abingdon_gridpoint = (20,191)

ann = None

# Define animation function (takes frame number as input)
def animate(num):
    # Don't proceed until this file exists
    while not exists('ICMSH{}+{:06d}.nc'.format(expid, num)):
        print('ICMSH{}+{:06d}.nc doesn\'t exist'.format(expid, num))
        sleep(1)

    print('Displaying ICMSH{}+{:06d}.nc'.format(expid, num))

    # Load temperature data
    temp_cube = load_cube('ICMSH{}+{:06d}.nc'.format(expid, num), 'Temperature')[0,0,:,:]

    # If not first frame, clear previous contours
    if num != 0:
        ax1.collections = []
        ax2.collections = []

    # Plot and set title
    iplt.contourf(temp_cube, levels=np.linspace(220.0, 320.0, 20), axes=ax1, cmap=inferno)
    iplt.contourf(temp_cube, levels=np.linspace(220.0, 320.0, 20), axes=ax2, cmap=inferno)
    abingdon_temp = temp_cube.data[abingdon_gridpoint[0], abingdon_gridpoint[1]] - 273.0
    ann.set_text("Abingdon: {:.0f}°C".format(abingdon_temp))
    plt.suptitle('Temperature {:%Y-%m-%d %H:%M}'.format(startdate+timedelta(hours=num)))

# Set up figure
us_proj = ccrs.Orthographic(central_latitude=10, central_longitude=-95)
uk_proj = ccrs.Orthographic(central_latitude=50.0)

fig = plt.figure(figsize=(20,12))
ax1 = plt.subplot(121, projection=us_proj)
ax2 = plt.subplot(122, projection=uk_proj)

transform = ccrs.PlateCarree()._as_mpl_transform(ax2)

ax1.set_global()
ax2.set_global()
plt.tight_layout()
ax1.coastlines()
ax2.coastlines()

ax2.plot(abingdon[0], abingdon[1], 'ow', transform=ccrs.PlateCarree())
ann = ax2.annotate("Test", xy=(abingdon[0], abingdon[1]+3.0), xycoords=transform, color="white",
                   ha="center", fontsize=18)

anim = FuncAnimation(fig, animate, interval=100)
plt.draw()
plt.show()
