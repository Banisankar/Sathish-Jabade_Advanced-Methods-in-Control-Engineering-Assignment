import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

base_path = "simdata/MPC/Init_angle_1.57_seed_1_Nactor_6"
run_files = sorted([f for f in os.listdir(base_path) if f.endswith(".csv")])[:3]

colors = ['r', 'g', 'b']
labels = ['Run 1', 'Run 2', 'Run 3']

def load_clean_csv(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        header_line = next((i for i, line in enumerate(lines) if 't [s]' in line), None)
    if header_line is None:
        raise ValueError("Could not find header line in file.")
    df = pd.read_csv(file_path, skiprows=header_line)
    df.columns = df.columns.str.strip().str.replace('"', '')
    return df

# Plot 1: Trajectory
plt.figure()
for i, file in enumerate(run_files):
    df = load_clean_csv(os.path.join(base_path, file))
    plt.plot(df['x [m]'], df['y [m]'], label=labels[i], color=colors[i])
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("MPC: Trajectories")
plt.legend()
plt.grid()
plt.savefig("mpc_trajectory.png")
plt.show()

# Plot 2: Tracking Error
plt.figure()
for i, file in enumerate(run_files):
    df = load_clean_csv(os.path.join(base_path, file))
    error = np.sqrt(df['x [m]']**2 + df['y [m]']**2)
    plt.plot(df['t [s]'], error, label=labels[i], color=colors[i])
plt.xlabel("Time [s]")
plt.ylabel("Tracking Error [m]")
plt.title("MPC: Tracking Error Over Time")
plt.legend()
plt.grid()
plt.savefig("mpc_tracking_error.png")
plt.show()

# Plot 3: Linear Velocity
plt.figure()
for i, file in enumerate(run_files):
    df = load_clean_csv(os.path.join(base_path, file))
    plt.plot(df['t [s]'], df['v [m/s]'], label=labels[i], color=colors[i])
plt.xlabel("Time [s]")
plt.ylabel("v [m/s]")
plt.title("MPC: Linear Velocity Over Time")
plt.legend()
plt.grid()
plt.savefig("mpc_velocity.png")
plt.show()

# Plot 4: Angular Velocity
plt.figure()
for i, file in enumerate(run_files):
    df = load_clean_csv(os.path.join(base_path, file))
    plt.plot(df['t [s]'], df['omega [rad/s]'], label=labels[i], color=colors[i])
plt.xlabel("Time [s]")
plt.ylabel("omega [rad/s]")
plt.title("MPC: Angular Velocity Over Time")
plt.legend()
plt.grid()
plt.savefig("mpc_omega.png")
plt.show()
