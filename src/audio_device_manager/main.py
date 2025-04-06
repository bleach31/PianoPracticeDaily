import pyudev
import json
import os
import threading
import time
import subprocess
import re
import tomllib  # Use tomllib for Python 3.11+; for older versions, use `import toml` instead
import sys  # Add this import at the top of the file
import datetime  # Add this import for timestamp generation

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
    def __init__(self, target_device_criteria=None, target_name=None):
        """
        Initialize the AudioDeviceManager.
        :param target_device_criteria: A list of dictionaries of attributes and values to match the target device.
        :param target_name: The name of the target MIDI device.
        """
        self.target_device_criteria = target_device_criteria
        self.target_name = target_name
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
                    self.on_device_connected(device)
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
        Check if the device matches any of the target criteria.
        :param device: The device object.
        :return: True if the device matches any criteria, False otherwise.
        """
        for criteria in self.target_device_criteria:
            match = all(device.get(key) == value for key, value in criteria.items())
            if match:
                return True
        return False

    def _get_arecordmidi_port(self, device):
        """
        Retrieve the ALSA MIDI port for the matched device using arecordmidi -l.
        :param device: The device object.
        :return: The MIDI port string (e.g., '28:0').
        """
        try:
            # Run arecordmidi -l to list available MIDI ports
            result = subprocess.run(
                ["arecordmidi", "-l"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f"Error running arecordmidi -l: {result.stderr.strip()}")
            # Parse the output to find the port for the target device
            if not self.target_name:
                raise ValueError("Target device name is not specified.")
            for line in result.stdout.splitlines():
                match = re.match(r"^\s*(\d+:\d+)\s+.*\b" + re.escape(self.target_name) + r"\b.*$", line)
                if match:
                    midi_port = match.group(1)
                    print(f"Debug: Found MIDI port for {self.target_name}: {midi_port}")
                    return midi_port
            raise ValueError(f"Target device '{self.target_name}' not found in arecordmidi -l output.")
        except Exception as e:
            raise RuntimeError(f"Failed to determine MIDI port: {e}")

    def on_device_connected(self, device):
        """
        Callback for when the device is connected (powered on).
        Start recording and perform custom actions.
        """
        print("Device connected. Determining MIDI port...")
        try:
            self.midi_port = self._get_arecordmidi_port(device)
            self.start_recording()
        except Exception as e:
            print(f"Error determining MIDI port: {e}")

    def on_device_disconnected(self):
        """
        Callback for when the device is disconnected (powered off).
        Stop recording and perform custom actions.
        """
        print("Device disconnected. Stopping recording...")
        self.stop_recording()

    def start_recording(self):
        """
        Start the audio recording process using arecordmidi.
        """
        print("Recording started with arecordmidi...")
        try:
            if not hasattr(self, 'midi_port'):
                raise ValueError("MIDI port is not set. Cannot start recording.")
            
            # Generate a unique filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{timestamp}.mid"
            print(f"Recording to file: {output_file}")
            
            # Start the arecordmidi process
            self.recording_process = subprocess.Popen(
                ["arecordmidi", "-p", self.midi_port, output_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # Ensure output is in text format
            )
            print("Recording process started.")
        except Exception as e:
            print(f"Error starting recording: {e}")

    def stop_recording(self):
        """
        Stop the audio recording process.
        """
        if hasattr(self, 'recording_process') and self.recording_process.poll() is None:
            # Send SIGINT to gracefully stop the arecordmidi process
            self.recording_process.send_signal(subprocess.signal.SIGINT)
            self.recording_process.wait()
            print("Recording process stopped.")

if __name__ == "__main__":
    # Load configuration from external TOML file
    try:
        with open("config.toml", "rb") as config_file:  # Use "rb" mode for tomllib
            config = tomllib.load(config_file)  # Parse the TOML configuration

        # Load pyudev target device criteria
        target_device_criteria = config.get("pyudev_target_device_crieria", {})
        if not isinstance(target_device_criteria, dict):
            print("Error: 'pyudev_target_device_crieria' must be a dictionary.")
            sys.exit(1)

        # Wrap the single dictionary into a list for consistency
        target_device_criteria = [target_device_criteria]

        # Load arecordmidi target device criteria
        arecordmidi_criteria = config.get("arecordmidi_target_device_crieria", {})
        target_name = arecordmidi_criteria.get("port_name")
        if not target_name:
            print("Error: 'port_name' is missing in 'arecordmidi_target_device_crieria'.")
            sys.exit(1)

    except FileNotFoundError:
        print("Configuration file not found. Using default settings.")
        sys.exit(1)
    except tomllib.TOMLDecodeError as e:
        print(f"Error decoding TOML configuration: {e}")
        sys.exit(1)

    manager = AudioDeviceManager(target_device_criteria=target_device_criteria, target_name=target_name)
    manager.monitor()
