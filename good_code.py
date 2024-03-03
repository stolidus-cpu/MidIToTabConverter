import mido
from timeit import default_timer
import time

# Dictionary mapping MIDI note numbers to note names
NOTE_NAMES = {
    0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
}
FRET_NAMES = {'E2': (1, 0), 'F2': (1, 1), 'F#2': (1, 2), 'G2': (1, 3), 'G#2': (1, 4), 'A2': (1, 5), 'A#2': (1, 6), 'B2': (1, 7), 'C3': (1, 8), 'C#3': (1, 9), 'D3': (1, 10), 'D#3': (1, 11), 'E3': (1, 12), 'F3': (1, 13), 'F#3': (1, 14), 'G3': (1, 15), 'G#3': (1, 16), 'A3': (1, 17), 'A#3': (1, 18), 'B3': (1, 19), 'C4': (1, 20), 'C#4': (1, 21), 'D4': (1, 22), 'D#4': (1, 23), 'E4': (1, 24),
              'A2': (2, 0), 'A#2': (2, 1), 'B2': (2, 2), 'C3': (2, 3), 'C#3': (2, 4), 'D3': (2, 5), 'D#3': (2, 6), 'E3': (2, 7), 'F3': (2, 8), 'F#3': (2, 9), 'G3': (2, 10), 'G#3': (2, 11), 'A3': (2, 12), 'A#3': (2, 13), 'B3': (2, 14), 'C4': (2, 15), 'C#4': (2, 16), 'D4': (2, 17), 'D#4': (2, 18), 'E4': (2, 19), 'F4': (2, 20), 'F#4': (2, 21), 'G4': (2, 22), 'G#4': (2, 23), 'A4': (2, 24),
              'D3': (3, 0), 'D#3': (3, 1), 'E3': (3, 2), 'F3': (3, 3), 'F#3': (3, 4), 'G3': (3, 5), 'G#3': (3, 6), 'A3': (3, 7), 'A#3': (3, 8), 'B3': (3, 9), 'C4': (3, 10), 'C#4': (3, 11), 'D4': (3, 12), 'D#4': (3, 13), 'E4': (3, 14), 'F4': (3, 15), 'F#4': (3, 16), 'G4': (3, 17), 'G#4': (3, 18), 'A4': (3, 19), 'A#4': (3, 20), 'B4': (3, 21), 'C5': (3, 22), 'C#5': (3, 23), 'D5': (3, 24),
              'G3': (4, 0), 'G#3': (4, 1), 'A3': (4, 2), 'A#3': (4, 3), 'B3': (4, 4), 'C4': (4, 5), 'C#4': (4, 6), 'D4': (4, 7), 'D#4': (4, 8), 'E4': (4, 9), 'F4': (4, 10), 'F#4': (4, 11), 'G4': (4, 12), 'G#4': (4, 13), 'A4': (4, 14), 'A#4': (4, 15), 'B4': (4, 16), 'C5': (4, 17), 'C#5': (4, 18), 'D5': (4, 19), 'D#5': (4, 20), 'E5': (4, 21), 'F5': (4, 22), 'F#5': (4, 23), 'G5': (4, 24),
              'B3': (5, 0), 'C4': (5, 1), 'C#4': (5, 2), 'D4': (5, 3), 'D#4': (5, 4), 'E4': (5, 5), 'F4': (5, 6), 'F#4': (5, 7), 'G4': (5, 8), 'G#4': (5, 9), 'A4': (5, 10), 'A#4': (5, 11), 'B4': (5, 12), 'C5': (5, 13), 'C#5': (5, 14), 'D5': (5, 15), 'D#5': (5, 16), 'E5': (5, 17), 'F5': (5, 18), 'F#5': (5, 19), 'G5': (5, 20), 'G#5': (5, 21), 'A5': (5, 22), 'A#5': (5, 23), 'B5': (5, 24),
              'E4': (6, 0), 'F4': (6, 1), 'F#4': (6, 2), 'G4': (6, 3), 'G#4': (6, 4), 'A4': (6, 5), 'A#4': (6, 6), 'B4': (6, 7), 'C5': (6, 8), 'C#5': (6, 9), 'D5': (6, 10), 'D#5': (6, 11), 'E5': (6, 12), 'F5': (6, 13), 'F#5': (6, 14), 'G5': (6, 15), 'G#5': (6, 16), 'A5': (6, 17), 'A#5': (6, 18), 'B5': (6, 19), 'C6': (6, 20), 'C#6': (6, 21), 'D6': (6, 22), 'D#6': (6, 23), 'E6': (6, 24)
}

def write_note_names(track, output_file, midif):
    with open(output_file, 'w') as f:
        current_time = 0
        notes_at_time = {}
        tempo = None
        for msg in track:
            current_time += msg.time
            if msg.type == "set_tempo":
                tempo = msg.tempo
            if msg.type == 'note_on':
                start_timer = default_timer()
                note_name = NOTE_NAMES[msg.note % 12] + str(msg.note // 12 - 1)
                if current_time not in notes_at_time:
                    notes_at_time[current_time] = []
                notes_at_time[current_time].append(note_name)

        # Write notes, concatenating notes played at the same time
        for time, notes in sorted(notes_at_time.items()):
            notes_string = ['-'] * 6  # Initialize with '-' for each string position
            for note in notes:
                string_index = FRET_NAMES[note][0] - 1
                fret = str(FRET_NAMES[note][1])
                notes_string[string_index] = fret if len(fret) == 1 else '-'
            f.write('|'.join(notes_string))
            time_in_seconds = mido.tick2second(time, midif.ticks_per_beat, tempo)
            f.write(f'|{time_in_seconds:.2f}| \n')
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