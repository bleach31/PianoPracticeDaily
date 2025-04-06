from mido import MidiFile, MidiTrack, Message

def remove_long_silence_from_midi(input_file, output_file, silence_threshold=5000):
    """
    Remove silent sections longer than the specified threshold from a MIDI file.
    
    Args:
        input_file (str): Path to the input MIDI file.
        output_file (str): Path to save the processed MIDI file.
        silence_threshold (int): Time (in milliseconds) considered as long silence.
    """
    midi = MidiFile(input_file)
    new_midi = MidiFile()

    for track in midi.tracks:
        new_track = MidiTrack()
        time_since_last_note = 0

        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                # If accumulated silence is longer than the threshold, skip it
                if time_since_last_note > silence_threshold:
                    time_since_last_note = 0
                new_track.append(msg)
            else:
                time_since_last_note += msg.time
                new_track.append(msg)  # Keep non-note events (e.g., tempo changes)

        new_midi.tracks.append(new_track)

    new_midi.save(output_file)

# Example usage
remove_long_silence_from_midi('input.mid', 'output.mid', silence_threshold=5000)