# snmp-booster

## Overview

`snmp-booster` is a component of the [srl-event-handler](https://github.com/saogawa/srl-event-handler) project. It is designed to optimize and streamline SNMP (Simple Network Management Protocol) operations, providing enhanced performance and integration for event handling workflows, particularly in environments using Nokia SR Linux (SRL).

## Features

- Peridic snmp process restart automatically with the Event Handler running on SR-Linux

## Directory Structure

```
snmp-booster/
├── snmp-booster.py
├── srl_cfg_event-handler.flat
└── README.md
```

## Installation

1. Clone the repository:

    ```sh
    cp snmp-booster.py /etc/opt/srlinux/eventmgr/
    ```

## Usage

You can use `snmp-booster` as a standalone module or as part of the `srl-event-handler` system. 

## Configuration

Configuration options (if any) can be set via environment variables or configuration files. Please refer to the code or configuration examples for details.
    
    ```sh
    set / system event-handler instance snmp-rebooter admin-state enable
    set / system event-handler instance snmp-rebooter upython-script snmp-booster.py
    set / system event-handler instance snmp-rebooter options object interval value 5000
    ```
    
## Development

- Ensure you have Python 3.8+ installed.
- Code contributions and PRs are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

## Contact

For questions or support, please open an issue in the main [srl-event-handler repository](https://github.com/saogawa/srl-event-handler/issues).
