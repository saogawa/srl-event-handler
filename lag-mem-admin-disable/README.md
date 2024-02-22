# SR-Linux LAG Interface Management Event Handler

This Python-based event handler enhances the management of LAG interfaces in SR-Linux by addressing operational state behavior discrepancies during administrative enable/disable actions.

## Overview

### Current Behavior
- **Admin Disable**: SR-Linux marks LAG member ports as down, but their operational state remains up.
- **Comparison**: In SR-OS and Arista devices, disabling a LAG interface also disables its member ports and stops the optical laser.

### Problem
The operational state of physical ports remains up when a LAG interface is admin disabled, causing the optical lasers to continue transmitting. This requires peer devices to rely on LACP or BFD for link down detection.

## Improvements
- **Admin Disable**: Sets the operating status of physical ports to down, stopping the optical lasers and allowing immediate link down detection by peer devices.
- **Admin Enable**: Sets the operation status of member ports to up.

## Limitations
- Supports a maximum of 25 ports per LAG interface. For more than 25 ports, multiple instances of the event handler can be created, with a limit of up to 20 instances.
