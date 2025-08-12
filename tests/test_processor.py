import os
from typing import List

import guitarpro as gp
import pytest
from asdadagp.encoder import guitarpro2tokens
from asdadagp.processor import (
    get_string_tunings,
    measures_playing_order,
    repeat_related_measure_indices,
    split_tokens_to_measures,
    tokens_to_measures,
    tracks_check,
)

DATA_FOLDER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests", "data"
)


@pytest.fixture
def celtic_tuning_gp_path():
    return os.path.join(DATA_FOLDER_PATH, "bensusan_pierre-dame_lombarde.gp5")


@pytest.fixture
def multi_tracks_gp_path():
    return os.path.join(DATA_FOLDER_PATH, "dyens-roland-la_bicyclette.gp4")


@pytest.fixture
def multi_track_tokens(multi_tracks_gp_path):
    song = gp.parse(multi_tracks_gp_path)
    tokens = guitarpro2tokens(song, "unknown", verbose=True, note_tuning=True)
    return tokens


@pytest.fixture
def repeat_bars_gp_path():
    # https://www.songsterr.com/a/wsa/leo-brouwer-un-dia-de-noviembre-classical-guitar-tab-s903099
    return os.path.join(DATA_FOLDER_PATH, "brower-leo-un_dia_de_noviembre.gp4")


@pytest.fixture
def repeat_bars_tokens(repeat_bars_gp_path):
    song = gp.parse(repeat_bars_gp_path)
    tokens = guitarpro2tokens(song, "unknown", verbose=True, note_tuning=True)
    return tokens


def test_get_string_tunings(celtic_tuning_gp_path, multi_tracks_gp_path):
    def gp_file_tuning(
        gp_path: str,
        correct_tuning: List[str],
        note_tuning: bool = True,
    ):
        song = gp.parse(gp_path)
        tokens = guitarpro2tokens(
            song, "unknown", verbose=True, note_tuning=note_tuning
        )
        tuning_results = get_string_tunings(tokens)
        assert (
            tuning_results == correct_tuning
        ), f"Expected {correct_tuning}, got {tuning_results}"

    celtic_tunings = [
        "D5",
        "A4",
        "G4",
        "D4",
        "A3",
        "D3",
    ]

    dyens_tuning = ["E5", "B4", "G4", "D4", "G3", "F3"]
    gp_file_tuning(
        celtic_tuning_gp_path,
        celtic_tunings,
        note_tuning=True,
    )
    gp_file_tuning(
        celtic_tuning_gp_path,
        celtic_tunings,
        note_tuning=False,
    )

    gp_file_tuning(
        multi_tracks_gp_path,
        dyens_tuning,
        note_tuning=True,
    )
    gp_file_tuning(
        multi_tracks_gp_path,
        dyens_tuning,
        note_tuning=False,
    )


def test_extra_track_merge(multi_track_tokens):
    sound_notes = [
        token
        for token in multi_track_tokens
        if token.startswith("clean") and "note" in token
    ]

    processed_tokens = tracks_check(multi_track_tokens)
    assert isinstance(processed_tokens, list)
    processed_sound_note = [
        token for token in processed_tokens if token.startswith("note")
    ]

    assert len(sound_notes) == len(
        processed_sound_note
    )  # Ensure no tokens are lost in processing


def test_extra_tracks_removal(multi_track_tokens):
    main_track = [token for token in multi_track_tokens if token.startswith("clean0")]
    main_track_notes = [token for token in main_track if "note" in token]

    processed_tokens = tracks_check(multi_track_tokens, False)
    assert isinstance(processed_tokens, list)
    processed_sound_note = [
        token for token in processed_tokens if token.startswith("note")
    ]

    assert len(main_track_notes) == len(
        processed_sound_note
    )  # Ensure no tokens are lost in processing

    assert len(main_track) == len(processed_sound_note) + processed_tokens.count("rest")


def test_split_measures(repeat_bars_tokens):
    # 77 bars + header
    measure_tokens = split_tokens_to_measures(repeat_bars_tokens)
    assert len(measure_tokens) == 78

    processed_tokens = tracks_check(repeat_bars_tokens, True)
    processed_measure_tokens = split_tokens_to_measures(processed_tokens)
    assert len(processed_measure_tokens) == 78


def test_measures(repeat_bars_tokens):
    print(len(repeat_bars_tokens))
    print(repeat_bars_tokens[-10:])

    measures = tokens_to_measures(repeat_bars_tokens)
    assert len(measures) == 77

    all_instrumental_tokens = [t for measure in measures for t in measure.tokens]
    assert len(all_instrumental_tokens) == 1129

    opens, closes, alternatives = repeat_related_measure_indices(measures)
    assert opens == [1, 9, 28]
    assert closes == [8, 25, 49]
    assert alternatives == [25, 26, 49, 50]

    measure_play_order = measures_playing_order(measures)
    assert len(measure_play_order) == 122

    assert measure_play_order == [0] + list(range(1, 9)) + list(range(1, 9)) + list(
        range(9, 26)
    ) + list(range(9, 25)) + [26, 27] + list(range(28, 50)) + list(
        range(28, 49)
    ) + list(
        range(50, 77)
    )

    play_order_tokens = measures_playing_order(measures, tokens=True)
    assert len(play_order_tokens) == 122
