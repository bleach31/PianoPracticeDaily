Piano Practice Daily
==========================

.. toctree::
   :maxdepth: 2
   :caption: Navigation

   Requirements <#requirements>
   System Architecture <#system-architecture>
   Specifications <#specifications>

Requirements
===================

.. req:: Detect Piano Start
    :id: REQ001

    The system shall detect when the electronic piano is turned on.

.. req:: Detect Piano Stop
    :id: REQ002

    The system shall detect when the electronic piano is turned off.

.. req:: Record Audio
    :id: REQ003

    The system shall record audio during the practice session.

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

    The system shall log the session start time, stop time, and total duration.

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


System Architecture
===================

The following diagram illustrates the system architecture for Piano Practice Daily:

.. needuml:: logical_architecture

    actor User
    package "Piano Practice Daily System" {
        component "Piano Detection Module" as PianoDetection
        component "Audio Recording Module" as AudioRecording
        component "Silence Processing Module" as SilenceProcessing
        component "Storage Module" as Storage
        component "Web Portal" as WebPortal
        component "Notification Module" as Notification
        component "Streaming Module (Optional)" as Streaming
    }

    User --> WebPortal : View Logs & Playback
    User --> Streaming : Listen in Real-time
    PianoDetection --> AudioRecording : Trigger Recording
    AudioRecording --> SilenceProcessing : Process Audio
    SilenceProcessing --> Storage : Save Processed Audio
    Storage --> WebPortal : Provide Audio Files
    WebPortal --> Notification : Send Email Notifications


.. needuml:: physical_architrecture

   actor Trainee
   actor User

   package "Local Resource" {
       [Electronic Piano] as Piano
       [Linux Device] as Linux
   }
   package "Cloud Resource" {
       [Google Drive] as Cloud
   }

   Trainee --> Piano : Plays Piano
   Piano --> Linux : Audio Output (via USB or Line-In)
   Linux --> Cloud : Upload Processed Audio
   Linux --> Cloud : Get Processed Audio List
   User  --> Linux : Web Portal Access (via Browser)
   User  --> Cloud : Access Stored Files (direct access)

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
