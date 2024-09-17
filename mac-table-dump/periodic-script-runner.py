import sys
import json
import time


def event_handler_main(in_json_str):
    """
    Main handler function that processes input JSON string and determines
    if a specified script should be executed based on the time interval.
    """
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]

    script = options["script"]
    response_actions = []

    response_actions.append({
        "reinvoke-with-delay": int(options["interval"])
    })

    response_actions.append({
        "run-script": {
            "always-execute": True,
            "cmdline": script
        }
    })

    response = {'actions': response_actions}

    if options.get("debug") == "true":
        # Debug information printing
        print("Debug Information:")
        print(f"Paths: {paths}")
        print(f"Options: {options}")
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
        "interval": "10000",
        "script": "/usr/bin/python3 /etc/opt/srlinux/eventmgr/mac-table-dump.py"
    }
}
"""

    json_response = event_handler_main(example_in_json_str)
    print(f"Response JSON:\n{json_response}")
    return 0  # Return 0 to indicate successful execution

if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as e:
        if e.args[0] != 0:
            raise

