import numpy as np
from systems import Sys3WRobotNI
from simulator import Simulator
from logger import Logger

# Simulation settings
t0 = 0
t1 = 10
dt = 0.1
Nruns = 3
is_log_data = 1

for run in range(Nruns):
    print(f"\n▶️ Starting Run {run+1}/{Nruns}")

    # Initial state: [x, y, theta]
    state_init = np.array([-3.0, -3.0, 1.57])
    dim_state = 3
    dim_input = 2
    dim_output = 3
    dim_disturb = 0

    sys = Sys3WRobotNI(
        sys_type="diff_eqn",
        dim_state=dim_state,
        dim_input=dim_input,
        dim_output=dim_output,
        dim_disturb=dim_disturb
    )

    def lqr_controller(t, state):
        # Simple proportional controller (mock LQR behavior)
        goal = np.array([3.0, 3.0])
        pos = state[:2]
        heading = state[2]

        error = goal - pos
        distance = np.linalg.norm(error)
        angle_to_goal = np.arctan2(error[1], error[0])
        angle_error = angle_to_goal - heading

        v = 0.5 * distance
        omega = 2.0 * angle_error

        return np.array([v, omega])

    def closed_loop_rhs(t, state_full):
        state = state_full
        action = lqr_controller(t, state)
        sys.receive_action(action)
        return sys.closed_loop_rhs(t, state)

    simulator = Simulator(
        sys_type="diff_eqn",
        closed_loop_rhs=closed_loop_rhs,
        sys_out=sys.out,
        state_init=state_init,
        t0=t0,
        t1=t1,
        dt=dt
    )

    if is_log_data:
        logger = Logger(system=sys, controller_name="lqr", is_log_data=1)

    while simulator.t < t1:
        simulator.sim_step()
        t, state, obs, _ = simulator.get_sim_step_data()
        v_omega = lqr_controller(t, state)
        run_obj = np.linalg.norm(state[:2])  # simple cost
        accum_obj = run_obj + t  # cumulative mock cost

        if is_log_data:
            logger.log_data(t, state, obs, v_omega, run_obj, accum_obj)

    if is_log_data:
        logger.save_to_csv()
        print(f"✅ Run {run+1} saved.\n")
