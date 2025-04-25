Specifications
===================

.. spec:: Audio Device Manager
    :id: CMP001
    :links: REQ001, REQ002, REQ003

    The Audio Device Manager is responsible for detecting when the electronic piano is powered on or off and managing audio recording. 
    This module ensures that the system automatically starts recording when the piano is powered on and stops recording when it is powered off.

.. spec:: Silence Processing Module
    :id: CMP002
    :links: REQ005, REQ010

    The Silence Processing Module processes the recorded audio to remove silent periods longer than a specified threshold.

.. spec:: Storage Module
    :id: CMP003
    :links: REQ004

    The Storage Module is responsible for saving the processed audio files to predefined storage locations such as Google Drive, NAS, or Cloud.

.. spec:: Web Portal
    :id: CMP004
    :links: REQ008

    The Web Portal provides a user interface for reviewing diary practice logs and playing back past recordings. 
    It also displays metadata such as session date, duration, and notes.

.. spec:: Notification Module
    :id: CMP005
    :links: REQ007

    The Notification Module sends email notifications containing session information, including start time, stop time, total duration, and a link to the processed audio.

.. spec:: Streaming Module (Optional)
    :id: CMP006
    :links: REQ009

    The Streaming Module provides real-time audio streaming during the piano session. 
    This module is optional and may not be implemented in all deployments.

.. spec:: Enhanced MIDI Device Handling
    :id: CMP007
    :links: REQ011, REQ012, REQ013

    The Audio Device Manager shall handle a single MIDI device at a time, start recording immediately if the device is active on script startup, and use retry logic with wait time to ensure reliable detection of MIDI devices.
