from datetime import datetime

import re
import os
import json
from collections import defaultdict


def organize_data_by_mac(parsed_data):
    signal_by_mac = defaultdict()
    frequency_by_mac = defaultdict()
    ssid_by_mac = defaultdict()

    for entry in parsed_data:
        mac_address = entry["mac"]
        quality = entry["strength"]
        frequency = entry["f"]
        timestemp = entry["time"]
        ssid = entry["ssid"]
        if not signal_by_mac.get(mac_address, None):
            signal_by_mac[mac_address] = {}
        signal_by_mac[mac_address][timestemp] = quality

        if not frequency_by_mac.get(mac_address, None):
            frequency_by_mac[mac_address] = frequency

        if not ssid_by_mac.get(mac_address, None):
            ssid_by_mac[mac_address] = ssid

    return signal_by_mac, frequency_by_mac, ssid_by_mac


def parse_ap_scans_dir(scan_dir):
    regex_file_name = re.compile(
        r"(\d{2})-(\d{2})-(\d{4})_(\d{2})%3A(\d{2})_(\d{2})"
    )
    mac_pattern = re.compile(r"BSS\s([\da-fA-F:]+)")
    freq_pattern = re.compile(r"freq:\s(\d+)")
    signal_pattern = re.compile(r"signal:\s(-?\d+\.\d+)\s+dBm")
    ssid_pattern = re.compile(r"SSID: ([\w-]+)\n")

    parsed_data = []
    timestamp_list = []
    file_list = sorted(os.listdir(scan_dir))
    for file_name in file_list:
        file_path = os.path.join(scan_dir, file_name)

        if file_name == "timestamps.txt":
            with open(file_path, "r") as file:
                for line in file:
                    time_string = line.strip()
                    date_string = "2025-01-18"
                    timestamp = datetime.strptime(
                        f"{date_string} {time_string}",
                        "%Y-%m-%d %H:%M:%S",
                    )
                    timestamp_list.append(str(timestamp))
            continue

        match = regex_file_name.search(file_name)
        if match:
            day, month, year, hour, minute, second = map(
                int, match.groups()
            )
            dt = datetime(year, month, day, hour, minute, second)

        with open(file_path, "r") as file:
            current_mac = None
            current_freq = None
            current_signal = None
            current_ssid = None

            for line in file:
                mac_match = mac_pattern.search(line)
                freq_match = freq_pattern.search(line)
                signal_match = signal_pattern.search(line)
                ssid_match = ssid_pattern.search(line)

                if mac_match:
                    current_mac = mac_match.group(1)
                if freq_match:
                    current_freq = int(freq_match.group(1))
                if signal_match:
                    current_signal = float(signal_match.group(1))
                if ssid_match:
                    current_ssid = ssid_match.group(1)

                if all(
                    [
                        current_mac,
                        current_ssid,
                        current_freq is not None,
                        current_signal is not None,
                    ]
                ):
                    parsed_data.append(
                        {
                            "mac": current_mac,
                            "time": str(dt),
                            "strength": current_signal,
                            "f": current_freq,
                            "ssid": current_ssid,
                        }
                    )
                    current_mac = None
                    current_freq = None
                    current_signal = None
                    current_ssid = None

    return parsed_data, timestamp_list


if __name__ == "__main__":
    icon_run_dir = (
        "measured_data/Leipzig_tests/evaluation/icon_3/run_2"
    )
    icon_run_dir_data, icon_timestamp_list = parse_ap_scans_dir(
        icon_run_dir
    )

    signal_by_mac, frequency_by_mac, ssid_by_mac = (
        organize_data_by_mac(icon_run_dir_data)
    )

    signal_by_mac["timestamps"] = icon_timestamp_list

    icon_run = "/icon3_run2"

    if True:
        with open(
            icon_run_dir + icon_run + "_signal.json", "w"
        ) as jfile:
            json.dump(signal_by_mac, jfile, indent=4)

        with open(
            icon_run_dir + icon_run + "_frequency.json", "w"
        ) as jfile:
            json.dump(frequency_by_mac, jfile, indent=4)

        with open(
            icon_run_dir + icon_run + "_ssid.json", "w"
        ) as jfile:
            json.dump(ssid_by_mac, jfile, indent=4)







# Create .gitignore for Python projects

# Add requirements.txt for dependencies

# Fix timestamp parsing

# Improve plot formatting

# Add code comments

# Improve logging

# Fix coordinate bugs

# Fix regex patterns
