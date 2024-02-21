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

    response_actions = []
    lag_members = {}

    # Iterate over the paths
    for path in paths:
        path_parts = path["path"].split(" ")

        # If the path contains "lag member", add it to the lag_members dictionary
        if "lag member" in path["path"]:
            interface = path_parts[1]
            if interface not in lag_members:
                lag_members[interface] = []
            lag_members[interface].append(path_parts[4])

    # Iterate over the paths again
    for path in paths:
        path_parts = path["path"].split(" ")

        # If the path contains "admin-state", check the admin state and set the oper-state accordingly
        if "admin-state" in path["path"]:
            interface = path_parts[1]
            admin_state = path["value"]
            if interface in lag_members:
                for member in lag_members[interface]:
                    if admin_state == "disable":
                        # If admin state is disable, set the oper-state of the member to down
                        response_actions.append(
                            {
                                "set-ephemeral-path": {
                                    "path": f"interface {member} oper-state",
                                    "value": "down",
                                }
                            }
                        )
                    elif admin_state == "enable":
                        # If admin state is enable, set the oper-state of the member to up
                        response_actions.append(
                            {
                                "set-ephemeral-path": {
                                    "path": f"interface {member} oper-state",
                                    "value": "up",
                                }
                            }
                        )

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
            "path": "interface lag1 admin-state",
            "value": "disable"
        },
        {
            "path": "interface lag1 lag member ethernet-1/1 oper-state",
            "value": "down"
        },
        {
            "path": "interface lag1 lag member ethernet-1/4 oper-state",
            "value": "down"
        },
        {
            "path": "interface lag2 admin-state",
            "value": "disable"
        },
        {
            "path": "interface lag2 lag member ethernet-1/2 oper-state",
            "value": "down"
        },
        {
            "path": "interface lag3 admin-state",
            "value": "disable"
        },
        {
            "path": "interface lag3 lag member ethernet-1/3 oper-state",
            "value": "down"
        }
    ],
    "options": {
        "debug": "true"
    }
}
"""
    json_response = event_handler_main(example_in_json_str)
    print(f"Response JSON:\n{json_response}")

# Run the main function and exit the script afterwards
if __name__ == "__main__":
    sys.exit(main())
