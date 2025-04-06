import pyudev


context = pyudev.Context()
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')
for action, device in monitor:
    print('{0}: {1} :{2} :{3} :{4} :{5} :{6}'.format(action, device.get('ID_MODEL'), device.get("ID_USB_MODEL_ID") , device.get("PRODUCT"), device.sys_name, device.get("ID_VENDOR_ID"), device.get("ID_MODEL_ID"))) 
