import numpy as np
import src_wifi_lib.wifi_pos_lib as wifi_pos_lib

data_path = "signal_data_export"
config = wifi_pos_lib.get_config(data_path)


Q = np.eye(4) * 0.1  # Process noise covariance
R = np.eye(3) * 1000  # Measurement noise covariance

F = np.array(
    [
        [1, 0, config["dt"], 0],
        [0, 1, 0, config["dt"]],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
)


def f(x):
    return np.array(
        [
            x[0] + x[2] * config["dt"],
            x[1] + x[3] * config["dt"],
            x[2],
            x[3],
        ]
    )


def h(x, APs):
    rssis = []
    for x_ap, y_ap in APs:
        d = np.sqrt((x[0] - x_ap) ** 2 + (x[1] - y_ap) ** 2)
        rssi = (
            -10 * config["n"] * np.log10(d / config["d0"])
            + config["P0"]
        )
        rssis.append(rssi)
    return np.array(rssis)


def H_jacobian(x, APs):
    H = []
    for x_ap, y_ap in APs:
        d = np.sqrt((x[0] - x_ap) ** 2 + (x[1] - y_ap) ** 2)
        H.append(
            [
                -10
                * config["n"]
                * (x[0] - x_ap)
                / (d**2 * np.log(10)),
                -10
                * config["n"]
                * (x[1] - y_ap)
                / (d**2 * np.log(10)),
                0,
                0,
            ]
        )
    return np.array(H)


def e_kalman_filter_1(x, P, measurements):
    estimated_positions = []
    for z in measurements:
        # Prediction step
        x = f(x)
        P = F @ P @ F.T + Q

        # Update step
        H = H_jacobian(x, config["APs"])
        y = z - h(x, config["APs"])
        S = H @ P @ H.T + R
        K = P @ H.T @ np.linalg.inv(S)
        x = x + K @ y
        P = (np.eye(4) - K @ H) @ P
        estimated_positions.append(x[:2])
    return estimated_positions


if __name__ == "__main__":
    (
        simulated_positions,
        measured_points_index,
        measured_points_value_noisy,
        measured_points_value_clean,
    ) = wifi_pos_lib.get_simulation_data_measured_points(data_path)

    measurements_car_noisy = np.transpose(measured_points_value_noisy)
    measurements_car_clean = np.transpose(measured_points_value_clean)

    x_ini = np.array([1.5, 6.5, 0.2, 0])
    P_ini = np.eye(4)
    estimated_positions = e_kalman_filter_1(
        x_ini, P_ini, measurements_car_noisy
    )

    distance_error = wifi_pos_lib.get_distance_array(
        estimated_positions, simulated_positions
    )
    wifi_pos_lib.plot_position_error(
        estimated_positions,
        simulated_positions,
        distance_error,
        config,
    )

    np.savetxt(
        data_path + "/ekf_full_state.csv",
        distance_error,
        delimiter=",",
        fmt="%.3f",
    )






# Add input validation

# Add statistics

# Apply code style

# Fix update equations

# Add cross-validation

# Fix alignment
