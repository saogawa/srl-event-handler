# SR-Linux Event Handler: MAC Limit Enhancement

This repository offers scripts and configurations to improve MAC limit event management in SRLinux, focusing on detecting and addressing MAC address table overflows by automatically shutting down the affected subinterfaces.
## Preassumption
- This script uses only python modules supported in SR-Linux v23.7/v23.10.
  ~~~bash
        root@D5-core1:~# pip list
        Package            Version
        ------------------ ----------
        asn1crypto         1.5.1
        certifi            2022.9.24
        chardet            5.1.0
        charset-normalizer 3.0.1
        construct          2.10.68
        cryptography       38.0.4
        distlib            0.3.6
        filelock           3.9.0
        idna               3.3
        numpy              1.24.2
        pexpect            4.8.0
        pip                23.0.1
        platformdirs       2.6.0
        ptyprocess         0.7.0
        pyasn1             0.4.8
        pyasn1-modules     0.2.8
        PyYAML             6.0
        requests           2.28.1
        sdkmgr-proto       0.1
        setuptools         66.1.1
        six                1.16.0
        urllib3            1.26.12
        virtualenv         20.17.1+ds
        wheel              0.38.4
  ~~~

## How It Works : SRL Event-Handler configuration

~~~bash
      --{ + running }--[  ]--
      A:D5-core1# info from running /system event-handler
          system {
              event-handler {
                  instance mac-limit-enh {
                      admin-state enable
                      upython-script run-script.py
                      paths [
                          "system information current-datetime"
                      ]
                      options {
                          object debug {
                              value true
                          }
                          object interval {
                              value 30
                          }
                          object script {
                              value "/usr/bin/python3 /opt/srlinux/eventmgr/mac-limit-enh.py"
                          }
                      }
                  }
              }
          }
~~~

## How It Works : run-script-eh.py
**Event Handling:** Executes `run-script-eh.py` to check the interval periodically and trigger external script, `mac-limit-enh.py`.
  
  1. **Calculate Time Difference:** It calculates the time difference between the current time and the last run time of the script. This involves parsing timestamps and converting them to seconds for comparison.
  
  2. **Read Input JSON:** The script reads an input JSON string, which includes paths, options (such as the interval between runs and the script to execute), and persistent data (like the last run time).
  
  3. **Determine Execution:** Based on the calculated time difference and the specified interval, it decides whether to execute the `mac-limit-enh.py` script. If the time difference is greater than or equal to the interval, the script is triggered.
  
  4. **Update Persistent Data:** It updates the persistent data with the current time as the new "last run time," ensuring that subsequent runs can calculate the correct time difference.
  
  5. **Generate Response:** The script generates a JSON response that includes actions to be taken (such as running the specified script) and the updated persistent data. This response can be used to trigger the actual execution of the `mac-limit-enh.py` script and to log the event handler's activity.
  
  ![diagram(3)](https://github.com/saogawa/srl-event-handler/assets/35554139/aa5f532a-aee5-4f86-a5af-b10a45be58ac)


## How It Works : mac-limit-enh.py
**MAC Limit Enforcement:** `mac-limit-enh.py` identifies and shuts down subinterfaces reaching MAC address limits.
  
  For the pre-condition, SRL logging for the mac-limit must be enabled with following configuration:
  
  ~~~bash
  --{ + running }--[  ]--
  A:D5-core1# info from running /system logging file mac-limit
      system {
          logging {
              file mac-limit {
                  rotate 3
                  size 1000000
                  filter [
                      mac-limit
                  ]
                  facility all {
                      priority {
                          match-above warning
                      }
                  }
              }
          }
      }
  ~~~
  
  
  1. **Read Log File:** It starts by opening and reading a log file (`/var/log/srlinux/file/mac-limit`) line by line, where MAC limit events are logged.
  
  2. **Detect MAC Limit Events:** It searches each line for patterns indicating that the MAC address limit has been reached for a subinterface. This is done using regular expressions to match specific log entries.
  
  3. **Parse Interface Details:** Upon finding a matching entry, it extracts the interface and subinterface details from the log line.
  
  4. **Shutdown Subinterface:** It constructs a command to shut down the identified subinterface by setting its administrative state to disable. This command is then executed using the system call.
  
  5. **Log Modification:** The script modifies the original log line to indicate that the subinterface has been shut down due to exceeding the MAC limit. This new line replaces the original in the list of lines to be written back to the log file.
  
  6. **Write Back to Log File:** Finally, the modified list of lines (including the updated entries) is written back to the log file, effectively updating it with the actions taken by the script.
  
  ![diagram(4)](https://github.com/saogawa/srl-event-handler/assets/35554139/66a7502a-f6ce-4055-9d8d-1de3881045bd)
  


## Setup and Configuration

To deploy this enhancement:
  
  1. Download the following files:
     - [run-script.py](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/run-script.py)
     - [mac-limit-enh.py](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/mac-limit-enh.py)
  
  2. Copy the files to the following folder and set permissions:
  
  ```bash
  chmod 777 /opt/srlinux/eventmgr/mac-limit-enh.py
  chown root:root /opt/srlinux/eventmgr/mac-limit-enh.py
  chmod 777 /opt/srlinux/eventmgr/run-script.py
  chown root:root /opt/srlinux/eventmgr/run-script.py
  ```
  
  3. Apply the following configuration:
  
     - [srl_cfg_event-handler.flat](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/srl_cfg_event-handler.flat)
     - [srl_cfg_logging-file.flat](https://github.com/saogawa/srl-event-handler/blob/main/mac-limit-enh/srl_cfg_logging-file.flat)
  
  4. Ensure that the log file has been generated:
  
  ```bash
  root@D2L:/# ls -lt /var/log/srlinux/file/mac-limit
  -rw-rw-r--+ 1 syslog adm 163 Feb 27 15:16 /var/log/srlinux/file/mac-limit
  ```
  
  5. Confirm there are no errors in the Event-Handler:
  
  ```bash
  --{ +* candidate shared default }--[  ]--
  A:D2L# info from state /system event-handler instance mac-limit-enh last-errored-execution
  --{ +* candidate shared default }--[  ]--
  A:D2L#
  ```
  
  *If errors are outputted, please send the following log:
  ```bash
  info from state /system event-handler
  ```
  
  6. Set the mac-limit for SubIF:
  
  ```bash
  A:D2L# /interface ethernet-1/1 subinterface 10 bridge-table mac-limit maximum-entries <1-8192>
  A:D2L# /interface ethernet-1/1 subinterface 10 bridge-table mac-limit warning-threshold-pct 100 maximum-entries
  ```
  
  *If you want not to disable the SubIF. please specify the value of 8192. The mac-limit-en.py will not shutdown the SubIF. (MAC learning will not occur, but communication will continue)
  
  7. The maximum number of MAC addresses for SubIF is checked periodically through polling. The interval can be tuned with the following value:
  
  ```bash
  A:D2L# /system event-handler instance mac-limit-enh options object interval value 60
  ```
