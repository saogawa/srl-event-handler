import sys
import json

# The main entry function for the event handler
def event_handler_main(in_json_str):
    # Parse the input JSON string passed by the event handler
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]

    # If the debug option is set to true, print the paths
    if options.get("debug") == "true":
        print(paths)

    network_instance_name = None
    for path in paths:
        if "network-instance" in path["path"] and "bridge-table" in path["path"]:
            # Split the path and find the network instance name
            path_parts = path["path"].split(" ")
            for i, part in enumerate(path_parts):
                if part == "network-instance":
                    network_instance_name = path_parts[i + 1]
                    break

    print(f"Network instance name: {network_instance_name}")
    response_actions = []

    if network_instance_name is not None:
        response_actions.append({
            "set-tools-path": {
                "path": f"network-instance {network_instance_name} bridge-table mac-duplication delete-macs-type",
                "value": "all"
            }
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
    "paths": [
        {
            "path": "network-instance mac-vrf10 bridge-table statistics mac-type duplicate active-entries",
            "value": "1"
        }
    ],
    "options": {
        "debug": "false"
    }
}
"""
    json_response = event_handler_main(example_in_json_str)
    print(f"Response JSON:\n{json_response}")

if __name__ == "__main__":
    sys.exit(main())
