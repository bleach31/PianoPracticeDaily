import pyudev
import json
import os
import threading
import time

class AudioDeviceManager:
    """
    The AudioDeviceManager class is responsible for managing the interaction with an audio device,
    such as detecting when the device (e.g., an electronic piano) is connected or disconnected,
    and controlling the audio recording process accordingly.

    Key Responsibilities:
    - Detect the connection and disconnection of the target audio device.
    - Automatically start recording when the device is connected.
    - Automatically stop recording when the device is disconnected.
    - Provide a framework for handling custom actions during device connection or disconnection.

    .. spec:: Audio Device Manager
        :id: CMP001
        :links: REQ001, REQ002, REQ003
    """
    def __init__(self, target_device_criteria=None):
        """
        Initialize the AudioDeviceManager.
        :param target_device_criteria: A dictionary of attributes and values to match the target device.
        """
        self.target_device_criteria = target_device_criteria
        self.recording = False

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
        Start recording and perform custom actions.
        """
        print("Device connected. Starting recording...")
        self.start_recording()
        print("Custom action: Start recording.")

    def on_device_disconnected(self):
        """
        Callback for when the device is disconnected (powered off).
        Stop recording and perform custom actions.
        """
        print("Device disconnected. Stopping recording...")
        self.stop_recording()
        print("Custom action: Stop recording.")

    def start_recording(self):
        """
        Start the audio recording process.
        """
        self.recording = True
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()

    def stop_recording(self):
        """
        Stop the audio recording process.
        """
        self.recording = False
        if hasattr(self, 'recording_thread'):
            self.recording_thread.join()

    def _record_audio(self):
        """
        Simulate audio recording process.
        Replace this with actual audio recording logic.
        """
        print("Recording started...")
        while self.recording:
            time.sleep(1)  # Simulate recording
        print("Recording stopped.")

if __name__ == "__main__":
    # Load configuration from external JSON file
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
        target_device_criteria = config.get("target_device_criteria", {})
    except FileNotFoundError:
        print("Configuration file not found. Using default settings.")
        target_device_criteria = {}

    manager = AudioDeviceManager(target_device_criteria=target_device_criteria)
    manager.monitor()
