import sys
import json
 
def get_max_entries(options):
    return int(options.get("max-entries", 1))

# main entry function for event handler
def event_handler_main(in_json_str):
    # parse input json string passed by event handler
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]
 
    max_learn_mac = get_max_entries(options)
    response_actions = []
    for path in paths:
        learn_mac = int(path.get("value"))
        instance = path['path'].replace(' bridge-table statistics active-entries', '')
        if  learn_mac > max_learn_mac:
            response_actions.append(
                {
                    "set-cfg-path": {
                    "path": f"{instance} admin-state",
                    "value": "disable",
                    }
                }
            )
 
    if options.get("debug") == "true":
        print (paths)
        print (options)
        print (max_learn_mac)
        print (instance)
 
    response = {"actions": response_actions}
    return json.dumps(response)
 
 
#
# This code is only if you want to test it from bash - this isn't used when invoked from SRL
#
def main():
    example_in_json_str = """
{
    "paths": [
        {
            "path":"interface ethernet-1/1 subinterface 10  bridge-table statistics active-entries",
            "value":"6"
        },
        {
            "path":"network-instance mac-vrf_10 bridge-table statistics active-entries",
            "value":"6"
        }
    ],
    "options": {
        "max-entries":5,
        "debug": "true"
    },
    "persistent-data": {"last-state":"up"}
}
"""
    json_response = event_handler_main(example_in_json_str)
    print(f"Response JSON:\n{json_response}")
 
if __name__ == "__main__":
    sys.exit(main())%           
