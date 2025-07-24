import os

import guitarpro as gp
from asdadagp.encoder import guitarpro2tokens

DATA_FOLDER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests", "data"
)


def test_strings_tokens():
    celtic_tuning = {
        "s1": "D4",
        "s2": "A3",
        "s3": "G3",
        "s4": "D3",
        "s5": "A2",
        "s6": "D2",
    }
    gp_path = os.path.join(DATA_FOLDER_PATH, "bensusan_pierre-dame_lombarde.gp5")
    song = gp.parse(gp_path)
    tokens = guitarpro2tokens(song, "unknown", verbose=True, note_tuning=True)
    for token in tokens:
        if "note" in token:
            start = token.index("note") + len("note")
            guitar_string = token[start + 1 : start + 3]
            if not token.endswith(celtic_tuning[guitar_string]):
                print(token)
            assert token.endswith(celtic_tuning[guitar_string])

    assert tokens[3] == "start"

    tokens_without_tuning = guitarpro2tokens(
        song, "unknown", verbose=True, note_tuning=False
    )
    for i in range(3, 9):
        assert tokens_without_tuning[i] == celtic_tuning[f"s{i-2}"]

    assert tokens_without_tuning[9] == "start"
