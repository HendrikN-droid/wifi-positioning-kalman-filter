import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import re
from datetime import datetime
import matplotlib.dates as mdates


def parse_log_file_unknwon_0(log_file_path):
    pattern = re.compile(
        r"\[(.*?)\] (\S+) connected\s+Quality=([-]?\d+) dBm\s+Freq=(\d+)+\s+Channel=\d+\s+Bitrate=([\d.]+) MBit/s"
    )
    parsed_data = []

    with open(log_file_path, "r") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                timestamp = match.group(1)
                timestamp_conv = datetime.strptime(
                    timestamp, "%Y-%m-%d %H:%M:%S.%f"
                )
                mac_address = match.group(2)
                quality = float(match.group(3))
                frequency = int(match.group(4))
                bitrate = float(match.group(5))
                parsed_data.append(
                    {
                        "mac": mac_address,
                        "time": timestamp_conv,
                        "strength": quality,
                        "f": frequency,
                    }
                )

    return parsed_data


def parse_log_file_wpa(log_file_path):
    pattern = re.compile(
        r"(\d+\.\d+): wlan0: \d+: ([\da-fA-F:]+) .*? level=([-]?\d+) freq=(\d+)"
    )
    parsed_data = []
    with open(log_file_path, "r") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                timestamp = datetime.fromtimestamp(
                    float(match.group(1))
                )
                parsed_data.append(
                    {
                        "mac": match.group(2),
                        "time": timestamp,
                        "strength": int(match.group(3)),
                        "f": int(match.group(4)),
                    }
                )
    return parsed_data






# Optimize covariance updates
