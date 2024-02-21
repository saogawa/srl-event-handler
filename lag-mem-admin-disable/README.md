
# Event Handler for SR-Linux LAG Interface Management

This Python code for an event handler improves the behavior of LAG interfaces in SR-Linux as follows:

### Current Behavior:
- When the LAG interface is admin disabled, SR-Linux sets the operation status of LAG member ports to down. However, the operation status of member ports remains up.
- In SR-OS, admin disabling the LAG interface causes the member ports to be blocked, and the optical laser stops. Arista implements a similar behavior.

### Issue:
Since the physical ports are not blocked, the optical lasers of the ports continue to transmit, requiring the peer device to detect the link down using LACP or BFD.

### Improvements by Implementing the Code:
- When the LAG interface is admin disabled, the physical ports (not just the LAG member port status) have their operation status set to down. This stops the optical lasers of the physical ports, enabling immediate link down detection by the peer device.
- When the LAG interface is admin enabled, the operation status of member ports becomes operation up.

### Limitations:
- To correctly obtain the admin-state of LAG interfaces, the configuration needs to be created so that each event-handler instance supports a maximum of 25 ports for LAG interfaces.
  (It is possible to adapt to LAG interfaces with more than 25 ports by creating multiple instances.)

