import pyudev


context = pyudev.Context()
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')
for action, device in monitor:
    print('{0}: {1}'.format(action, device.get('ID_MODEL')))
