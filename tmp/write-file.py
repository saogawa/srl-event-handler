import sys
import json

def event_handler_main(in_json_str):

    try:
        with open('./data.txt', 'w') as file:
            file.write("Hello world!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Failed to write to file at path: './data.txt'")

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
