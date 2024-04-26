# Importing necessary libraries
import sys
import json
import os
import re

# Main function to handle events
def event_handler_main(in_json_str):

    # Log file to read from /etc/opt/srlinux/eventmgr
    log_file_path = 'mac-limit'

    # Set to store unique interfaces
    interface_list = set()
    # List to store response actions
    response_actions = []

    # Pattern to match in the log file
    pattern = r"The number of MAC addresses in the bridge table for the sub-interface (\S+) has reached the allowed limit of"

    try:
        # Open the log file in read mode
        with open(log_file_path, 'r') as file:
            lines = file.readlines()
        # Open the log file in write mode
        with open(log_file_path, 'w') as file:
            for line in lines:
                # Search for the pattern in each line
                match = re.search(pattern, line)
                # If match found and interface_list size is less than 100, add the interface to the list
                if match and len(interface_list) < 100:
                    interface_list.add(match.group(1))
                else:
                    # If no match found, write the line back to the file
                    file.write(line)

    # If file does not exist, print error message and exit
    except OSError:
        print(f"{log_file_path} does not exist.")
        sys.exit()

    response_actions.append({
        "reinvoke-with-delay": 5000
    })

    # For each interface, add a set-ephemeral-path action to the response actions
    for interface in interface_list:
        # Split the interface into interface name and subinterface
        interface_name, subinterface = interface.split('.')
        # Append the action to the response actions list
        response_actions.append({
            "set-cfg-path": {
                "always-execute": True,
                "path": f"interface {interface_name} subinterface {subinterface} admin-state",
                "value": "disable",
            }
        })

    # Initialize response dictionary
    response = { }
    # Add actions to the response
    response = {'actions': response_actions}

    # Return the response as a JSON string
    return json.dumps(response)

    # Initialize response dictionary
    response = {}  
    # Return the response as a JSON string
    return json.dumps(response)

# Main function
def main():
    # Example JSON string
    example_in_json_str = """
{
    "paths": [ ],
    "options": {
      "object": [{}]
    }
}
"""
    # Call the event handler function and print the response
    json_response = event_handler_main(example_in_json_str)
    print(f"Response JSON:\n{json_response}")

# If this script is run directly, call the main function
if __name__ == "__main__":
    sys.exit(main())
