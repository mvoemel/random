import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('time_series.csv')

# Create a figure with subplots
fig, axs = plt.subplots(3, 2, figsize=(15, 12))

# Plot positions
axs[0, 0].plot(data['t'], data[' y_Dart'], label='Dart')
axs[0, 0].plot(data['t'], data[' y_Board'], label='Board')
axs[0, 0].set_title('Y-Position over Time')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Position (m)')
axs[0, 0].legend()
axs[0, 0].grid(True)

axs[0, 1].plot(data['t'], data[' z_Dart'], label='Dart')
axs[0, 1].plot(data['t'], data[' z_Board'], label='Board')
axs[0, 1].set_title('Z-Position over Time')
axs[0, 1].set_xlabel('Time (s)')
axs[0, 1].set_ylabel('Position (m)')
axs[0, 1].legend()
axs[0, 1].grid(True)

# Plot velocities
axs[1, 0].plot(data['t'], data[' vy_Dart'], label='Dart')
axs[1, 0].plot(data['t'], data[' vy_Board'], label='Board')
axs[1, 0].set_title('Y-Velocity over Time')
axs[1, 0].set_xlabel('Time (s)')
axs[1, 0].set_ylabel('Velocity (m/s)')
axs[1, 0].legend()
axs[1, 0].grid(True)

axs[1, 1].plot(data['t'], data[' vz_Dart'], label='Dart')
axs[1, 1].plot(data['t'], data[' vz_Board'], label='Board')
axs[1, 1].set_title('Z-Velocity over Time')
axs[1, 1].set_xlabel('Time (s)')
axs[1, 1].set_ylabel('Velocity (m/s)')
axs[1, 1].legend()
axs[1, 1].grid(True)

# Plot accelerations
axs[2, 0].plot(data['t'], data[' ay_Dart'], label='Dart')
axs[2, 0].plot(data['t'], data[' ay_Board'], label='Board')
axs[2, 0].set_title('Y-Acceleration over Time')
axs[2, 0].set_xlabel('Time (s)')
axs[2, 0].set_ylabel('Acceleration (m/s²)')
axs[2, 0].legend()
axs[2, 0].grid(True)

axs[2, 1].plot(data['t'], data[' az_Dart'], label='Dart')
axs[2, 1].plot(data['t'], data[' az_Board'], label='Board')
axs[2, 1].set_title('Z-Acceleration over Time')
axs[2, 1].set_xlabel('Time (s)')
axs[2, 1].set_ylabel('Acceleration (m/s²)')
axs[2, 1].legend()
axs[2, 1].grid(True)

plt.tight_layout()
plt.savefig('dart_physics_analysis.png')
plt.show()