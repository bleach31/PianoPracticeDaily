.. _system_architecture:

System Architecture
===================

.. _system-architecture:

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
