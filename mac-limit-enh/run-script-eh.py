import sys
import json
import time

def calculate_time_difference(current_time, last_run_time):
    """
    Calculates the time difference in seconds between two timestamps.
    Both timestamps are in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
    """
    def parse_time(time_str):
        """
        Parses a timestamp string into its components.
        """
        date, time = time_str.split('T')
        year, month, day = map(int, date.split('-'))
        hour, minute, second = map(int, time.split(':'))
        return year, month, day, hour, minute, second

    def convert_to_seconds(year, month, day, hour, minute, second):
        """
        Converts time components into total seconds from a base time.
        Note: Simplified conversion, does not account for varying month lengths or leap years.
        """
        return second + minute * 60 + hour * 3600 + day * 86400 + month * 2592000 + year * 31104000

    current_time_parsed = parse_time(current_time)
    last_run_time_parsed = parse_time(last_run_time)

    current_time_seconds = convert_to_seconds(*current_time_parsed)
    last_run_time_seconds = convert_to_seconds(*last_run_time_parsed)

    return current_time_seconds - last_run_time_seconds

def event_handler_main(in_json_str):
    """
    Main handler function that processes input JSON string and determines
    if a specified script should be executed based on the time interval.
    """
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]
    persist = in_json.get("persistent-data", [{}])
    persist = persist[0] if persist else [{}]
    
    local_time = time.localtime()
    current_time = "%04d-%02d-%02dT%02d:%02d:%02d" % (local_time[0:6])
    default_last_run_time = "%04d-%02d-%02dT%02d:%02d:%02d" % ((local_time[0]-10,) + local_time[1:6])
    last_run_time = persist.get("last_run_time", default_last_run_time)
    time_difference = calculate_time_difference(current_time, last_run_time)

    interval = int(options["interval"])
    script = options["script"]
    
    response_actions = []
    response_persistent_data = []

    if time_difference >= interval:
        response_persistent_data.append({"last_run_time": current_time})
        response_actions.append({
            "run-script": {
                "always-execute": True,
                "cmdline": script
            }
        })

    else:
        response_persistent_data.append({"last_run_time": last_run_time})

    response = {'actions': response_actions, 'persistent-data': response_persistent_data}

    if options.get("debug") == "true":
        # Debug information printing
        print("Debug Information:")
        print(f"Paths: {paths}")
        print(f"Options: {options}")
        print(f"Persistent Data: {persist}")
        print(f"Current Time: {current_time}")
        print(f"Default Last Run Time: {default_last_run_time}")
        print(f"Last Run Time: {last_run_time}")
        print(f"Time Difference: {time_difference}")
        print(f"Response: {response}")

    return json.dumps(response)

def main():
    """
    Test function for event_handler_main with example JSON input.
    """
    example_in_json_str = """
{
    "paths": [
    ],
    "options": {
        "debug": "true",
        "interval": "50",
        "script": "/usr/bin/python3 /etc/opt/srlinux/eventmgr/mac-limit-enh.py"
    },
    "persistent-data": [
        {
            "last_run_time": "2024-02-26T14:36:09"
        }
    ]
}
"""

    json_response = event_handler_main(example_in_json_str)
    print(f"Response JSON:\n{json_response}")

if __name__ == "__main__":
    sys.exit(main())
