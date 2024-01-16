import sys
import json

"""
This script compares the number of active MAC entries to the MAC limit for each subinterface.
If the number of active entries exceeds the configured MAC limit, the corresponding subinterface
is administratively disabled to prevent further MAC address learning.

The comparison is done by parsing the JSON data which contains the paths and values for
the 'bridge-table mac-limit maximum-entries' and 'bridge-table statistics active-entries'
for each subinterface. The script identifies each subinterface by its unique path and then
compares the values. If the 'active-entries' value is greater than the 'maximum-entries' value,
a command to administratively disable the subinterface is generated.

Note: The actual disabling of the subinterface is not performed by this script and should be
handled by the network management system that executes the script's output commands.
"""

# main entry function for event handler
def event_handler_main(in_json_str):
    # parse input json string passed by event handler
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]

    # Create a dictionary to store the values for comparison
    entries_dict = {}

    # Iterate through the paths and populate the dictionary
    for entry in paths:
        # Split the path to get the key and value type
        key, value_type = entry["path"].split(" bridge-table ")

        # Convert the value to integer
        value = int(entry["value"])

        # If the key is not in the dictionary, initialize it with an empty dictionary
        entries_dict.setdefault(key, {})

        # Add the value type and value to the dictionary
        entries_dict[key][value_type.split(" ")[1]] = value

    response_actions = []

    # Iterate through the dictionary
    for key, values in entries_dict.items():
        # If both "active-entries" and "maximum-entries" are in the dictionary
        if "active-entries" in values and "maximum-entries" in values:
            # If the number of active entries is greater than the maximum entries
            if values["active-entries"] >= values["maximum-entries"]:
                response_actions.append(
                    {
                        "set-cfg-path": {
                            "path": f"{key} admin-state",
                            "value": "disable",
                            }
                    }
                )
                if options.get("debug") == "true":
                    print(f"Shutdown port {key}")

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
      "path": "interface ethernet-1/1 subinterface 10 bridge-table statistics active-entries",
      "value": "9"
    },
    {
      "path": "interface ethernet-1/1 subinterface 10 bridge-table mac-limit maximum-entries",
      "value": "8"
    },
    {
      "path": "interface ethernet-1/10 subinterface 11 bridge-table statistics active-entries",
      "value": "10"
    },
    {
      "path": "interface ethernet-1/10 subinterface 11 bridge-table mac-limit maximum-entries",
      "value": "6"
    },
    {
      "path": "interface ethernet-1/11 subinterface 20 bridge-table statistics active-entries",
      "value": "9"
    },
    {
      "path": "interface ethernet-1/11 subinterface 20 bridge-table mac-limit maximum-entries",
      "value": "8"
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
