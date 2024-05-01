import re
import matplotlib.pyplot as plt
import numpy as np
from astropy.time import Time
from datetime import datetime

def extract_data(filename):
    data = {}

    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith('!') or line.strip() == '':
            continue  # Skip comment lines and blank lines

        parts = line.split()

        band = parts[0]
        ut_date = ' '.join(parts[1:4])  # Join UT Date parts
        time = parts[4]
        flux_value = float(parts[7])
        error_value = float(parts[9])

        key = (band, ut_date, time)
        value = (flux_value, error_value)

        data[key] = value

    return data

# Example usage
filename = 'cena_data.txt'
data_dict = extract_data(filename)

# For check the data_dict
# for key, value in data_dict.items():
#     band, ut_date, time = key
#     flux, error = value
#     print(f"Band: {band}, UT Date: {ut_date}, Time: {time}, Flux: {flux}, Error: {error}")

# Extract data for Band '1mm'
band_1mm_data = {
    key: value for key, value in data_dict.items() if key[0] == '1mm'
    }

# # Convert dates to MJD
# t = Time()
mjd = [datetime.strptime(index[1] + ' ' + index[2], '%d %b %Y %H:%M') for index in band_1mm_data.keys()]
mjd_iso = [date.strftime('%Y-%m-%dT%H:%M:%S.%f') for date in mjd]
flux = [value[0] for value in band_1mm_data.values()]
errors = [value[1] for value in band_1mm_data.values()]
mjd = Time(mjd_iso, format='isot').mjd

# Extract data for Band '870um'
band_870um_data = {
    key: value for key, value in data_dict.items() if key[0] == '850'
    }

mjd2 = [datetime.strptime(index[1] + ' ' + index[2], '%d %b %Y %H:%M') for index in band_870um_data.keys()]
mjd_iso2 = [date.strftime('%Y-%m-%dT%H:%M:%S.%f') for date in mjd2]
flux2 = [value[0] for value in band_870um_data.values()]
errors2 = [value[1] for value in band_870um_data.values()]
mjd2 = Time(mjd_iso2, format='isot').mjd

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Plotting 1mm band
ax.plot(mjd, flux, c='blue')
ax.errorbar(mjd, flux, yerr=errors, fmt='^', color='blue', markeredgecolor='blue', markerfacecolor='none', markersize=6, capsize=3)

# Plotting 870um band
ax.plot(mjd2, flux2, c='red')
ax.errorbar(mjd2, flux2, yerr=errors2, fmt='o', color='red', markeredgecolor='red', markerfacecolor='none', markersize=9, capsize=3)

# Set major tick and minor tick
major_x_ticks = np.arange(52000, 61001, 2000)
minor_x_ticks = np.arange(52000, 61001, 1000)
major_y_ticks = np.arange(0, 16, 5)
minor_y_ticks = np.arange(0, 16, 1)

ax.set_xticks(major_x_ticks)
ax.set_xticks(minor_x_ticks, minor=True)
ax.set_yticks(major_y_ticks)
ax.set_yticks(minor_y_ticks, minor=True)

# Set grid
ax.grid(axis='x', linestyle='--', which='both')

# # Add additional x-axis at the top of the figure with customized tick labels
# ax2 = ax.twiny()
# ax2.set_xlim(ax.get_xlim())  # Set the same limits as ax1
# new_tick_locations = np.linspace(49000, 60800, 25)  # Define new tick locations
# new_tick_labels = [f'{tick/1000:.1f}' for tick in new_tick_locations]  # Convert ticks to desired format
# ax2.set_xticks(new_tick_locations)
# ax2.set_xticklabels(new_tick_labels)
# ax2.xaxis.tick_top()  # Move the ticks to the top
# ax2.tick_params(axis='x', labelsize=8)  # Set smaller font size for ticks

plt.xlim([52000,60800])
plt.ylim([0,15.5])
ax.set_xlabel('MJD')
ax.set_ylabel('Database Flux (Jy)')

ax.set_title('Flux and MJD for Band 1 mm and 870 $\mu$m')

plt.show()