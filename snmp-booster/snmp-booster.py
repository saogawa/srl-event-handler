import sys
import json

def event_handler_main(in_json_str):
    """
    Main handler function that processes input JSON string and determines
    if a specified script should be executed based on the time interval.
    """
    in_json = json.loads(in_json_str)
    options = in_json["options"]

    response_actions = []

    response_actions.append({
        "reinvoke-with-delay": int(options["interval"])
    })

    response_actions.append({
        "set-tools-path": {
            "path": "system app-management application snmp_server-mgmt restart",
            "value": ""
        }
    })

    response = {'actions': response_actions}

    return json.dumps(response)

if __name__ == "__main__":
    sys.exit(0)
