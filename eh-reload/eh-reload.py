import sys
import json
import time

def convert_timestamp_to_seconds(timestamp):
    """
    Converts a timestamp in ISO 8601 format (YYYY-MM-DDTHH:MM:SS) into total seconds from a base time.
    Note: Simplified conversion, does not account for varying month lengths or leap years.
    """
    timestamp = timestamp.split('.')[0]
    date, time = timestamp.split('T')
    year, month, day = map(int, date.split('-'))
    hour, minute, second = map(int, time.split(':'))
    total_seconds = second + minute * 60 + hour * 3600 + day * 86400 + month * 2592000 + year * 31104000

    return total_seconds

def event_handler_main(in_json_str):
    # Parse the input JSON string passed by the event handler
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]
    persistent_data = in_json.get("persistent-data", [{}])[0]

    if options.get("debug") == "true":
        print("DEBUG: Input paths -", paths)

    instances = options.get("instance", [])
    last_change_timestamp = persistent_data.get("last_change_timestamp", "")

    response_actions = []
    response_persistent_data = []

    for path in paths:
        if path["path"] == "system configuration last-change":
            current_change_timestamp = path["value"]

            if options.get("debug") == "true":
                print("DEBUG: Current Change Timestamp -", current_change_timestamp)

            if current_change_timestamp > last_change_timestamp:
                for instance in instances:
                    response_actions.append(
                        {
                            "set-tools-path": {
                                "path": f"system event-handler instance {instance} reload",
                                "always-execute": True,
                                "value": "",
                            }
                        }
                    )
                last_change_timestamp = current_change_timestamp

    response_persistent_data.append({"last_change_timestamp": last_change_timestamp})
    response = {'actions': response_actions, 'persistent-data': response_persistent_data}

    if options.get("debug") == "true":
        print("DEBUG: Response -", response)

    time.sleep(5)
    return json.dumps(response)

def main():
    example_in_json_str = """
{
    "paths": [
        {
            "path": "system configuration last-change",
            "value": "2024-03-13T06:22:49.274Z"
        },
        {
            "path": "interface lag1 oper-state",
            "value": "down"
        },
        {
            "path": "interface lag1 lag member ethernet-1/55 oper-state",
            "value": "down"
        },
        {
            "path": "interface lag1 lag member ethernet-1/56 oper-state",
            "value": "down"
        }
    ],
    "options": {
        "debug": "true"
    }
}
"""
    json_response = event_handler_main(example_in_json_str)
    print("Response JSON:\n", json_response)

# Run the main function and exit the script afterwards
if __name__ == "__main__":
    sys.exit(main())
