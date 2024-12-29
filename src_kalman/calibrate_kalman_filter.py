import json

import matplotlib.pyplot as plt
import numpy as np
import yaml
from scipy.optimize import curve_fit

export_data = False


def log_dist_path_loss_func(distance, P0, d0, n):
    distance = np.maximum(distance, d0)
    P = P0 - 10 * n * np.log10(distance / d0)
    return P


def plot_data_fit(x_data, y_data, fitted_parameter):
    plt.figure(figsize=(8, 6))
    plt.plot(x_data, y_data, "o", label="calibration data")
    plt.plot(
        x_data,
        log_dist_path_loss_func(x_data, *fitted_parameter),
        "-",
        label="fitted curve",
    )
    plt.xlabel("position (m)")
    plt.ylabel("Signal strength (dBm)")
    plt.legend()
    plt.grid(True)
    plt.title("Curve fit: Signal strength and distance (y, L0, d0)")
    plt.show()


def fit_curve(data_x, data_y, initial_guess=[-30, 1, 2]):

    try:
        parameter, covariance = curve_fit(
            log_dist_path_loss_func, data_x, data_y, p0=initial_guess
        )
        print("Fitted Parameters:", parameter)
    except RuntimeError as e:
        print("Curve fitting failed:", e)
        return [], []
    return parameter, covariance


if __name__ == "__main__":
    with open(
        (
            "measured_data/Leipzig_tests/evaluation/icon_2/"
            "kalman_data_export/icon2_run2_kalman_snipped_n.json"
        ),
        "r",
    ) as file:
        measurements_pos_icon = json.load(file)
    measurements_icon = np.flip(
        np.array(list(measurements_pos_icon.values()))
    )
    x_exp = np.flip(
        np.array(
            [float(entry) for entry in measurements_pos_icon.keys()]
        )
    )

    plt.plot(x_exp, measurements_icon)
    plt.show()

    paramater, _ = fit_curve(x_exp, measurements_icon)
    plot_data_fit(x_exp, measurements_icon, paramater)

    if export_data:
        config_file = (
            "measured_data/Leipzig_tests/evaluation/icon_2"
            "/kalman_data_export/icon2_run2_config.yaml"
        )
        with open(config_file) as c_file:
            config = yaml.load(c_file, Loader=yaml.FullLoader)
            config["P0"] = float(paramater[0])
            config["d0"] = float(paramater[1])
            config["n"] = float(paramater[2])

        with open(config_file, "w") as c_file:
            yaml.dump(config, c_file)






