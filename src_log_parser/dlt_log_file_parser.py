import re
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import yaml
from scipy.optimize import curve_fit

pattern = r"(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{6}).+WifiDiagnosticJobStubService: onSignalLevelChanged \[0\]\[(-\d+)\]"


def parse_dlt_log_file(log_file_path):
    signal_strength_dict = {}
    with open(log_file_path, "r") as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                timestamp_str = match.group(1)
                signal_strength = int(match.group(2))
                timestamp = datetime.strptime(
                    timestamp_str, "%Y/%m/%d %H:%M:%S.%f"
                )

                signal_strength_dict[timestamp] = signal_strength
    return signal_strength_dict


def plot_signals_path(signal_strength_dict_list):
    fig, axes = plt.subplots(3, 1, figsize=(12, 12))

    for i, ax in enumerate(axes):
        signal_strength_dict = signal_strength_dict_list[i]
        ax.plot(
            signal_strength_dict.keys(),
            signal_strength_dict.values(),
            marker="o",
            label=f"Signal strength {i+1}",
        )
        ax.set_ylabel("Signal strength (dBm)")
        ax.set_title(f"Test {i+1}")
        ax.grid(True)
        ax.legend()

    axes[-1].set_xlabel("Time")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


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


def log_dist_path_loss_func(distance, P0, d0, n):
    distance = np.maximum(distance, d0)
    P = P0 - 10 * n * np.log10(distance / d0)
    return P


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
    path_0 = "real_env_data/Jember_munich/1_ap_id_5/Filtered.txt"
    signal = parse_dlt_log_file(path_0)
    plt.plot(signal.values())
    plt.show()
    config_file = (
        "real_env_data/Jember_munich/1_ap/Validation/config.yaml"
    )
    log_file_path_1 = "real_env_data/Jember_munich/1_ap_id_1/1_test_run_fuzzy_Pacome/wifi_test_dynamic_15h05_22_L_27_41_ascII.txt"
    log_file_path_2 = "real_env_data/Jember_munich/1_ap_id_1/1_test_run_fuzzy_Pacome/wifi_test_dynamic_14h53_14_R_14_40_ascII.txt"
    log_file_path_3 = "real_env_data/Jember_munich/1_ap_id_1/0_run_testing/wifi_test_13h34_58_ascII.txt"

    sig_str_dict_1 = parse_dlt_log_file(log_file_path_1)
    sig_str_dict_2 = parse_dlt_log_file(log_file_path_2)
    sig_str_dict_3 = parse_dlt_log_file(log_file_path_3)

    signal_strength_dict_list = [
        sig_str_dict_1,
        sig_str_dict_2,
        sig_str_dict_3,
    ]
    # Define global paramter
    plot_signals_path(signal_strength_dict_list)
    # Snip signal values to perform curve fit
    # 1
    sig_str_dict_1_values = list(sig_str_dict_1.values())
    sig_str_1_max = np.max(sig_str_dict_1_values)
    sig_str_1_max_id = sig_str_dict_1_values.index(sig_str_1_max)
    sig_y = np.array(sig_str_dict_1_values[0 : sig_str_1_max_id + 1])
    sig_x = np.linspace(27, 1, len(sig_y))
    paramater_1, _ = fit_curve(sig_x, sig_y)
    plot_data_fit(sig_x, sig_y, paramater_1)

    # 2
    start_x = 14
    end_x = 1
    sig_str_dict_2_values = list(sig_str_dict_2.values())
    sig_str_2_max = np.max(sig_str_dict_2_values)
    sig_str_2_max_id = sig_str_dict_2_values.index(sig_str_2_max)
    sig_y = np.array(sig_str_dict_2_values[0 : sig_str_2_max_id + 1])
    sig_x = np.linspace(start_x, end_x, len(sig_y))
    paramater_2, _ = fit_curve(sig_x, sig_y)
    plot_data_fit(sig_x, sig_y, paramater_1)

    # 3
    start_x = 14
    end_x = 1
    sig_str_dict_3_values = list(sig_str_dict_3.values())
    sig_str_3_max = np.max(sig_str_dict_3_values)
    sig_str_3_max_id = sig_str_dict_3_values.index(sig_str_3_max)
    sig_y = np.array(sig_str_dict_3_values[0 : sig_str_3_max_id + 1])
    sig_x = np.linspace(start_x, end_x, len(sig_y))
    paramater_3, _ = fit_curve(sig_x, sig_y)

    if True:
        np.savetxt(
            "real_env_data/Jember_munich/1_ap/Validation/wifi_test_dynamic_15h05_22_L_27_41.csv",
            sig_str_dict_1_values[0:-7],
            delimiter=",",
            fmt="%.3f",
        )

        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config["P0"] = float(paramater_2[0])
            config["d0"] = float(paramater_2[1])
            config["n"] = float(paramater_2[2])
            config["v_x"] = (
                41
                / (
                    max(sig_str_dict_1.keys())
                    - min(sig_str_dict_1.keys())
                ).seconds
            )

        with open(config_file, "w") as f:
            yaml.dump(config, f)








# Optimize file I/O
