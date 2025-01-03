"""
R: Meassurement noise covariance matrix
    The dimension of the matrix is dependend of the number of 
    measurements per time step. That means in our case the
    number of APs
F: State-transition matrix. The dimension depends on the 
    dimension of the state vector. For this model we have only
    a free variable x. That means F has one dimesnion.
    y,v_x,v_y are constant
Q: Process noise covariance. The matrix dimesnion is definied by the
    state-transition matrix.
"""

import json

import numpy as np
import yaml
from scipy.optimize import curve_fit
import src_wifi_lib.wifi_plot_lib as wifi_plot


# Global definitions
export_results = False
config_file = (
    "measured_data/Leipzig_tests/evaluation/"
    "icon_1/kalman_data_export/icon1_run1_config.yaml"
)
with open(config_file) as c_file:
    config = yaml.load(c_file, Loader=yaml.FullLoader)


y = 0
Q = np.eye(1) * 0.1
R = np.eye(config["AP_n"]) * 50
F = np.array([1])


def log_dist_path_loss_func(distance, P0, d0, n):
    distance = np.maximum(distance, d0)
    P = P0 - 10 * n * np.log10(distance / d0)
    return P


def log_dist_path_loss_func_inverse(P, P0, d0, n):
    d = d0 * 10 ** ((P0 - P) / (10 * n))
    return d


def f(x):
    return np.array([x[0] + config["v_x"] * config["dt"]])


def h(x, APs):
    rssis = []
    for x_ap, y_ap in APs:
        d = np.sqrt((x[0] - x_ap) ** 2 + (y - y_ap) ** 2)
        rssi = (
            -10 * config["n"] * np.log10(d / config["d0"])
            + config["P0"]
        )
        rssis.append(rssi)
    return np.array(rssis)


def H_jacobian(x, APs):
    H = []
    for x_ap, y_ap in APs:
        d = np.sqrt((x[0] - x_ap) ** 2 + (y - y_ap) ** 2)
        H.append(
            [-10 * config["n"] * (x[0] - x_ap) / (d**2 * np.log(10))]
        )
    return np.array(H)


def e_kalman_filter_3(x, P, measurements):
    estimated_positions = []
    P_list = []
    for z in measurements:
        # Prediction step
        x = f(x)
        P = F @ P @ F.T + Q

        # Update step
        H = H_jacobian(x, config["APs"])
        y_til = z - h(x, config["APs"])
        S = H @ P @ H.T + R
        K = P @ H.T @ np.linalg.inv(S)
        x = x + K @ y_til
        P = (np.eye(1) - K @ H) @ P
        estimated_positions.append(x)
        P_list.append(P[0])
    return estimated_positions, P_list


if __name__ == "__main__":
    # Import and arrange data
    with open(
        (
            "measured_data/Leipzig_tests/evaluation/"
            "icon_1/kalman_data_export/icon1_run2_kalman.json"
        ),
        "r",
    ) as file:
        measurements_positions = json.load(file)

    signal_measurements = np.array(
        list(measurements_positions.values())
    )
    pos_expected = np.array(
        [float(entry) for entry in measurements_positions.keys()]
    )

    # Initialize Kalman Filter
    x_ini_calc = log_dist_path_loss_func_inverse(
        signal_measurements[0],
        config["P0"],
        config["d0"],
        config["n"],
    )
    x_ini = np.array([x_ini_calc])
    P_ini = np.eye(1)

    # Run Kalman Filter
    estimated_positions, P_list = e_kalman_filter_3(
        x_ini, P_ini, signal_measurements
    )

    # Plot and axport results
    wifi_plot.plot_single_kalman_error(
        signal_measurements, pos_expected, estimated_positions
    )
    if export_results:
        export_path = (
            "measured_data/Leipzig_tests/evaluation/"
            "icon_2/kalman_data_export/results_icon2_run2_kalman_snipped.json"
        )
        estimated_positions_export = [
            cal_pos[0] for cal_pos in estimated_positions
        ]
        export_results = {
            "measurements_pos": measurements_positions,
            "estimated_positions": estimated_positions_export,
            "error": pos_expected,
        }
        with open(export_path, "w") as jfile:
            json.dump(export_results, jfile, indent=4)





# Add comprehensive README documentation
