
# Event Handler for SR-Linux LAG Interface Management

This Python code for an event handler improves the behaviour of LAG interfaces in SR-Linux as follows:

### Current behaviour:
- When the LAG interface is admin disabled, SR-Linux sets the operational state of LAG member ports to down. However, the operational state of the member ports remains up.
- In SR-OS, admin disabling the LAG interface causes the member ports to be disabled and the optical laser to stop. Arista implements similar behaviour.

### Issue:
Since the physical ports are not disabled, the optical lasers of the ports continue to transmit, requiring the peer device to detect the link down using LACP or BFD.

### Code implementation improvements:
- When the LAG interface is admin disabled, the physical ports (not just the LAG member port status) have their operating status set to down. This stops the optical lasers of the physical ports, allowing immediate link down detection by the peer device.
- When the LAG interface is Admin-enabled, the operation status of the member ports is set to operation up.

### Limitations:
- To correctly obtain the admin state of LAG interfaces, the configuration must be set up so that each event handler instance supports a maximum of 25 ports for LAG interfaces.
  (It is possible to accommodate LAG interfaces with more than 25 ports by creating multiple instances. The EH instance can be created up to 20).

