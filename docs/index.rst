Piano Practice Daily
==========================

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

    The system shall remove silent periods longer than a specified threshold from the recording.

.. req:: Log Practice Time
    :id: REQ006

    The system shall log the session start time, stop time, and total duration.

.. req:: Send Email Notification
    :id: REQ007

    The system shall send an email with session information, including start time, stop time, total duration, and a link to the processed audio.

.. req:: Web Portal for History
    :id: REQ008

    The system shall provide a website that displays daily practice logs and allows playback of past recordings.

.. req:: Real-time Streaming (Optional)
    :id: REQ009

    The system may support real-time streaming of the piano session.

.. req:: Silence Threshold
    :id: REQ010

    Silence is defined as a continuous period of no audio for more than a configurable number of seconds (e.g., 5 seconds).

.. req:: Detect Piano Power On
    :id: REQ011

    Detects when the piano is powered on.

.. req:: Detect Piano Power Off
    :id: REQ012

    Detects when the piano is powered off.

.. req:: Start Audio Recording
    :id: REQ013

    Starts audio recording once the piano is turned on.

.. req:: Save Audio File
    :id: REQ014

    Saves the recorded audio to a predefined storage.

.. req:: Process and Trim Silence
    :id: REQ015

    Removes silent sections based on the silence threshold.

.. req:: Log Session Data
    :id: REQ016

    Logs session metadata: start time, end time, duration.

.. req:: Send Summary Email
    :id: REQ017

    Sends an email containing session information and the recording link.

.. req:: Display Log via Web
    :id: REQ018

    Provides a web interface for reviewing daily logs and playback.

    - The web interface shall allow users to view a list of recorded sessions.
    - Users shall be able to play back audio files directly from the web interface.
    - The interface shall display metadata such as session date, duration, and any notes.

.. req:: Stream Audio in Real-time
    :id: REQ019

    Streams audio live during the session.


System Architecture
===================

The following diagram illustrates the system architecture for Piano Practice Daily:

.. uml:: system_architecture
   :caption: System Architecture Diagram

    @startuml
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
    @enduml

.. uml:: physical_connections
   :caption: Physical Connections Diagram

   @startuml
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
   @enduml