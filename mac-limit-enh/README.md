# SRL Event Handler: MAC Limit Enhancement

This repository contains a set of scripts and configurations designed to enhance the handling of MAC limit events in SRLinux. The primary focus is on detecting when the number of MAC addresses on a subinterface reaches its limit and automatically shutting down the subinterface to prevent further issues.

## Components

- **[mac-limit-enh.py](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/mac-limit-enh.py):** This Python script searches for exceeded MAC limit events in the specified log file. Upon finding such an event, it automatically shuts down the affected subinterface.

- **[run-script-eh.py](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/run-script-eh.py):** A Python script that serves as an event handler. It triggers `mac-limit-enh.py` based on specific conditions, such as the comparison between the current time and the last execution time of the event handler.

- **[srl_cfg_event-handler.json](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/srl_cfg_event-handler.json):** JSON configuration for setting up the event handler within SRLinux. It specifies the event handler instance, its administrative state, and the script to be executed.

- **[srl_cfg_logging-file.json](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/srl_cfg_logging-file.json):** JSON configuration for logging settings in SRLinux. It defines the log file parameters, including file rotation, size, and filters for capturing MAC limit events.

## How It Works

1. **Logging Configuration:** The system is configured to log MAC limit events to a specific file, as defined in `srl_cfg_logging-file.json`.

2. **Event Handling:** The `run-script-eh.py` script is periodically executed a specified external script. It uses the configuration specified in `srl_cfg_event-handler.json` to determine when to run.

3. **MAC Limit Enforcement:** Upon detecting a MAC limit event, `mac-limit-enh.py` is triggered periodicaly. This script then proceeds to check for new MAC limit events and shut down the affected subinterface to prevent any further issues related to MAC address overflow.

## Setup and Configuration

To implement this enhancement in your SRLinux environment, follow these steps:

1. Place the scripts in the appropriate directory on your SRLinux system.
2. Apply the JSON configurations to your system's configuration.
3. Ensure that the event handler and logging configurations are correctly set up to capture and handle MAC limit events.

This setup provides an automated response to potential network issues caused by MAC address table overflow, enhancing the stability and reliability of the network.
