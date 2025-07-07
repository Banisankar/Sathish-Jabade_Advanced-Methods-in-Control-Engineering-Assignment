import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === File Paths (Make sure these 3 exist) ===
run_paths = [
    "simdata/Nominal/Init_angle_1.57_seed_1_Nactor_10/3wrobotNI_Nominal_2025-07-06_17h31m53s__run01.csv",
    "simdata/Nominal/Init_angle_1.57_seed_1_Nactor_10/3wrobotNI_Nominal_2025-07-06_17h31m53s__run02.csv",
    "simdata/Nominal/Init_angle_1.57_seed_1_Nactor_10/3wrobotNI_Nominal_2025-07-06_17h31m53s__run03.csv",
]
labels = ["Run 1", "Run 2", "Run 3"]

def load_clean_csv(path):
    with open(path, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("t [s]"):
            data_start = i
            break
    df = pd.read_csv(path, skiprows=data_start)
    df.columns = df.columns.str.strip().str.replace('"', '')
    df = df.dropna()
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()
    return df

# === Load data ===
dfs = [load_clean_csv(path) for path in run_paths]

# === Plot 1: Trajectory ===
plt.figure(figsize=(6, 5))
for df, label in zip(dfs, labels):
    plt.plot(df['x [m]'], df['y [m]'], label=label)
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Robot Trajectories vs Reference")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("nominal_trajectory.png")
plt.show()

# === Plot 2: Tracking Error ===
plt.figure(figsize=(6, 5))
for df, label in zip(dfs, labels):
    error = np.sqrt(df['x [m]']**2 + df['y [m]']**2)
    plt.plot(df['t [s]'], error, label=label)
plt.xlabel("Time [s]")
plt.ylabel("Tracking Error [m]")
plt.title("Tracking Errors Over Time")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("nominal_tracking_error.png")
plt.show()

# === Plot 3: Linear Velocity ===
plt.figure(figsize=(6, 5))
for df, label in zip(dfs, labels):
    plt.plot(df['t [s]'], df['v [m/s]'], label=label)
plt.xlabel("Time [s]")
plt.ylabel("v [m/s]")
plt.title("Linear Velocity vs Time")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("nominal_velocity.png")
plt.show()

# === Plot 4: Angular Velocity ===
plt.figure(figsize=(6, 5))
for df, label in zip(dfs, labels):
    plt.plot(df['t [s]'], df['omega [rad/s]'], label=label)
plt.xlabel("Time [s]")
plt.ylabel("omega [rad/s]")
plt.title("Angular Velocity vs Time")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("nominal_omega.png")
plt.show()
