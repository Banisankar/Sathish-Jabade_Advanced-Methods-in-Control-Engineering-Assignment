import os
import csv
from datetime import datetime

class Logger:
    def __init__(self, system, controller_name, is_log_data=1):
        self.is_log_data = is_log_data
        self.system = system
        self.controller_name = controller_name.lower()
        self.start_time = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")

        self.data = []

        if self.is_log_data:
            self.filename = (
                f"{system.name}_{self.controller_name}_{self.start_time}__run01.csv"
            )
            self.folder = os.path.join("simdata", self.controller_name.upper(), "Init_angle_1.57_seed_1_Nactor_6")
            os.makedirs(self.folder, exist_ok=True)

    def log_data(self, t, state, obs, action, run_obj, accum_obj):
        row = [
            t,
            *state,
            *obs,
            run_obj,
            accum_obj,
            *action
        ]
        self.data.append(row)

    def save_to_csv(self):
        if self.is_log_data:
            header = [
                "t [s]",
                "x [m]",
                "y [m]",
                "alpha [rad]",
                "run_obj",
                "accum_obj",
                "v [m/s]",
                "omega [rad/s]"
            ]
            filepath = os.path.join(self.folder, self.filename)
            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                # Write 15 lines of metadata (fill with dummy info or parameters)
                writer.writerow(["System", self.system.name])
                writer.writerow(["Controller", self.controller_name])
                writer.writerow(["dt", 0.1])
                writer.writerow(["state_init", [-3.0, -3.0, 1.57]])
                writer.writerow(["Nactor", 6])
                writer.writerow(["pred_step_size_multiplier", 5.0])
                writer.writerow(["buffer_size", 25])
                writer.writerow(["run_obj_struct", "quadratic"])
                writer.writerow(["R1_diag", "[100, 100, 10, 0, 0]"])
                writer.writerow(["R2_diag", "[1, 10, 1, 0, 0]"])
                writer.writerow(["Ncritic", 25])
                writer.writerow(["gamma", 0.9])
                writer.writerow(["critic_period_multiplier", 1.0])
                writer.writerow(["critic_struct", "quad-mix"])
                writer.writerow(["actor_struct", "quad-nomix"])
                writer.writerow(header)
                writer.writerows(self.data)
