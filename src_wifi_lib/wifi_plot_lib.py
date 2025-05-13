import numpy as np
import matplotlib.pyplot as plt


def plot_single_kalman_error(
    signal_measurements, position_expected, estimated_positions
):
    x_err = []
    for i in range(len(position_expected)):
        x_err.append(
            np.abs(position_expected[i] - estimated_positions[i][0])
        )
    fig, axes = plt.subplots(2, 1, figsize=(12, 12))

    ax1 = axes[0]
    ax2 = ax1.twinx()

    ax1.plot(
        position_expected,
        position_expected,
        label="True Position",
        color="blue",
    )
    ax1.plot(
        position_expected,
        [pos[0] for pos in estimated_positions],
        label="Estimated Position",
        color="red",
    )
    ax2.plot(
        position_expected,
        signal_measurements,
        label="Measurements (RSSI)",
        color="orange",
        linestyle="dashed",
    )

    ax1.set_xlabel("Exact position (m)")
    ax1.set_ylabel("Position (m)", color="blue")
    ax2.set_ylabel("RSSI (dBm)", color="orange")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax2.tick_params(axis="y", labelcolor="orange")

    ax1.legend(loc="upper left")
    ax2.legend(loc="lower right")
    ax1.set_title("Icon1 Run3: Position and RSSI")

    ax1.grid(True)
    axes[1].grid(True)
    axes[1].plot(
        position_expected,
        x_err,
        label="Position Error",
        color="purple",
    )
    axes[1].set_xlabel("Exact position (m)")
    axes[1].set_ylabel("Error (m)")
    axes[1].legend()
    plt.show()


def plot_multi_kalman_error(
    kalman_results_1, kalman_results_2, kalman_results_3
):

    fig, axes = plt.subplots(2, 1, figsize=(12, 12))

    ax1 = axes[0]
    # ax2 = ax1.twinx()
    results = [kalman_results_1, kalman_results_2, kalman_results_3]
    icon = 0
    for res in results:
        icon = icon + 1
        pos_expected = np.array(
            [float(entry) for entry in res["measurements_pos"].keys()]
        )[0:9]
        signals = np.array(
            [
                float(entry)
                for entry in res["measurements_pos"].values()
            ]
        )[0:9]
        # ax1.plot(
        #     pos_expected,
        #     [pos for pos in res["estimated_positions"]],
        #     label="Estimated Position",
        #     color="red",
        # )
        ax1.plot(
            signals,
            label=f"Icon{icon} signal",
        )

        ax1.set_xlabel("Samples")
        ax1.set_ylabel("RSSI (dBm)")
        ax1.tick_params(axis="y")

        # ax1.legend(loc="upper left")
        ax1.legend(loc="upper left")
        ax1.set_title(
            "Error and signal strength 2. run: Icon1, Icon2, Icon3"
        )

        ax1.grid(True)
        axes[1].grid(True)
        axes[1].plot(
            res["error"][0:9],
            label=f"Icon{icon} position error",
        )
        axes[1].set_xlabel("Samples")
        axes[1].set_ylabel("Error (m)")
        axes[1].legend()
    plt.show()


def plot_quality_by_mac_subplots(
    data_by_mac,
    data_f,
    data_ssid,
    timestamps,
    log_file_path,
    time_dependent=True,
):
    # AP Translation
    ap_translation = {
        "f0:61:c0:6f:8a:f0": "M5085",
        "f0:61:c0:70:fa:f0": "M5005",
        "f0:61:c0:6f:51:50": "M5064",
        "f0:61:c0:70:32:50": "M5004",
        "f0:61:c0:70:fb:f0": "M5002",
        "f0:61:c0:6f:76:f0": "M5083",
        "f0:61:c0:70:57:b0": "M5006",
    }

    # M5085 f0:61:c0:6f:8a:f0
    # M5005 f0:61:c0:70:fa:f0
    # M5064 f0:61:c0:6f:51:50
    # M5004 f0:61:c0:70:32:50 # Interesting
    # M5002 f0:61:c0:70:fb:f0
    # M5083 f0:61:c0:6f:76:f0
    # M5006 f0:61:c0:70:57:b0

    max_subplots = 4
    mac_addresses = list(data_by_mac.keys())
    num_macs = len(mac_addresses)
    num_figures = (num_macs + max_subplots - 1) // max_subplots

    for fig_index in range(num_figures):
        start_index = fig_index * max_subplots
        end_index = min(start_index + max_subplots, num_macs)

        fig, axes = plt.subplots(
            end_index - start_index,
            1,
            figsize=(15, 5 * (end_index - start_index)),
            sharex=True,
        )
        plt.suptitle(f"Icon1 1. Run")

        if end_index - start_index == 1:
            axes = [axes]

        for ax, mac_address in zip(
            axes, mac_addresses[start_index:end_index]
        ):
            data = data_by_mac[mac_address]
            quality_values = np.array(list(data.values()))
            time = list(data.keys())
            quality_values_std = np.round(np.std(quality_values), 2)
            print(mac_address)
            if time_dependent:
                ax.plot(
                    time,
                    quality_values,
                    marker="o",
                    linestyle="-",
                    label=f"{mac_address}, SSID: {data_ssid[mac_address]}\nf: {data_f[mac_address]}MHz",  # , Std: {quality_values_std} dBm", {ap_translation[mac_address]}
                )
                ax.axvline(
                    timestamps[0],
                    color="red",
                    linestyle=":",
                    label="0 m",
                )
                ax.axvline(
                    timestamps[1],
                    color="red",
                    linestyle="-.",
                    label="5 m",
                )
                ax.axvline(
                    timestamps[2],
                    color="red",
                    linestyle="--",
                    label="15 m",
                )
            else:
                ax.plot(
                    quality_values,
                    marker="o",
                    linestyle="-",
                    label=f"{mac_address}, Std: {quality_values_std} dBm",
                )
            ax.set_xlabel("Timestamp")
            ax.set_ylabel("dBm")
            ax.grid(True, which="both")
            ax.legend()
            ax.xaxis_date()
            time_format = "%H:%M:%S"
            ax.xaxis.set_major_formatter(
                mdates.DateFormatter(time_format)
            )

        plt.xticks(rotation=45)
    plt.show()


def plot_icon_multi_run(
    mac_of_interest,
    data_by_mac,
    data_f,
    timestamps,
    time_dependent=True,
):
    if time_dependent:
        vertical_lines = timestamps
        x_label = "timestamps"
    else:
        vertical_lines = [0, 5, 15]
        x_label = "distance [m]"
    i = 0
    for run in data_by_mac:
        i = i + 1
        data = run[mac_of_interest]
        quality_values = np.array(list(data.values()))
        x_data = list(data.keys())
        plt.plot(
            x_data,
            quality_values,
            marker="o",
            linestyle="-",
            label=f"Icon {i}",
        )
    vline_min, vline_max = plt.gca().get_ylim()
    plt.vlines(
        vertical_lines[0],
        vline_min,
        vline_max,
        color="red",
        linestyle=":",
        label="0 m",
    )
    plt.vlines(
        vertical_lines[1],
        vline_min,
        vline_max,
        color="red",
        linestyle="-.",
        label="5 m",
    )
    plt.vlines(
        vertical_lines[2],
        vline_min,
        vline_max,
        color="red",
        linestyle="--",
        label="15 m",
    )
    if not time_dependent:
        plt.vlines(
            7.45,
            vline_min,
            vline_max,
            color="green",
            linestyle="--",
            label="6 Ghz antenna; 7,45 m",
        )
    plt.suptitle(
        f"Run2; Signal of {mac_of_interest};  f:{data_f[mac_of_interest]}MHz"
    )
    plt.xlabel(x_label)
    plt.ylabel("Signal dBm")
    plt.grid(True, which="both")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()








# Update dependencies

# Improve initialization
