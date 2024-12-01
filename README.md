# WiFi Positioning with Extended Kalman Filter

This repository implements WiFi-based indoor positioning using Extended Kalman Filtering techniques.

## Overview

The project uses WiFi signal strength (RSSI) measurements from multiple access points to estimate device position. An Extended Kalman Filter processes noisy measurements to provide smooth, accurate position estimates.

## Directory Structure

- `src_kalman/` - Kalman filter implementations
  - `kalman_filter.py` - Extended Kalman Filter with full state vector
  - `kalman_filter_fixed_v.py` - Kalman filter with fixed velocity assumption
  - `kalman_filter_fixed_v_fixed_y_measured_data.py` - Filter for measured WiFi data
  - `calibrate_kalman_filter.py` - Calibration tools for filter parameters
  - `evaluation_kalman_filter.py` - Evaluation and visualization routines

- `src_log_parser/` - Log file parsing utilities
  - `log_file_parser_lib.py` - Base parser library
  - `dlt_log_file_parser.py` - DLT (Diagnostic Log and Trace) parser
  - `wpa_log_file_parser.py` - WPA supplicant log parser

- `src_wifi_lib/` - WiFi signal processing libraries
  - `wifi_pos_lib.py` - Core positioning algorithms
  - `wifi_signal_simulation.py` - Signal strength simulation
  - `wifi_plot_lib.py` - Visualization utilities

- `src_wpa_supplicant/` - WPA supplicant control scripts

## Requirements

See `requirements.txt` for Python package dependencies.

## Usage

1. Collect WiFi signal strength data from multiple access points
2. Parse log files using the appropriate parser
3. Run Kalman filter on the measurements
4. Evaluate results and visualize position estimates

## Features

- Extended Kalman Filter implementation for nonlinear state estimation
- Multiple filter variants with different state assumptions
- Comprehensive signal strength simulation
- Log file parsing for DLT and WPA supplicant formats
- Visualization and evaluation tools
- Parameter calibration utilities

## License

Research and educational use.
