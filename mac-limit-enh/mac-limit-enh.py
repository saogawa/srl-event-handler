# Importing necessary libraries
import sys
import json
import re
import os

# Function to check MAC limit log
def check_mac_limit_log():
    # Creating a set to store unique interfaces
    interfaces = set()

    # Defining the log file path
    log_file_path = './logs/mac-limit'
    temp_file_path = './logs/mac-limit.temp'

    # Checking if the log file exists
    try:
        os.stat(log_file_path)
    except OSError:
        print(f"{log_file_path} does not exist.")
        sys.exit()

    # Checking if the temporary file exists, if not, create one
    try:
        os.stat(temp_file_path)
    except OSError:
        open(temp_file_path, 'w').close()

    # Regular expression pattern to extract interface names from the log
    pattern = r"The number of MAC addresses in the bridge table for the sub-interface (\S+) has reached the allowed limit of"

    # Opening the log file and temporary file
    with open(log_file_path, 'r') as read_file, open(temp_file_path, 'w') as write_file:
        # Reading each line in the log file
        for line in read_file:
            # Searching for the pattern in each line
            match = re.search(pattern, line)
            # If the pattern is found, extract the interface name and add it to the set
            if match:
                interface_name = match.group(1)
                interfaces.add(interface_name)
                continue  
            # If the pattern is not found, write the line to the temporary file
            write_file.write(line)  

    # Replacing the original log file with the temporary file
    os.replace(temp_file_path, log_file_path)

    # Return the list of unique interface names
    return(list(interfaces))


# Main event handler function
def event_handler_main(in_json_str):
    """
    Main handler function that processes input JSON string and determines
    if a specified script should be executed based on the time interval.
    """
    # Loading the JSON string
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]
    persist = in_json.get("persistent-data", [{}])
    persist = persist[0] if persist else [{}]

    # Checking the MAC limit log and getting the list of interfaces
    interface_list = check_mac_limit_log()

    # Getting the debug and interval options
    debug = options.get('debug', None)
    interval = options.get('interval', None)
    print(interval)
    
    # Initializing the response actions and persistent data
    response_actions = []
    response_persistent_data = []

    # Adding the reinvoke-with-delay action to the response actions
    response_actions.append({'reinvoke-with-delay' : int(interval)*1000})
    # For each interface, add a set-ephemeral-path action to the response actions
    for interface in interface_list:
        interface_name, subinterface = interface.split('.')
        response_actions.append({
            "set-ephemeral-path": {
                "always-execute": True,
                "path": f"interface {interface_name} subinterface {subinterface} admin-state",
                "value": "disable",
            }
        })

    # Creating the response dictionary
    response = {'actions': response_actions, 'persistent-data': response_persistent_data}

    # If debug is true, print debug information
    if debug == "true":
        print("Debug Information:")
        print(f"Paths: {paths}")
        print(f"Options: {options}")              

    # Return the response as a JSON string
    return json.dumps(response)

# Test function for event_handler_main with example JSON input
def main():
    example_in_json_str = """
{
    "paths": [
      "system information current-datetime"
    ],
    "options": {
      "debug": "true",
      "interval": "1"
    },
    "persistent-data": [
        {
            "last_run_time": "2024-02-26T14:36:09"
        }
    ]
}
"""

    # Running the event handler main function with the example JSON string
    json_response = event_handler_main(example_in_json_str)
    # Printing the response JSON
    print(f"Response JSON:\n{json_response}")

# If the script is run directly, execute the main function
if __name__ == "__main__":
    sys.exit(main())
