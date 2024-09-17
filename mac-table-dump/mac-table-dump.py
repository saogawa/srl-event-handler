import os
import glob
import subprocess
import time

def execute_commands_and_save_output(file_path, commands, max_files):
    # Get current time and format it as a timestamp
    local_time = time.localtime()
    time_stamp = "%04d-%02d-%02d_%02d-%02d-%02d" % local_time[0:6]

    # Append timestamp to the file path
    file_path_with_timestamp = f"{file_path}_{time_stamp}"

    # Open the file with timestamp in the name
    with open(file_path_with_timestamp, 'w') as file:
        # Execute each command and redirect its output to the file
        for command in commands:
            subprocess.run(command, stdout=file, shell=True)

    # Compress the file with zip format
    zip_file_path = f"{file_path_with_timestamp}.zip"
    subprocess.run(f"zip -j {zip_file_path} {file_path_with_timestamp}", shell=True)

    # Remove the original uncompressed file
    os.remove(file_path_with_timestamp)

    # Get all files that match the file path pattern
    files = sorted(glob.glob(f"{file_path}_*"))

    # If the number of files is greater than max_files, delete the oldest files
    for file in files[:-max_files]:
        os.remove(file)

def main():
    file_path = "/var/log/srlinux/file/mac_dump_log"
    commands = [
        "sr_cli --output-format json 'info from state /system information current-datetime'",
        "sr_cli --output-format json 'info from state /platform control A cpu all'",
        "sr_cli --output-format json 'info from state /platform control A memory'",
        "sr_cli --output-format json 'info from state /interface * | filter subinterface fields oper-state oper-down-reason'",
        "sr_cli --output-format json 'info from state /network-instance * bridge-table mac-table'"
    ]
    max_files = 10
    execute_commands_and_save_output(file_path, commands, max_files)

if __name__ == "__main__":
    main()

