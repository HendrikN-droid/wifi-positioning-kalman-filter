import json
from datetime import datetime
import numpy as np

import src_wifi_lib.wifi_plot_lib as wifi_plot

evaluation = "Kalman"
plot = False


def import_icon_data(in_path, file_name):
    signal_by_mac = {}

    with open(
        in_path + file_name + "_frequency.json", "r"
    ) as json_file:
        frequency_by_mac = json.load(json_file)

    with open(in_path + file_name + "_signal.json", "r") as json_file:
        signal_by_mac_raw = json.load(json_file)

    with open(in_path + file_name + "_ssid.json", "r") as json_file:
        ssid_by_mac = json.load(json_file)

    timestamps = [
        datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        for time in signal_by_mac_raw["timestamps"]
    ]
    del signal_by_mac_raw["timestamps"]

    for mac in signal_by_mac_raw:
        signal_by_mac[mac] = {
            datetime.strptime(key, "%Y-%m-%d %H:%M:%S"): value
            for key, value in signal_by_mac_raw[mac].items()
        }

    list_of_interest = []
    signal_by_mac_filter = {}
    for key, value in ssid_by_mac.items():
        if (
            value == "W07PICOM"
            or value == "6E-Test"
            or value == "W07PROBO"
        ):
            list_of_interest.append(key)
            signal_by_mac_filter[key] = dict(
                sorted(signal_by_mac[key].items())
            )

    # Mac Filter
    # 1. Macs which are better than one treshold
    if True:
        signal_by_mac_filter_filter = {}
        treshold = -75
        for mac in signal_by_mac_filter:
            if any(
                value > treshold
                for value in list(signal_by_mac_filter[mac].values())
            ):
                signal_by_mac_filter_filter[mac] = (
                    signal_by_mac_filter[mac]
                )
        signal_by_mac_filter = signal_by_mac_filter_filter

    # 2. Filter by Mac adress
    # M5085 f0:61:c0:6f:8a:f0
    # M5005 f0:61:c0:70:fa:f0
    # M5064 f0:61:c0:6f:51:50
    # M5004 f0:61:c0:70:32:50 # Interesting
    # M5002 f0:61:c0:70:fb:f0
    # M5083 f0:61:c0:6f:76:f0
    # M5006 f0:61:c0:70:57:b0
    if False:
        # Common mac addresses between icon1,2,3
        # mac_of_interest = ['f0:61:c0:70:fa:f4', 'f0:61:c0:6f:51:54',
        # '98:8f:00:44:1b:82', '44:12:44:42:54:74', 'f0:61:c0:6f:51:51',
        # 'f0:61:c0:70:fa:f1', '44:12:44:42:54:71']
        # Common mac addresses between icon1,2,3, threshold -75
        mac_of_interest = [
            "f0:61:c0:6f:51:51",
            "44:12:44:42:54:71",
            "44:12:44:42:b4:d4",
            "f0:61:c0:70:fa:f1",
            "f0:61:c0:6f:51:54",
            "f0:61:c0:6c:04:b1",
            "f0:61:c0:6f:8a:f4",
            "44:12:44:42:54:74",
            "f0:61:c0:70:fa:f4",
            "98:8f:00:44:1b:82",
            "f0:61:c0:6f:8a:f1",
            "f0:61:c0:6c:04:b4",
        ]
        # Interesting Macs Confluence
        # mac_of_interest = ["44:12:44:42:39:04", "f0:61:c0:6f:51:50", "64:60:38:01:b3:8a"]
        signal_by_mac_filter_filter_2 = {}
        for mac in mac_of_interest:
            if signal_by_mac_filter.get(mac, None):
                signal_by_mac_filter_filter_2[mac] = (
                    signal_by_mac_filter[mac]
                )
            else:
                print("MAC not included: ", mac)
        signal_by_mac_filter = signal_by_mac_filter_filter_2

    return (
        signal_by_mac_filter,
        frequency_by_mac,
        ssid_by_mac,
        timestamps,
    )


def normalize_data(data_by_mac, timestamps, time_based=True):
    general_start_time = datetime(2025, 1, 18, 14, 0, 0)
    v_x = 0.1
    data_by_mac_selection = {}

    for mac in data_by_mac.keys():
        for time in data_by_mac[mac]:
            if time_based:
                data_by_mac_selection[mac] = {
                    general_start_time + (time - timestamps[0]): value
                    for time, value in data_by_mac[mac].items()
                }
            else:
                data_by_mac_selection[mac] = {
                    np.round(
                        (time - timestamps[0]).total_seconds() * v_x,
                        2,
                    ): value
                    for time, value in data_by_mac[mac].items()
                }
    timestamps_normal = [
        general_start_time + (orignal_time - timestamps[0])
        for orignal_time in timestamps
    ]
    return data_by_mac_selection, timestamps_normal


def save_data_kalman(data, mac, export_path, offset_x):
    data_export = {}
    for key, value in data[mac].items():
        if key > 0:
            data_export[key + offset_x] = value
    with open(export_path, "w") as jfile:
        json.dump(data_export, jfile, indent=4)


if __name__ == "__main__":
    # Icon1
    icon1_run1_path = (
        "measured_data/Leipzig_tests/evaluation/" "icon_1/run_1/"
    )
    icon1_run2_path = (
        "measured_data/Leipzig_tests/evaluation/" "icon_1/run_2/"
    )
    icon1_run3_path = (
        "measured_data/Leipzig_tests/evaluation/" "icon_1/run_3/"
    )
    icon1_run4_path = (
        "measured_data/Leipzig_tests/evaluation/" "icon_1/run_4/"
    )
    # Icon2
    icon2_run1_path = (
        "measured_data/Leipzig_tests/evaluation/" "icon_2/run_1/"
    )
    icon2_run2_path = (
        "measured_data/Leipzig_tests/evaluation/" "icon_2/run_2/"
    )
    icon2_run3_path = (
        "measured_data/Leipzig_tests/evaluation/" "icon_2/run_3/"
    )
    icon2_run4_path = (
        "measured_data/Leipzig_tests/evaluation/" "icon_2/run_4/"
    )
    # Icon3
    icon3_run1_path = (
        "measured_data/Leipzig_tests/evaluation/" "icon_3/run_1/"
    )
    icon3_run2_path = (
        "measured_data/Leipzig_tests/evaluation/" "icon_3/run_2/"
    )

    if evaluation == "Icon1":
        (
            icon1_run1_data,
            icon1_run1_f,
            icon1_run1_ssid,
            icon1_run1_time,
        ) = import_icon_data(icon1_run1_path, file_name="icon1_run1")
        (
            icon1_run2_data,
            icon1_run2_f,
            icon1_run2_ssid,
            icon1_run2_time,
        ) = import_icon_data(icon1_run2_path, file_name="icon1_run2")
        (
            icon1_run3_data,
            icon1_run3_f,
            icon1_run3_ssid,
            icon1_run3_time,
        ) = import_icon_data(icon1_run3_path, file_name="icon1_run3")
        (
            icon1_run4_data,
            icon1_run4_f,
            icon1_run4_ssid,
            icon1_run4_time,
        ) = import_icon_data(icon1_run4_path, file_name="icon1_run4")
        if plot:
            wifi_plot.plot_quality_by_mac_subplots(
                icon1_run1_data,
                icon1_run1_f,
                icon1_run1_ssid,
                icon1_run1_time,
                icon1_run1_path,
            )
            wifi_plot.plot_quality_by_mac_subplots(
                icon1_run2_data,
                icon1_run2_f,
                icon1_run2_ssid,
                icon1_run2_time,
                icon1_run2_path,
            )
            wifi_plot.plot_quality_by_mac_subplots(
                icon1_run3_data,
                icon1_run3_f,
                icon1_run3_ssid,
                icon1_run3_time,
                icon1_run3_path,
            )
            wifi_plot.plot_quality_by_mac_subplots(
                icon1_run4_data,
                icon1_run4_f,
                icon1_run4_ssid,
                icon1_run4_time,
                icon1_run4_path,
            )

    if evaluation == "Icon2":
        (
            icon2_run1_data,
            icon2_run1_f,
            icon2_run1_ssid,
            icon2_run1_time,
        ) = import_icon_data(icon2_run1_path, file_name="icon2_run1")
        (
            icon2_run2_data,
            icon2_run2_f,
            icon2_run2_ssid,
            icon2_run2_time,
        ) = import_icon_data(icon2_run2_path, file_name="icon2_run2")
        (
            icon2_run3_data,
            icon2_run3_f,
            icon2_run3_ssid,
            icon2_run3_time,
        ) = import_icon_data(icon2_run3_path, file_name="icon2_run3")
        (
            icon2_run4_data,
            icon2_run4_f,
            icon2_run4_ssid,
            icon2_run4_time,
        ) = import_icon_data(icon2_run4_path, file_name="icon2_run4")

        icon2_run1_data_n, icon2_run1_time_n = normalize_data(
            icon2_run1_data, icon2_run1_time, time_based=False
        )
        icon2_run2_data_n, icon2_run2_time_n = normalize_data(
            icon2_run2_data, icon2_run2_time, time_based=False
        )
        icon2_run3_data_n, icon2_run3_time_n = normalize_data(
            icon2_run3_data, icon2_run3_time, time_based=False
        )
        icon2_run4_data_n, icon2_run4_time_n = normalize_data(
            icon2_run4_data, icon2_run4_time, time_based=False
        )

        icon2_all_run_n = [
            icon2_run3_data_n,
            icon2_run4_data_n,
        ]
        mac_of_interest = [
            "44:12:44:42:39:04",
            "98:8f:00:44:1b:82",
            "44:12:44:42:54:71",
            "44:12:44:42:54:74",
        ]

        export_path = "measured_data/Leipzig_tests/evaluation/icon_2/kalman_data_export/icon2_run4_kalman.json"

        wifi_plot.plot_icon_multi_run(
            mac_of_interest[0],
            icon2_all_run_n,
            icon2_run1_f,
            icon2_run1_time_n,
            time_dependent=False,
        )
        save_data_kalman(
            icon2_all_run_n[3],
            mac_of_interest[0],
            export_path,
            offset_x=6,
        )
        if False:
            wifi_plot.plot_quality_by_mac_subplots(
                icon2_run1_data,
                icon2_run1_f,
                icon2_run1_time,
                icon2_run1_path,
            )
            wifi_plot.plot_quality_by_mac_subplots(
                icon2_run2_data,
                icon2_run2_f,
                icon2_run2_time,
                icon2_run2_path,
            )
            wifi_plot.plot_quality_by_mac_subplots(
                icon2_run3_data,
                icon2_run3_f,
                icon2_run3_time,
                icon2_run3_path,
            )
            wifi_plot.plot_quality_by_mac_subplots(
                icon2_run4_data,
                icon2_run4_f,
                icon2_run4_time,
                icon2_run4_path,
            )

    if evaluation == "Icon3":
        (
            icon3_run1_data,
            icon3_run1_f,
            icon3_run1_ssid,
            icon3_run1_time,
        ) = import_icon_data(icon3_run1_path, file_name="icon3_run1")
        (
            icon3_run2_data,
            icon3_run2_f,
            icon3_run2_ssid,
            icon3_run2_time,
        ) = import_icon_data(icon3_run2_path, file_name="icon3_run2")

        icon3_run1_data_n, icon3_run1_time_n = normalize_data(
            icon3_run1_data, icon3_run1_time, time_based=False
        )
        icon3_run2_data_n, icon3_run2_time_n = normalize_data(
            icon3_run2_data, icon3_run2_time, time_based=False
        )
        icon3_all_run_n = [
            icon3_run1_data_n,
            icon3_run2_data_n,
        ]
        mac_of_interest = [
            "44:12:44:42:39:04",
            "98:8f:00:44:1b:82",
            "44:12:44:42:54:71",
            "44:12:44:42:54:74",
        ]

        export_path = "measured_data/Leipzig_tests/evaluation/icon_3/kalman_data_export/icon3_run2_kalman.json"

        # wifi_plot.plot_icon_multi_run(
        #     mac_of_interest[0],
        #     icon3_all_run_n,
        #     icon3_run1_f,
        #     icon3_run1_time_n,
        #     time_dependent = False
        # )
        save_data_kalman(
            icon3_all_run_n[1],
            mac_of_interest[0],
            export_path,
            offset_x=12,
        )
        # wifi_plot.plot_quality_by_mac_subplots(
        #     icon3_run1_data,
        #     icon3_run1_f,
        #     icon3_run1_time,
        #     icon3_run1_path,
        # )
        # wifi_plot.plot_quality_by_mac_subplots(
        #     icon3_run2_data,
        #     icon3_run2_f,
        #     icon3_run2_time,
        #     icon3_run2_path,
        # )

    # 2 Evaluation
    if evaluation == "Icon1_all":
        (
            icon1_run1_data,
            icon1_run1_f,
            icon1_run1_ssid,
            icon1_run1_time,
        ) = import_icon_data(icon1_run1_path, file_name="icon1_run1")
        (
            icon1_run2_data,
            icon1_run2_f,
            icon1_run2_ssid,
            icon1_run2_time,
        ) = import_icon_data(icon1_run2_path, file_name="icon1_run2")
        (
            icon1_run3_data,
            icon1_run3_f,
            icon1_run3_ssid,
            icon1_run3_time,
        ) = import_icon_data(icon1_run3_path, file_name="icon1_run3")
        (
            icon1_run4_data,
            icon1_run4_f,
            icon1_run4_ssid,
            icon1_run4_time,
        ) = import_icon_data(icon1_run4_path, file_name="icon1_run4")

        icon1_run1_data_n, icon1_run1_time_n = normalize_data(
            icon1_run1_data, icon1_run1_time, time_based=False
        )
        icon1_run2_data_n, icon1_run2_time_n = normalize_data(
            icon1_run2_data, icon1_run2_time, time_based=False
        )
        icon1_run3_data_n, icon1_run3_time_n = normalize_data(
            icon1_run3_data, icon1_run3_time, time_based=False
        )
        icon1_run4_data_n, icon1_run4_time_n = normalize_data(
            icon1_run4_data, icon1_run4_time, time_based=False
        )
        icon1_all_run_n = [
            icon1_run1_data_n,
            icon1_run2_data_n,
            icon1_run3_data_n,
            icon1_run4_data_n,
        ]
        mac_of_interest = [
            "44:12:44:42:39:04",
            "98:8f:00:44:1b:82",
            "44:12:44:42:54:71",
            "44:12:44:42:54:74",
        ]

        export_path = "measured_data/Leipzig_tests/evaluation/icon_1/kalman_data_export/icon1_run4_kalman.json"
        save_data_kalman(
            icon1_all_run_n[3], mac_of_interest[0], export_path
        )

    # 3 Evaluation
    if evaluation == "Run1":
        (
            icon1_run1_data,
            icon1_run1_f,
            icon1_run1_ssid,
            icon1_run1_time,
        ) = import_icon_data(icon1_run1_path, file_name="icon1_run1")
        icon1_run1_time[0] = icon1_run1_time[0]
        (
            icon2_run1_data,
            icon2_run1_f,
            icon2_run1_f,
            icon2_run1_time,
        ) = import_icon_data(icon2_run1_path, file_name="icon2_run1")
        (
            icon3_run1_data,
            icon3_run1_f,
            icon3_run1_f,
            icon3_run1_time,
        ) = import_icon_data(icon3_run1_path, file_name="icon3_run1")
        common_mac = set.intersection(
            set(icon1_run1_data.keys()),
            set(icon2_run1_data.keys()),
            set(icon3_run1_data.keys()),
        )
        del icon2_run1_time[0]

        icon1_run1_data_n, icon1_run1_time_n = normalize_data(
            icon1_run1_data, icon1_run1_time
        )
        icon2_run1_data_n, icon2_run1_time_n = normalize_data(
            icon2_run1_data, icon2_run1_time
        )
        icon3_run1_data_n, icon3_run1_time_n = normalize_data(
            icon3_run1_data, icon3_run1_time
        )
        icon_all_run1_data_n = [
            icon1_run1_data_n,
            icon2_run1_data_n,
            icon3_run1_data_n,
        ]
        mac_of_interest = [
            "44:12:44:42:39:04",
            "f0:61:c0:6f:51:50",
            "f0:61:c0:6f:51:54",
            "f0:61:c0:6f:8a:f4",
            "f0:61:c0:6f:8a:f1",
            "f0:61:c0:6f:8a:f1",
        ]
        # Interesting 1,4, 3
        wifi_plot.plot_icon_multi_run(
            mac_of_interest[0],
            icon_all_run1_data_n,
            icon1_run1_f,
            icon1_run1_time_n,
            time_dependent=True,
        )

    # 3 Evaluation
    if evaluation == "Run2":
        (
            icon1_run2_data,
            icon1_run2_f,
            icon1_run2_ssid,
            icon1_run2_time,
        ) = import_icon_data(icon1_run2_path, file_name="icon1_run2")

        (
            icon2_run2_data,
            icon2_run2_f,
            icon2_run2_f,
            icon2_run2_time,
        ) = import_icon_data(icon2_run2_path, file_name="icon2_run2")
        (
            icon3_run2_data,
            icon3_run2_f,
            icon3_run2_f,
            icon3_run2_time,
        ) = import_icon_data(icon3_run2_path, file_name="icon3_run2")
        common_mac = set.intersection(
            set(icon1_run2_data.keys()),
            set(icon2_run2_data.keys()),
            set(icon3_run2_data.keys()),
        )
        # wifi_plot.plot_quality_by_mac_subplots(
        #         icon1_run2_data,
        #         icon1_run2_f,
        #         icon1_run2_ssid,
        #         icon1_run2_time,
        #         icon1_run2_path,
        #     )
        # del icon2_run2_time[0]

        icon1_run2_data_n, icon1_run2_time_n = normalize_data(
            icon1_run2_data, icon1_run2_time
        )
        icon2_run2_data_n, icon2_run2_time_n = normalize_data(
            icon2_run2_data, icon2_run2_time
        )
        icon3_run2_data_n, icon3_run2_time_n = normalize_data(
            icon3_run2_data, icon3_run2_time
        )
        icon_all_run2_data_n = [
            icon1_run2_data_n,
            icon2_run2_data_n,
            icon3_run2_data_n,
        ]
        mac_of_interest = [
            "44:12:44:42:39:04",
            "98:8f:00:44:1b:82",
            "44:12:44:42:54:71",
            "44:12:44:42:54:74",
        ]
        # Interesting 1,4, 3
        wifi_plot.plot_icon_multi_run(
            mac_of_interest[0],
            icon_all_run2_data_n,
            icon1_run2_f,
            icon1_run2_time_n,
        )

    # 3 Evaluation
    if evaluation == "Run3":
        (
            icon1_run3_data,
            icon1_run3_f,
            icon1_run3_ssid,
            icon1_run3_time,
        ) = import_icon_data(icon1_run3_path, file_name="icon1_run3")

        (
            icon2_run3_data,
            icon2_run3_f,
            icon2_run3_f,
            icon2_run3_time,
        ) = import_icon_data(icon2_run3_path, file_name="icon2_run3")
        # common_mac = set.intersection(set(icon1_run3_data.keys()), set(icon2_run3_data.keys()))
        # wifi_plot.plot_quality_by_mac_subplots(
        #         icon1_run3_data,
        #         icon1_run3_f,
        #         icon1_run3_ssid,
        #         icon1_run3_time,
        #         icon1_run3_path,
        #     )
        # del icon2_run3_time[0]
        icon2_run3_data_n, icon2_run3_time_n = normalize_data(
            icon2_run3_data, icon2_run3_time
        )

        icon1_run3_data_n, icon1_run3_time_n = normalize_data(
            icon1_run3_data, icon1_run3_time
        )

        icon_all_run3_data_n = [
            icon1_run3_data_n,
            icon2_run3_data_n,
        ]
        mac_of_interest = [
            "44:12:44:42:39:04",
            "98:8f:00:44:1b:82",
            "44:12:44:42:54:71",
            "44:12:44:42:54:74",
        ]
        # Interesting 1,4, 3
        wifi_plot.plot_icon_multi_run(
            mac_of_interest[0],
            icon_all_run3_data_n,
            icon1_run3_f,
            icon1_run3_time_n,
            time_dependent=True,
        )

    if evaluation == "Kalman":
        with open(
            (
                "measured_data/Leipzig_tests/evaluation/icon_1/kalman_data_export/"
                "kalman_evaluation/results_icon1_run2_kalman.json"
            ),
            "r",
        ) as json_file:
            results_kalman_1 = json.load(json_file)

        with open(
            (
                "measured_data/Leipzig_tests/evaluation/icon_2/kalman_data_export/"
                "kalman_evaluation/results_icon2_run2_kalman_snipped.json"
            ),
            "r",
        ) as json_file:
            results_kalman_2 = json.load(json_file)

        with open(
            (
                "measured_data/Leipzig_tests/evaluation/icon_3/kalman_data_export/"
                "kalman_evaluation/results_icon3_run1_kalman_snipped.json"
            ),
            "r",
        ) as json_file:
            results_kalman_3 = json.load(json_file)

    wifi_plot.plot_multi_kalman_error(
        results_kalman_1, results_kalman_2, results_kalman_3
    )









