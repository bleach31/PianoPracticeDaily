.. _specifications:

Specifications
===================

.. spec:: Piano Detection Module
    :id: CMP001
    :links: REQ001, REQ002

    The Piano Detection Module is responsible for detecting when the electronic piano is powered on or off. 
    This module ensures that the system can automatically start and stop recording based on the piano's state.

.. spec:: Audio Recording Module
    :id: CMP002
    :links: REQ003

    The Audio Recording Module handles the recording of audio during the practice session. 
    It starts recording when the piano is detected as powered on.

.. spec:: Silence Processing Module
    :id: CMP003
    :links: REQ005, REQ010

    The Silence Processing Module processes the recorded audio to remove silent periods longer than a specified threshold.

.. spec:: Storage Module
    :id: CMP004
    :links: REQ004

    The Storage Module is responsible for saving the processed audio files to predefined storage locations such as Google Drive, NAS, or Cloud.

.. spec:: Web Portal
    :id: CMP005
    :links: REQ008

    The Web Portal provides a user interface for reviewing daily practice logs and playing back past recordings. 
    It also displays metadata such as session date, duration, and notes.

.. spec:: Notification Module
    :id: CMP006
    :links: REQ007

    The Notification Module sends email notifications containing session information, including start time, stop time, total duration, and a link to the processed audio.

.. spec:: Streaming Module (Optional)
    :id: CMP007
    :links: REQ009

    The Streaming Module provides real-time audio streaming during the piano session. 
    This module is optional and may not be implemented in all deployments.
