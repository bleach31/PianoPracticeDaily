import pyudev
import json

class PianoDetector:
    def __init__(self, target_device_name="ARIUS"):
        """
        Initialize the PianoDetector.
        :param target_device_name: The name of the USB device to monitor.
        """
        self.target_device_name = target_device_name

    def monitor(self):
        """
        Monitor USB events and detect the target device's connection or disconnection.
        """
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb')

        print(f"Monitoring USB events for device: {self.target_device_name}")
        for device in iter(monitor.poll, None):
            if device.action == "add" and self.target_device_name in device.device_path:
                print("Piano powered ON")
                self.on_device_connected()
            elif device.action == "remove" and self.target_device_name in device.device_path:
                print("Piano powered OFF")
                self.on_device_disconnected()

    def on_device_connected(self):
        """
        Callback for when the device is connected (powered on).
        Override this method to implement custom behavior.
        """
        print("Device connected. Implement custom behavior here.")

    def on_device_disconnected(self):
        """
        Callback for when the device is disconnected (powered off).
        Override this method to implement custom behavior.
        """
        print("Device disconnected. Implement custom behavior here.")

class CustomPianoDetector(PianoDetector):
    def on_device_connected(self):
        print("Custom action: Start recording.")

    def on_device_disconnected(self):
        print("Custom action: Stop recording.")

if __name__ == "__main__":
    # Load configuration from external JSON file
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
        target_device_name = config.get("target_device_name", "ARIUS")
    except FileNotFoundError:
        print("Configuration file not found. Using default settings.")
        target_device_name = "ARIUS"

    detector = CustomPianoDetector(target_device_name=target_device_name)
    detector.monitor()
