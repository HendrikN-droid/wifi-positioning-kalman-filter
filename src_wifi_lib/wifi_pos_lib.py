import matplotlib.pyplot as plt
import numpy as np
import yaml


def span_space(N_x, N_y, x_length, y_length):
    grid_x, grid_y = np.meshgrid(
        np.linspace(0, x_length, N_x), np.linspace(0, y_length, N_y)
    )
    grid_points = np.c_[grid_x.ravel(), grid_y.ravel()]
    return grid_x, grid_y, grid_points


def get_config(path):
    with open(f"{path}/config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def get_distance_array(array_x, array_y):
    distance_array_len = len(array_x)
    distance_array = np.empty(distance_array_len)

    for i in range(distance_array_len):
        distance_array[i] = np.linalg.norm(array_x[i] - array_y[i])

    return distance_array


def get_simulation_data_measured_points(path):
    measured_points_value_clean = np.loadtxt(
        f"{path}/measured_points_signal_clean.csv", delimiter=","
    )
    measured_points_value_noisy = np.loadtxt(
        f"{path}/measured_points_signal_noisy.csv", delimiter=","
    )
    measured_points = np.loadtxt(
        f"{path}/measured_points.csv", delimiter=","
    )
    measured_points_index = np.loadtxt(
        f"{path}/measured_points_index.csv", delimiter=","
    )
    return (
        measured_points,
        measured_points_index,
        measured_points_value_noisy,
        measured_points_value_clean,
    )


def plot_signal_field(
    N_x, N_y, grid_x, grid_y, signal_strengths, access_points
):
    fig, axes = plt.subplots(1, len(access_points), figsize=(24, 8))

    for i, router in enumerate(access_points):
        cs = axes[i].contourf(
            grid_x, grid_y, signal_strengths[i, :].reshape(N_y, N_x)
        )  # , levels=50, cmap='viridis')
        fig.colorbar(cs, ax=axes[i], label="Signal Strength (dBm)")
        axes[i].set_title(f"Signal Strength Router {i+1} {router}")
        axes[i].set_xlabel("x (m)")
        axes[i].set_ylabel("y (m)")

    plt.tight_layout()
    plt.show()


def plot_signal_field_noise(
    N_x,
    N_y,
    grid_x,
    grid_y,
    signal_strengths,
    signal_strengths_noisy,
    APs,
    measured_points,
):
    aps_x, aps_y = zip(*APs)
    measured_points_x, measured_points_y = zip(*measured_points)

    fig, axes = plt.subplots(2, len(APs), figsize=(20, 10))

    for i, router in enumerate(APs):
        cs = axes[0, i].contourf(
            grid_x, grid_y, signal_strengths[i, :].reshape(N_x, N_y)
        )
        fig.colorbar(cs, ax=axes[0, i], label="Signal Strength (dBm)")
        axes[0, i].set_title(f"Signal Strength Router {i+1} {router}")
        axes[0, i].set_xlabel("x (m)")
        axes[0, i].set_ylabel("y (m)")
        axes[0, i].scatter(aps_x, aps_y, color="green")
        axes[0, i].plot(
            aps_x + (aps_x[0],), aps_y + (aps_y[0],), "b-"
        )
        axes[0, i].scatter(
            measured_points_x, measured_points_y, color="red"
        )

        cs = axes[1, i].contourf(
            grid_x,
            grid_y,
            signal_strengths_noisy[i, :].reshape(N_x, N_y),
        )
        fig.colorbar(cs, ax=axes[1, i], label="Signal Strength (dBm)")
        axes[1, i].set_title(
            f"Signal Strength Noisy Router {i+1} {router}"
        )
        axes[1, i].set_xlabel("x (m)")
        axes[1, i].set_ylabel("y (m)")

    plt.tight_layout()
    plt.show()


def plot_signal_field_model(
    N_x,
    N_y,
    grid_x,
    grid_y,
    signal_strengths,
    APs,
    measured_points,
    hline_y,
):
    aps_x, aps_y = zip(*APs)
    measured_points_x, measured_points_y = zip(*measured_points)
    txt_points = [
        "  t_0",
        "  t_1",
        "  t_2",
        "  t_3",
        "  t_4",
        "  t_5",
        "  t_6",
        "  t_7",
        "  t_8",
        "  t_9",
        "",
    ]
    signal_strengths_min = np.min(signal_strengths)
    signal_strengths_max = np.max(signal_strengths)

    fig, axes = plt.subplots(1, len(APs), figsize=(30, 5))

    if len(APs) == 1:
        cs = axes.contourf(
            grid_x,
            grid_y,
            signal_strengths[0, :].reshape(N_y, N_x),
            vmin=signal_strengths_min,
            vmax=signal_strengths_max,
        )
        fig.colorbar(
            cs,
            ax=axes,
            label="Signal Strength (dBm)",
        )
        axes.set_title("Signal Strength Router")
        axes.set_xlabel("x (m)")
        axes.set_ylabel("y (m)")
        axes.scatter(aps_x, aps_y, color="red")
        axes.plot(aps_x + (aps_x[0],), aps_y + (aps_y[0],), "b-")
        axes.axhline(
            y=hline_y, color="r", linestyle="--", linewidth=2
        )
        axes.annotate("Icon Path", (0.1, 5.1), fontsize=15)
    else:
        for i, router in enumerate(APs):
            cs = axes[i].contourf(
                grid_x,
                grid_y,
                signal_strengths[i, :].reshape(N_y, N_x),
                vmin=signal_strengths_min,
                vmax=signal_strengths_max,
            )
            fig.colorbar(
                cs,
                ax=axes[i],
                label="Signal Strength (dBm)",
            )
            axes[i].set_title(
                f"Signal Strength Router {i+1} {router}"
            )
            axes[i].set_xlabel("x (m)")
            axes[i].set_ylabel("y (m)")
            axes[i].scatter(aps_x, aps_y, color="red")
            axes[i].plot(
                aps_x + (aps_x[0],), aps_y + (aps_y[0],), "b-"
            )
            axes[i].axhline(
                y=hline_y, color="r", linestyle="--", linewidth=2
            )
            axes[i].annotate("Icon Path", (0.1, 5.1), fontsize=15)
            # axes[i].scatter(measured_points_x, measured_points_y, color="red")
            # for j, txt in enumerate(txt_points):
            #     axes[i].annotate(txt, (measured_points_x[j], measured_points_y[j]))

    plt.tight_layout()
    plt.show()


def plot_position_error(
    estimated_positions, simulated_positions, distance_error, config
):
    estimated_positions_x, estimated_positions_y = zip(
        *estimated_positions
    )
    simulated_positions_x, simulated_positions_y = zip(
        *simulated_positions
    )
    distance_error_mean = np.round(np.mean(distance_error), 2)
    distance_error_mean_20 = np.round(np.mean(distance_error[50:]), 2)
    estimated_pos_x_error_mean = np.round(
        np.mean(
            np.abs(
                np.array(estimated_positions_x)
                - np.array(simulated_positions_x)
            )
        ),
        2,
    )
    estimated_pos_y_error_mean = np.round(
        np.mean(
            np.abs(
                np.array(estimated_positions_y)
                - np.array(simulated_positions_y)
            )
        ),
        2,
    )
    fig, axes = plt.subplots(3, 1, figsize=(20, 10))
    # plt.suptitle(
    #     "Extended Kalman Filter; state vector x:= [x, y]; assumptions: v_x := 0.1 m/s, v_y := 0 m/s"
    # )
    plt.suptitle("Extended Kalman Filter; state vector x:= [x, y]")

    axes[0].scatter(
        estimated_positions_x,
        estimated_positions_y,
        s=20,
        c="blue",
        marker="o",
        label="Estimated Positions",
    )
    axes[0].scatter(
        simulated_positions_x,
        simulated_positions_y,
        s=20,
        c="red",
        marker="x",
        label="Simulated Positions",
    )

    axes[0].set_xlabel("x position [m]")
    axes[0].set_ylabel("y position [m]")
    axes[0].legend(loc=2)

    axes[1].scatter(
        np.linspace(1, len(distance_error), len(distance_error)),
        distance_error,
        s=20,
        c="blue",
        marker="o",
        label="Distance Error [m], euclidean norm",
    )
    axes[1].axhline(
        y=distance_error_mean,
        linestyle="-",
        label=f"mean(E) = {distance_error_mean} m",
    )
    axes[1].set_xlabel("Number of iteration")
    axes[1].set_ylabel("Error [m]")
    axes[1].legend(loc=2)

    # Create a subplot for the table
    axes[2].axis("off")  # Hide the subplot's axes

    # Data for the table
    table_data = [
        [
            "Geometric parameter",
            "Value",
            "Simulation parameter",
            "Value",
            "Positioning results",
            "Value",
        ],
        [
            "x length",
            str(config["x_length"]) + " m",
            "Reference signal strength P0",
            str(config["P0"]) + " dBm",
            "Mean distance error",
            f"{distance_error_mean} m",
        ],
        [
            "y length",
            str(config["y_length"]) + " m",
            "Reference length d0",
            str(config["d0"]) + " m",
            "Mean distance error (excl. first 50 samples)",
            f"{distance_error_mean_20} m",
        ],
        [
            "Access points",
            str(config["APs"]) + " m",
            "Path loss exponent",
            config["n"],
            "Mean x error",
            f"{estimated_pos_x_error_mean} m",
        ],
        [
            "Car start point",
            f"[{config['measured_points_x_start']}, {config['measured_points_y_start']}] m",
            "Gaussian standard deviation",
            f"{config['gaussian_sigma']} dB",
            "Mean y error",
            f"{estimated_pos_y_error_mean} m",
        ],
        [
            "Car end point",
            f"[{config['measured_points_x_end']}, {config['measured_points_y_end']}] m",
            "",
            "",
            "",
            "",
        ],
    ]

    # Add table to the third subplot
    table = axes[2].table(
        cellText=table_data,
        loc="center",
        cellLoc="center",
        colWidths=[0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
    )
    # Set the first row to a gray color
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # i==0 is the first row
            cell.set_facecolor("lightgray")

    # Adjust layout to make space for the table and plots
    plt.subplots_adjust(hspace=0.25)  #
    plt.show()
    return 0


def plot_position_error_compare(path, config):
    dist_error_ekf_full_state = np.loadtxt(
        f"{path}/ekf_full_state.csv", delimiter=","
    )
    dist_error_ekf_fixed_v = np.loadtxt(
        f"{path}/ekf_fixed_v.csv", delimiter=","
    )
    dist_error_ekf_fixed_v_fixed_y = np.loadtxt(
        f"{path}/ekf_fixed_v_fixed_y.csv", delimiter=","
    )

    dist_error_ekf_full_state_mean = np.round(
        np.mean(dist_error_ekf_full_state), 2
    )
    dist_error_ekf_full_state_mean_20 = np.round(
        np.mean(dist_error_ekf_full_state[50:]), 2
    )
    dist_error_ekf_fixed_v_mean = np.round(
        np.mean(dist_error_ekf_fixed_v), 2
    )
    dist_error_ekf_fixed_v_mean_20 = np.round(
        np.mean(dist_error_ekf_fixed_v[50:]), 2
    )
    dist_error_ekf_fixed_v_fixed_y_mean = np.round(
        np.mean(dist_error_ekf_fixed_v_fixed_y), 2
    )
    dist_error_ekf_fixed_v_fixed_y_mean_20 = np.round(
        np.mean(dist_error_ekf_fixed_v_fixed_y[50:]), 2
    )

    fig, axes = plt.subplots(2, 1, figsize=(20, 10))
    plt.suptitle("Comparison of different EKF state vectors")

    axes[0].plot(
        np.linspace(
            1,
            len(dist_error_ekf_full_state),
            len(dist_error_ekf_full_state),
        ),
        dist_error_ekf_full_state,
        "--bx",
        label="EKF x =[x, y, v_x, v_y]",
        linewidth=1,
    )
    axes[0].plot(
        np.linspace(
            1,
            len(dist_error_ekf_fixed_v),
            len(dist_error_ekf_fixed_v),
        ),
        dist_error_ekf_fixed_v,
        "--rx",
        label="EKF x =[x, y]",
        linewidth=1,
    )
    axes[0].plot(
        np.linspace(
            1,
            len(dist_error_ekf_fixed_v_fixed_y),
            len(dist_error_ekf_fixed_v_fixed_y),
        ),
        dist_error_ekf_fixed_v_fixed_y,
        "--yx",
        label="EKF x =[x]",
        linewidth=1,
    )
    axes[0].set_xlabel("Number of iteration")
    axes[0].set_ylabel("Error [m]")
    axes[0].legend(loc=2)
    axes[0].legend()

    # Create a subplot for the table
    axes[1].axis("off")  # Hide the subplot's axes

    # Data for the table
    table_data = [
        [
            "Geometric parameter",
            "Value",
            "Simulation parameter",
            "Value",
            "Positioning results",
            "x =[x, y, v_x, v_y]",
            "x =[x, y]",
            "x =[x]",
        ],
        [
            "x length",
            str(config["x_length"]) + " m",
            "Reference signal strength P0",
            str(config["P0"]) + " dBm",
            "Mean distance error",
            f"{dist_error_ekf_full_state_mean} m",
            f"{dist_error_ekf_fixed_v_mean} m",
            f"{dist_error_ekf_fixed_v_fixed_y_mean} m",
        ],
        [
            "y length",
            str(config["y_length"]) + " m",
            "Reference length d0",
            str(config["d0"]) + " m",
            "Mean distance error (excl. first 50 samples)",
            f"{dist_error_ekf_full_state_mean_20} m",
            f"{dist_error_ekf_fixed_v_mean_20} m",
            f"{dist_error_ekf_fixed_v_fixed_y_mean_20} m",
        ],
        [
            "Access points",
            str(config["APs"]) + " m",
            "Path loss exponent",
            config["n"],
            "",
            "",
            "",
            "",
        ],
        [
            "Car start point",
            f"[{config['measured_points_x_start']}, {config['measured_points_y_start']}] m",
            "Gaussian standard deviation",
            f"{config['gaussian_sigma']} dB",
            "",
            "",
            "",
            "",
        ],
        [
            "Car end point",
            f"[{config['measured_points_x_end']}, {config['measured_points_y_end']}] m",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
    ]

    # Add table to the third subplot
    table = axes[1].table(
        cellText=table_data,
        loc="center",
        cellLoc="center",
        colWidths=[0.125, 0.125, 0.125, 0.125, 0.25, 0.1, 0.1, 0.1],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    # Set the first row to a gray color
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # i==0 is the first row
            cell.set_facecolor("lightgray")

    # Adjust layout to make space for the table and plots
    plt.subplots_adjust(hspace=0.25)  #
    plt.show()
    return 0










# Reduce memory usage
