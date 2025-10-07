import os

import guitarpro as gp
import pytest
from asdadagp.decoder import asdadagp_decode, tokens2guitarpro
from asdadagp.encoder import asdadagp_encode, guitarpro2tokens
from asdadagp.processor import pre_decoding_processing, tracks_check

DATA_FOLDER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests", "data"
)


@pytest.fixture
def gp_path():
    return os.path.join(DATA_FOLDER_PATH, "brower-leo-un_dia_de_noviembre.gp4")


def test_encode_decode(gp_path):
    def actual_test(read_song, note_tuning, verbose):
        tokens = guitarpro2tokens(read_song, "", verbose, note_tuning)

        processed_tokens = tracks_check(tokens)

        tokens_for_decoding, tunings = pre_decoding_processing(processed_tokens)
        decoded_song = tokens2guitarpro(tokens_for_decoding, verbose, tunings)

        read_track = read_song.tracks[0]
        decoded_track = decoded_song.tracks[0]

        assert len(read_track.measures) == len(decoded_track.measures)
        for i in range(len(read_track.measures)):
            read_measure = read_track.measures[i]
            decoded_measure = decoded_track.measures[i]
            assert len(read_measure.voices) == len(decoded_measure.voices)
            for j in range(len(read_measure.voices)):
                read_voice = read_measure.voices[j]
                decoded_voice = decoded_measure.voices[j]
                assert len(read_voice.beats) == len(decoded_voice.beats)
                for k in range(len(read_voice.beats)):
                    read_beat = read_voice.beats[k]
                    decoded_beat = decoded_voice.beats[k]
                    assert len(read_beat.notes) == len(decoded_beat.notes)
                    for l in range(len(read_beat.notes)):
                        read_note = read_beat.notes[l]
                        decoded_note = decoded_beat.notes[l]
                        assert read_note.value == decoded_note.value
                        assert read_note.string == decoded_note.string
                        assert read_note.realValue == decoded_note.realValue

        encoded_tokens = guitarpro2tokens(decoded_song, "", verbose, note_tuning)
        assert tokens == encoded_tokens

    read_song = gp.parse(gp_path)
    actual_test(read_song, True, False)
    for note_tuning in [True, False]:
        for verbose in [True, False]:
            print(f"Testing with note_tuning={note_tuning}, verbose={verbose}")
            actual_test(read_song, note_tuning, verbose)
