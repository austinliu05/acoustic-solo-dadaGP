import os
from typing import List

import guitarpro as gp
import pytest
from asdadagp.encoder import guitarpro2tokens
from asdadagp.processor import get_string_tunings, tracks_check

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
        "D4",
        "A3",
        "G3",
        "D3",
        "A2",
        "D2",
    ]

    dyens_tuning = ["E4", "B3", "G3", "D3", "G2", "F2"]
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
