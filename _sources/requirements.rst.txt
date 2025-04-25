Requirements
===================

.. req:: Detect Piano Start
    :id: REQ001

    The system shall detect when the electronic piano is turned on and automatically start recording audio.

.. req:: Detect Piano Stop
    :id: REQ002

    The system shall detect when the electronic piano is turned off and automatically stop recording audio.

.. req:: Record Audio
    :id: REQ003

    The system shall record audio during the practice session, starting when the piano is turned on and stopping when the piano is turned off.

.. req:: Store Audio on Storage
    :id: REQ004

    The system shall store the recorded audio either in Google Drive or NAS or Cloud.

.. req:: Remove Silence
    :id: REQ005
    :links: REQ010

    The system shall remove silent periods longer than a specified threshold from the recording.
    Silent periods are defined as described in id: ``REQ010``.

.. req:: Log Practice Time
    :id: REQ006

    The system shall log the session start time, stop time, and total duration, triggered by the piano's power state changes.

.. req:: Send Email Notification
    :id: REQ007

    The system shall send an email with session information, including start time, stop time, total duration, and a link to the processed audio.

.. req:: Web Portal for History
    :id: REQ008

    The system shall provide a website that displays daily practice logs and allows playback of past recordings.

    - The web interface shall allow users to view a list of recorded sessions.
    - Users shall be able to play back audio files directly from the web interface.
    - The interface shall display metadata such as session date, duration, and any notes.

.. req:: Real-time Streaming (Optional)
    :id: REQ009

    The system may support real-time streaming of the piano session.

.. req:: Silence Threshold
    :id: REQ010

    Silence is defined as a continuous period of no audio for more than a configurable number of seconds (e.g., 5 seconds).

.. req:: Single MIDI Device Detection
    :id: REQ011

    The system shall detect only one MIDI device at a time and proceed sequentially through detection, recording, and termination.

.. req:: Immediate Recording on Startup
    :id: REQ012

    The system shall immediately start recording if a MIDI device is already active when the script starts.

.. req:: Reliable MIDI Device Detection
    :id: REQ013

    The system shall reliably detect MIDI devices even in cases where timing issues may occur.
