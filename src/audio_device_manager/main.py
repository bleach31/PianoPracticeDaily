from storage import session_manager
import pyudev
import json
import os
import threading
import time
import subprocess
import re
import yaml  # Import YAML for configuration parsing
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
    def __init__(self, target_device_criteria=None, target_name=None, session_file_path="practice_sessions.json"):
        """
        Initialize the AudioDeviceManager.
        :param target_device_criteria: A list of dictionaries of attributes and values to match the target device.
        :param target_name: The name of the target MIDI device.
        :param session_file_path: Path to the session file.
        """
        self.target_device_criteria = target_device_criteria
        self.target_name = target_name
        self.recording = False
        self.session_manager = session_manager.PracticeSessionManager(session_file_path)  # JSONファイルのパス


    def monitor(self):
        """
        Monitor USB events asynchronously and detect the target device's connection or disconnection.
        Also checks for already connected devices at the start.
        """
        context = pyudev.Context()

        # Check if the device is already connected
        for device in context.list_devices(subsystem='usb', device_type='usb_device'):
            if self._matches_criteria(device):
                print("Device already connected. Determining MIDI port...")
                try:
                    self.midi_port = self._get_arecordmidi_port()
                    self.start_recording()
                except Exception as e:
                    print(f"Error determining MIDI port: {e}")
                return

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
                    print("Device connected. Determining MIDI port...")
                    try:
                        self.midi_port = self._get_arecordmidi_port()
                        self.start_recording()
                    except Exception as e:
                        print(f"Error determining MIDI port: {e}")
                elif action == "remove":
                    print("Device disconnected. Stopping recording...")
                    self.stop_recording()

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

    def _get_arecordmidi_port(self):
        """
        Retrieve the ALSA MIDI port for the matched device using arecordmidi -l with retry logic.
        """
        retries = 3
        delay = 2  # seconds
        for attempt in range(retries):
            try:
                result = subprocess.run(
                    ["arecordmidi", "-l"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.returncode != 0:
                    raise RuntimeError(f"Error running arecordmidi -l: {result.stderr.strip()}")

                for line in result.stdout.splitlines():
                    match = re.match(r"^\s*(\d+:\d+)\s+.*\b" + re.escape(self.target_name) + r"\b.*$", line)
                    if match:
                        return match.group(1)
                raise ValueError(f"Target device '{self.target_name}' not found in arecordmidi -l output.")
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise

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

            # Save the session to JSON
            stop_time = datetime.datetime.now()
            self.session_manager.add_session(
                start_time=self.start_time,
                stop_time=stop_time,
                midi_file_path=self.output_file
            )

if __name__ == "__main__":
    # Load configuration from external YAML file
    try:
        with open("config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)  # Parse the YAML configuration

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

        # Load session file path from config.yaml
        session_file_path = config.get("session_file_path", "practice_sessions.json")

    except FileNotFoundError:
        print("Configuration file not found. Using default settings.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error decoding YAML configuration: {e}")
        sys.exit(1)

    manager = AudioDeviceManager(target_device_criteria=target_device_criteria, target_name=target_name, session_file_path=session_file_path)
    manager.monitor()
