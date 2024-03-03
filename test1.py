import mido
from timeit import default_timer
import time

# Dictionary mapping MIDI note numbers to note names
NOTE_NAMES = {
    0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
}

FRET_NAMES = {
    'E2': [(1, 0)],
    'F2': [(1, 1)],
    'F#2': [(1, 2)],
    'G2': [(1, 3)],
    'G#2': [(1, 4)],
    'A2': [(1, 5), (2, 0)],
    'A#2': [(1, 6), (2, 1)],
    'B2': [(1, 7), (2, 2)],
    'C3': [(1, 8), (2, 3)],
    'C#3': [(1, 9), (2, 4)],
    'D3': [(1, 10), (2, 5)],
    'D#3': [(1, 11), (2, 6)],
    'E3': [(1, 12), (2, 7)],
    'F3': [(1, 13), (2, 8)],
    'F#3': [(1, 14), (2, 9)],
    'G3': [(1, 15), (2, 10)],
    'G#3': [(1, 16), (2, 11)],
    'A3': [(1, 17), (2, 12)],
    'A#3': [(1, 18), (2, 13)],
    'B3': [(1, 19), (2, 14)],
    'C4': [(1, 20), (2, 15)],
    'C#4': [(1, 21), (2, 16)],
    'D4': [(1, 22), (2, 17)],
    'D#4': [(1, 23), (2, 18)],
    'E4': [(1, 24), (2, 19)],
    'F4': [(2, 20), (3, 1)],
    'F#4': [(2, 21), (3, 2)],
    'G4': [(2, 22), (3, 3)],
    'G#4': [(2, 23), (3, 4)],
    'A4': [(2, 24), (3, 5)],
    'A#4': [(3, 6), (4, 16)],
    'B4': [(3, 7), (4, 17)],
    'C5': [(3, 8), (4, 18)],
    'C#5': [(3, 9), (4, 19)],
    'D5': [(3, 10), (4, 20)],
    'D#5': [(3, 11), (4, 21)],
    'E5': [(3, 12), (4, 22)],
    'F5': [(3, 13), (4, 23)],
    'F#5': [(3, 14), (4, 24)],
    'G5': [(3, 15), (5, 0)],
    'G#5': [(3, 16), (5, 1)],
    'A5': [(3, 17), (5, 2)],
    'A#5': [(3, 18), (5, 3)],
    'B5': [(3, 19), (5, 4)],
    'C6': [(3, 20), (5, 5)],
    'C#6': [(3, 21), (5, 6)],
    'D6': [(3, 22), (5, 7)],
    'D#6': [(3, 23), (5, 8)],
    'E6': [(3, 24), (5, 9)]
}
def write_note_names(track, output_file, midif):
    with open(output_file, 'w') as f:
        notes_on = {}  # Dictionary to store note-on events
        tempo = 500000  # Default tempo value in microseconds per beat
        for msg in track:
            if msg.type == "set_tempo":
                tempo = msg.tempo
            elif msg.type == 'note_on':
                # Store note-on events with their timestamps
                notes_on[msg.note] = msg.time
            elif msg.type == 'note_off':
                # If corresponding note-on exists, calculate duration and write
                if msg.note in notes_on:
                    start_time = notes_on.pop(msg.note)
                    duration_ticks = msg.time - start_time
                    duration_seconds = mido.tick2second(duration_ticks, midif.ticks_per_beat, tempo)
                    note_name = NOTE_NAMES[msg.note % 12] + str(msg.note // 12 - 1)
                    string_index = FRET_NAMES[note_name][0][0] - 1
                    fret = str(FRET_NAMES[note_name][0][1])
                    notes_string = ['-'] * 6
                    notes_string[string_index] = fret if len(fret) == 1 else '-'
                    f.write('|'.join(notes_string))
                    f.write(f'|{duration_seconds:.2f}|\n')

def separate_tracks(midifile):
    tracks = {}
    for i, track in enumerate(midifile.tracks):
        track_name = track.name if track.name else f'Track_{i+1}'
        tracks[track_name] = track
    return tracks
def remove_dupes(midifile):
    message_numbers = []
    duplicates = []
    for track in midifile.tracks:
        if len(track) in message_numbers:
            duplicates.append(track)
        else:
            message_numbers.append(len(track))
    for track in duplicates:
        midifile.tracks.remove(track)

if __name__ == "__main__":
    midi_file = mido.MidiFile('Metallica_-_Nothing_Else_Matters.mid')

    remove_dupes(midi_file)

    midi_file.save('new_song.mid')

    output_file = 'note_names.txt'

    tracks = separate_tracks(midi_file)
    for i, track_name in enumerate(tracks.keys()):
        print(f"{i + 1}: {track_name}")

    chosen_track_index = int(input(f"Which track do you want to choose? Pick a number from 1 to {len(tracks)}: ")) - 1
    chosen_track = list(tracks.values())[chosen_track_index]

    write_note_names(chosen_track, output_file, midi_file)

    print(f"Note names extracted from track '{list(tracks.keys())[chosen_track_index]}' and saved to {output_file}.")