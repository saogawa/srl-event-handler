import sys
import json


def event_handler_main(in_json_str):
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]

    response_actions = []

# Will add a condition to compare the periodic execution time after compare between end-time and current-datatime.
#
#[2024-01-30 12:57:39.480862]: update /system/event-handler/instance[name=mac-limit-enh]/last-execution/end-time:2024-01-30T03:55:28.923Z
#^CCommand execution aborted : 'monitor on-change /system event-handler instance mac-limit-enh last-execution end-time '
#--{ + candidate shared default }--[ system event-handler instance mac-limit-enh ]--
#A:D5-core1# monitor on-change /system information current-datetime
#[2024-01-30 12:57:41.969677]: update /system/information/current-datetime:2024-01-30T03:57:41.273Z
#[2024-01-30 12:57:42.273007]: update /system/information/current-datetime:2024-01-30T03:57:42.272Z


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
