#!/bin/bash\
LOGFILE="wifi_signal_log.csv"\
\
echo "Timestamp,SSID,BSSID,Signal Strength (dBm),Frequency" > $LOGFILE\
\
while true; do\
    # Trigger a scan\
    sudo wpa_cli scan > /dev/null\
\
    # Wait for the scan to complete\
    sleep 5\
\
    # Fetch scan results\
    RESULTS=$(sudo wpa_cli scan_results)\
\
    # Parse and log the results\
    echo "$RESULTS" | tail -n +3 | while read -r line; do\
        BSSID=$(echo $line | awk '\{print $1\}')\
        FREQ=$(echo $line | awk '\{print $2\}')\
        SIGNAL=$(echo $line | awk '\{print $3\}')\
        SSID=$(echo $line | cut -d' ' -f5-)\
\
        echo "$(date),$SSID,$BSSID,$SIGNAL,$FREQ" >> $LOGFILE\
    done\
\
    sleep 60  # Wait before the next scan\
done\
}

