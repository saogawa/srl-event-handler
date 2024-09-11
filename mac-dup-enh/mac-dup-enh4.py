import sys
import json
import subprocess

# The main entry function for the event handler
def event_handler_main(in_json_str):
    # Parse the input JSON string passed by the event handler
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]

    # If the debug option is set to true, print the paths
    if options.get("debug") == "true":
        print(paths)

    # Execute the shell command to get the active entries
    command = 'sr_cli -s "info /network-instance * bridge-table statistics mac-type duplicate active-entries"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Initialize the list to store network instance names
    network_instance_names = []

    # Parse the command output
    for line in result.stdout.splitlines():
        if "network-instance" in line:
            current_instance = line.split()[1]
        if "active-entries" in line and int(line.split()[1]) != 0:
            network_instance_names.append(current_instance)

    print(f"Network instance name: {network_instance_names}")
    response_actions = []

    if network_instance_names is not None:
        for network_instance_name in network_instance_names:
            response_actions.append({
                "set-tools-path": {
                    "path": f"network-instance {network_instance_name} bridge-table mac-duplication delete-macs-type",
                    "value": "all"
                }
            })

    response_actions.append({
        "reinvoke-with-delay": 1000
    })

    # If the debug option is set to true, print the response actions
    if options.get("debug") == "true":
        print(response_actions)

    response = {"actions": response_actions}
    return json.dumps(response)

# Function to test the event handler_main function
def main():
    example_in_json_str = """
{
    "options": {
        "debug": "true"
    }
}
"""
    json_response = event_handler_main(example_in_json_str)
    print(f"Response JSON:\n{json_response}")

if __name__ == "__main__":
    sys.exit(main())
