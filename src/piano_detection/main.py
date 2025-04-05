import pyudev
import json

class PianoDetector:
    def __init__(self, target_device_criteria=None):
        """
        Initialize the PianoDetector.
        :param target_device_criteria: A dictionary of attributes and values to match the target device.
        """
        self.target_device_criteria = target_device_criteria

    def monitor(self):
        """
        Monitor USB events asynchronously and detect the target device's connection or disconnection.
        """
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb', device_type='usb_device')

        def handle_event(action, device):
            """
            Handle USB events asynchronously.
            :param action: The action performed (e.g., 'add', 'remove').
            :param device: The device object.
            """
            if self._matches_criteria(device):
                if action == "add":
                    print("Piano powered ON")
                    self.on_device_connected()
                elif action == "remove":
                    print("Piano powered OFF")
                    self.on_device_disconnected()

        observer = pyudev.MonitorObserver(monitor, handle_event)
        print(f"Monitoring USB events for device matching criteria: {self.target_device_criteria}")
        observer.start()

        try:
            while True:
                pass  # Keep the main thread alive to allow asynchronous monitoring
        except KeyboardInterrupt:
            print("Stopping monitor...")
            observer.stop()

    def _matches_criteria(self, device):
        """
        Check if the device matches the target criteria.
        :param device: The device object.
        :return: True if the device matches, False otherwise.
        """
        for key, value in self.target_device_criteria.items():
            if device.get(key) != value:
                return False
        return True

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
        target_device_criteria = config.get("target_device_criteria", {})
    except FileNotFoundError:
        print("Configuration file not found. Using default settings.")
        target_device_criteria = {}

    detector = CustomPianoDetector(target_device_criteria=target_device_criteria)
    detector.monitor()
