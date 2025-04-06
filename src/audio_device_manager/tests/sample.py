import pyudev

context = pyudev.Context()

for device in context.list_devices(subsystem='usb', DEVTYPE='usb_device'):
    print("ID_MODEL:", device.get('ID_MODEL'))