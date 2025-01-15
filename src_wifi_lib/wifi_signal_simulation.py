import matplotlib.pyplot as plt
import numpy as np
import wifi_pos_lib
import yaml

with open("src_wifi_lib/config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

config["N_x_y"] = config["N_x"] * config["N_y"]
config["dx"] = config["x_length"] / (config["N_x"] - 1)
config["dy"] = config["y_length"] / (config["N_y"] - 1)


def log_dist_path_loss_func(APs, point, P0=-30, d0=1, n=3):
    distance = np.linalg.norm(np.array(APs) - np.array(point))
    if distance < d0:
        distance = d0
    P = np.round(P0 - 10 * n * np.log10(distance / d0), 3)
    return P


def simulate_signal_strength(grid_points, APs, P0, d0, n):
    signal_strengths = np.zeros((len(APs), grid_points.shape[0]))

    for i, router in enumerate(APs):
        for j, point in enumerate(grid_points):
            signal_strengths[i, j] = log_dist_path_loss_func(
                router, point, P0, d0, n
            )

    np.savetxt(
        "signal_data_export/signal_strengths.csv",
        signal_strengths,
        delimiter=",",
        fmt="%.3f",
    )
    return signal_strengths


def get_signal_strength_noisy(signal_strengths, gaussian_sigma):
    signal_strengths_noisy = signal_strengths - np.random.normal(
        0, gaussian_sigma, signal_strengths.shape
    )
    np.savetxt(
        "signal_data_export/signal_strengths_noisy.csv",
        signal_strengths_noisy,
        delimiter=",",
        fmt="%.3f",
    )
    return signal_strengths_noisy


def get_measured_points(
    measured_points_x_start,
    measured_points_x_end,
    measured_points_y_start,
    measured_points_y_end,
    measured_points_n,
    dump_into_file=True,
):
    measured_points = list(
        zip(
            np.linspace(
                measured_points_x_start,
                measured_points_x_end,
                measured_points_n,
            ),
            np.linspace(
                measured_points_y_start,
                measured_points_y_end,
                measured_points_n,
            ),
        )
    )
    measured_points_index = []
    for points in measured_points:
        measured_points_index.append(
            np.where((grid_points == points).all(axis=1))[0][0]
        )
    if dump_into_file:
        np.savetxt(
            "signal_data_export/measured_points.csv",
            measured_points,
            delimiter=",",
            fmt="%.3f",
        )
        np.savetxt(
            "signal_data_export/measured_points_index.csv",
            measured_points_index,
            delimiter=",",
            fmt="%.3f",
        )
    return measured_points, measured_points_index


def get_measured_signal(
    measured_points_index,
    signal_data_clean,
    signal_data_noisy,
    dump_into_file=True,
):
    measured_points_signal_clean = np.zeros(
        [
            np.shape(signal_data_clean)[0],
            np.shape(measured_points_index)[0],
        ]
    )
    measured_points_signal_noisy = np.zeros(
        [
            np.shape(signal_data_noisy)[0],
            np.shape(measured_points_index)[0],
        ]
    )

    for i in range(np.shape(signal_data_noisy)[0]):
        measured_points_signal_clean[i] = signal_data_clean[i][
            measured_points_index
        ]
        measured_points_signal_noisy[i] = signal_data_noisy[i][
            measured_points_index
        ]

    if dump_into_file:
        np.savetxt(
            "signal_data_export/measured_points_signal_noisy.csv",
            measured_points_signal_noisy,
            delimiter=",",
            fmt="%.3f",
        )
        np.savetxt(
            "signal_data_export/measured_points_signal_clean.csv",
            measured_points_signal_clean,
            delimiter=",",
            fmt="%.3f",
        )
    return measured_points_signal_clean, measured_points_signal_noisy


if __name__ == "__main__":
    grid_x, grid_y, grid_points = wifi_pos_lib.span_space(
        config["N_x"],
        config["N_y"],
        config["x_length"],
        config["y_length"],
    )

    signal_strengths = simulate_signal_strength(
        grid_points,
        config["APs"],
        config["P0"],
        config["d0"],
        config["n"],
    )

    signal_strengths_noisy = get_signal_strength_noisy(
        signal_strengths, config["gaussian_sigma"]
    )

    measured_points, measured_points_index = get_measured_points(
        config["measured_points_x_start"],
        config["measured_points_x_end"],
        config["measured_points_y_start"],
        config["measured_points_y_end"],
        config["measured_points_n"],
    )

    measured_points_signal_clean, measured_points_signal_noisy = (
        get_measured_signal(
            measured_points_index,
            signal_strengths,
            signal_strengths_noisy,
        )
    )

    # with open("signal_data_export/config.yaml", "w") as file:
    #     yaml.dump(config, file)

    plt.show()
    wifi_pos_lib.plot_signal_field_model(
        config["N_x"],
        config["N_y"],
        grid_x,
        grid_y,
        signal_strengths_noisy,
        config["APs"],
        measured_points,
        config["measured_points_y_start"],
    )

    plt.plot(measured_points_signal_clean[0])










# Fix numpy array broadcasting

# Add type annotations
