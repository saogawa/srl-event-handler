import sys
import json

def event_handler_main(in_json_str):

    try:
        with open('/var/log/srlinux/file/readme.txt', 'r') as file:
            print(file.read())
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Failed to open file at path: '/var/log/srlinux/file/readme.txt'")

    response = {}
    return json.dumps(response)

def main():
    example_in_json_str = """
{
    "paths": [ ],
    "options": {
      "object": [{}]
    }
}
"""

    json_response = event_handler_main(example_in_json_str)
    print(f"Response JSON:\n{json_response}")

if __name__ == "__main__":
    sys.exit(main())
