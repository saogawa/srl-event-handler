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

    network_instance_names = []
    for path in paths:
        if "network-instance" in path["path"] and path["value"] == "mac-vrf":
            network_instance_name = path["path"].split(" ")[1]
            network_instance_names.append(network_instance_name)

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
    "paths": [
        {
            "path": "network-instance default type",
            "value": "default"
        },
        {
            "path": "network-instance mac-vrf10 type",
            "value": "mac-vrf"
        },
        {
            "path": "network-instance mac-vrf20 type",
            "value": "mac-vrf"
        },
        {
            "path": "network-instance mgmt type",
            "value": "ip-vrf"
        }
    ],
    "options": {
        "debug": "true"
    }
}
"""
    json_response = event_handler_main(example_in_json_str)
    print(f"Response JSON:\n{json_response}")

if __name__ == "__main__":
    sys.exit(main())
