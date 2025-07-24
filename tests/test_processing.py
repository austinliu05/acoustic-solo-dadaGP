import os
import pprint
from typing import List

import guitarpro as gp
import pytest
from asdadagp.encoder import guitarpro2tokens
from asdadagp.processor import get_string_tunings, tracks_check

DATA_FOLDER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests", "data"
)


def test_get_string_tunings():
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

    dyens_tyning = ["E5", "B4", "G4", "D4", "G3", "F3"]
    gp_file_tuning(
        os.path.join(DATA_FOLDER_PATH, "bensusan_pierre-dame_lombarde.gp5"),
        celtic_tunings,
        note_tuning=True,
    )
    gp_file_tuning(
        os.path.join(DATA_FOLDER_PATH, "bensusan_pierre-dame_lombarde.gp5"),
        celtic_tunings,
        note_tuning=False,
    )

    gp_file_tuning(
        os.path.join(DATA_FOLDER_PATH, "dyens-roland-la_bicyclette.gp4"),
        dyens_tyning,
        note_tuning=True,
    )
    gp_file_tuning(
        os.path.join(DATA_FOLDER_PATH, "dyens-roland-la_bicyclette.gp4"),
        dyens_tyning,
        note_tuning=False,
    )


def test_extra_track_clean():
    gp_path = os.path.join(DATA_FOLDER_PATH, "dyens-roland-la_bicyclette.gp4")
    song = gp.parse(gp_path)
    tokens = guitarpro2tokens(song, "unknown", verbose=True, note_tuning=True)
    # pprint.pprint(tokens[:10])
    sound_notes = [
        token for token in tokens if token.startswith("clean") and "note" in token
    ]
    extra_rest = [
        token for token in tokens if token.startswith("clean1") and "rest" in token
    ]

    processed_tokens = tracks_check(tokens)
    processed_sound_note = [
        token for token in processed_tokens if token.startswith("note")
    ]


    assert len(sound_notes) == len(
        processed_sound_note
    )  # Ensure no tokens are lost in processing
    assert len(tokens) - len(processed_tokens) == len(extra_rest)
