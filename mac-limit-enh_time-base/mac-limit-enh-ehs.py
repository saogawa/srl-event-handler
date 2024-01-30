import sys
import json


def event_handler_main(in_json_str):
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]

    response_actions = []

    response_actions.append(
      {
        "run-script": {
            "always-execute": True,
            "cmdline": f"/usr/bin/python3 /etc/opt/srlinux/eventmgr/mac-limit-enh.py"
        }
      }
    )

    if options.get("debug") == "true":
      print(f"Run the mac-limit-enh.py")

    response = {"actions": response_actions}
    return json.dumps(response)

#
# This code is only if you want to test it from bash - this isn't used when invoked from SRL
#
def main():
    example_in_json_str = """
{
   "paths":[
      {
         "path":"interface mgmt0 statistics in-packets",
         "value":"45833182"
      }
   ],
   "schemas":[
      {
         "path":"interface mgmt0 statistics in-packets"
      }
   ],
   "options":{

   }
}
"""

    json_response = event_handler_main(example_in_json_str)
    print(f"Response JSON:\n{json_response}")

if __name__ == "__main__":
    sys.exit(main())