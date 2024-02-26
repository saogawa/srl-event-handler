# SRL Event Handler: MAC Limit Enhancement

This repository offers scripts and configurations to improve MAC limit event management in SRLinux, focusing on detecting and addressing MAC address table overflows by automatically shutting down the affected subinterfaces.

## How It Works
1. **Logging Configuration:** Configures system logging to capture MAC limit events.
2. **Event Handling:** Executes `run-script-eh.py` to check the interval periodically and trigger external script, `mac-limit-enh.py`.
    1. **Calculate Time Difference:** It calculates the time difference between the current time and the last run time of the script. This involves parsing timestamps and converting them to seconds for comparison.
    2. **Read Input JSON:** The script reads an input JSON string, which includes paths, options (such as the interval between runs and the script to execute), and persistent data (like the last run time).
    3. **Determine Execution:** Based on the calculated time difference and the specified interval, it decides whether to execute the `mac-limit-enh.py` script. If the time difference is greater than or equal to the interval, the script is triggered.
    4. **Update Persistent Data:** It updates the persistent data with the current time as the new "last run time," ensuring that subsequent runs can calculate the correct time difference.
    5. **Generate Response:** The script generates a JSON response that includes actions to be taken (such as running the specified script) and the updated persistent data. This response can be used to trigger the actual execution of the `mac-limit-enh.py` script and to log the event handler's activity.

3. **MAC Limit Enforcement:** `mac-limit-enh.py` identifies and shuts down subinterfaces reaching MAC address limits.
    1. **Read Log File:** It starts by opening and reading a log file (`/var/log/srlinux/file/mac-limit`) line by line, where MAC limit events are logged.
    2. **Detect MAC Limit Events:** It searches each line for patterns indicating that the MAC address limit has been reached for a subinterface. This is done using regular expressions to match specific log entries.
    3. **Parse Interface Details:** Upon finding a matching entry, it extracts the interface and subinterface details from the log line.
    4. **Shutdown Subinterface:** It constructs a command to shut down the identified subinterface by setting its administrative state to disable. This command is then executed using the system call.
    5. **Log Modification:** The script modifies the original log line to indicate that the subinterface has been shut down due to exceeding the MAC limit. This new line replaces the original in the list of lines to be written back to the log file.
    6. **Write Back to Log File:** Finally, the modified list of lines (including the updated entries) is written back to the log file, effectively updating it with the actions taken by the script.


## Setup and Configuration

To deploy this enhancement:

1. Install the scripts in the designated directory on your SRLinux system.
2. Apply the provided JSON configurations.
3. Verify the event handler and logging setups are correctly capturing and managing MAC limit events.

This approach automates responses to MAC address table overflows, enhancing network stability and reliability.
