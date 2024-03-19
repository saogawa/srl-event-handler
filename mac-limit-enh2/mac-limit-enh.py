import sys
import json
import re
import os

def extract_interfaces_from_log():
    # Log file path
    log_file_path = '/var/log/srlinux/file/mac-limit'
    temp_file_path = '/var/log/srlinux/file/mac-limit_temp'

    try:
        os.stat(log_file_path)
    except OSError:
        print(f"{log_file_path} does not exist.")
        return []

    try:
        os.stat(temp_file_path)
    except OSError:
        print(f"{temp_file_path} does not exist.")
        return []

    # Regular expression pattern to extract interface names from the log
    pattern = r"The number of MAC addresses in the bridge table for the sub-interface (\S+) has reached the allowed limit of"

    # Set to store interface names (no duplicates)
    interfaces = set()

    try:
        with open(log_file_path, 'r') as read_file:
            pass
    except OSError as e:
        print(f"Failed to open {log_file_path}. Error: {str(e)}")
        return []

    try:
        with open(temp_file_path, 'w') as write_file:
            pass
    except OSError:
        print(f"Failed to open {temp_file_path}")
        return []

    # Use os module to replace the original file with the temporary file
    os.remove(log_file_path)
    os.rename(temp_file_path, log_file_path)

    # Return the list of interface names
    return list(interfaces)

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
    interface_list = extract_interfaces_from_log()

    debug = options.get('debug', None)
    object1 = options.get('object1', None)
    object2 = options.get('object2', None)
    object3 = options.get('object3', None)
    object4 = options.get('object4', None)

    response_actions = []
    response_persistent_data = []

    print(options)

    response_actions.append({'reinvoke-with-delay' : 1000})

    for interface in interface_list:
        interface_name, subinterface = interface.split('.')
        response_actions.append({
            "set-ephemeral-path": {
                "always-execute": True,
                "path": f"interface {interface_name} subinterface {subinterface} admin-state",
                "value": "disable",
            }
        })

    response = {'actions': response_actions, 'persistent-data': response_persistent_data}

    if debug == "true":
        # Debug information printing
        print("Debug Information:")
        print(f"Paths: {paths}")
        print(f"Options: {options}")
        print(f"Object1: {object1}")
        print(f"Object2: {object2}")
        print(f"Object3: {object3}")
        print(f"Object4: {object4}")
        print(f"Persistent Data: {persist}")
        print(f"Interface List: {interface_list}")
        print(f"Response: {response}")

    return json.dumps(response)

def main():
    """
    Test function for event_handler_main with example JSON input.
    """
    example_in_json_str = """
{
    "paths": [
      "system information current-datetime"
    ],
    "options": {
      "object": [
        {
          "name": "debug",
          "value": "true"
        },
        {
          "name": "object1",
          "value": "10"
        },
        {
          "name": "object2",
          "value": "20"
        },
        {
          "name": "object3",
          "value": "30"
        },
        {
          "name": "object4",
          "values": [
            "100",
            "200",
            "300"
          ]
        }
      ]
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
