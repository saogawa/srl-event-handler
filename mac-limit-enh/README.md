# SRL Event Handler: MAC Limit Enhancement

This repository offers scripts and configurations to improve MAC limit event management in SRLinux, focusing on detecting and addressing MAC address table overflows by automatically shutting down the affected subinterfaces.

## Components

- **[mac-limit-enh.py](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/mac-limit-enh.py):** Automates the detection and shutdown of subinterfaces exceeding MAC address limits.
- **[run-script-eh.py](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/run-script-eh.py):** Acts as an event handler, triggering `mac-limit-enh.py` under specific conditions.
- **[srl_cfg_event-handler.json](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/srl_cfg_event-handler.json):** Configures the event handler in SRLinux, detailing the instance, state, and executable script.
- **[srl_cfg_logging-file.json](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/srl_cfg_logging-file.json):** Sets logging parameters in SRLinux for capturing MAC limit events.

## How It Works

1. **Logging Configuration:** Configures system logging to capture MAC limit events.
2. **Event Handling:** Executes `run-script-eh.py` to periodically check and trigger `mac-limit-enh.py`.
3. **MAC Limit Enforcement:** `mac-limit-enh.py` identifies and shuts down subinterfaces reaching MAC address limits.

## Setup and Configuration

To deploy this enhancement:

1. Install the scripts in the designated directory on your SRLinux system.
2. Apply the provided JSON configurations.
3. Verify the event handler and logging setups are correctly capturing and managing MAC limit events.

This approach automates responses to MAC address table overflows, enhancing network stability and reliability.
