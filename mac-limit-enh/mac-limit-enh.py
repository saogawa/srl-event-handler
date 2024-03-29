import re
import os

# Step 1: Read the file into a list
with open('/var/log/srlinux/file/mac-limit', 'r') as file:
    lines = file.readlines()

# Step 2: Process the lines
new_lines = []
for line in lines:
    lower_line = line.lower()
    if re.search(r'the number of mac addresses in the bridge table for the sub-interface .* has reached the allowed limit of .*', lower_line):
        # Check if the limit is 8192, if so, do nothing
        if "reached the allowed limit of 8192" in lower_line:
            new_lines.append(line)
        else:
            # Parse the interface name from the string
            match = re.search(r'ethernet-(\d+/\d+).(\d+)', line)
            if match:
                interface = match.group(1)
                subinterface = match.group(2)

                # Output the string
                shutdown_command = f"sr_cli --candidate-mode --commit-at-end -- /interface ethernet-{interface} subinterface {subinterface} admin-state disable"
                print(lower_line)
                print(shutdown_command)

                # Execute the command to enable the subinterface
                os.system(shutdown_command)

                # Replace the line
                new_line = re.sub(r'The number of MAC addresses in the bridge table for the sub-interface .* has reached the allowed limit of .*',
                                  f'The bridge table for the sub-interface ethernet-{interface}.{subinterface} has been shutdown.', line)
                new_lines.append(new_line)
    else:
        new_lines.append(line)

# Step 3: Write the new lines back to the file
with open('/var/log/srlinux/file/mac-limit', 'w') as file:
    file.writelines(new_lines)
