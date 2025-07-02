"""
Token Processor Script

This module processes raw acoustic solo token files and outputs structured JSON representations
in three modes:

- **full** (default): Outputs the complete sequence of processed tokens as a flat list.
- **-m**: Splits the token sequence into measures based on the "new_measure" marker, producing a list of measures (each a list of tokens).
- **-b**: Splits the sequence into beats by first splitting into measures and then splitting each measure on "wait:" markers, producing a flattened list of beats. by first splitting into measures and then splitting each measure on "wait:" markers, producing a flattened list of beats.

Usage:
    python token_processor.py           # full mode
    python token_processor.py -m        # measures mode
    python token_processor.py -b        # beats mode
"""
import re
from typing import List, Dict, Tuple, Union
import os
import sys
import json

def is_instrumental(token: str) -> bool:
    return token.startswith("note:")

def strip_non_instrumental(tokens: List[str]) -> Tuple[List[str], Dict[int, str]]:
    pure_tokens: List[str] = []
    removed_map: Dict[int, str] = {}
    for idx, tok in enumerate(tokens):
        if is_instrumental(tok):
            pure_tokens.append(tok)
        else:
            removed_map[idx] = tok
    return pure_tokens, removed_map

def restore_non_instrumental(pure_tokens: List[str], removed_map: Dict[int, str]) -> List[str]:
    total_length = len(pure_tokens) + len(removed_map)
    reconstructed = [None] * total_length
    for idx, tok in removed_map.items():
        reconstructed[idx] = tok
    i_pure = 0
    for i in range(total_length):
        if reconstructed[i] is None:
            reconstructed[i] = pure_tokens[i_pure]
            i_pure += 1
    return reconstructed

def sort_notes(pruned_notes: List[str]):
    def extract_s_number(s):
        match = re.search(r's(\d+):', s)
        return int(match.group(1)) if match else float('inf')
    return sorted(pruned_notes, key=extract_s_number)

def merge_tracks_and_prune(notes: List[str]):
    processed_notes = []
    has_rest = False
    for token in notes:
        cleaned = re.sub(r"clean\d+:", "", token)
        if cleaned == "rest":
            if not has_rest:
                processed_notes.append("rest")
                has_rest = True
        else:
            processed_notes.append(cleaned)
    return sort_notes(processed_notes)

def expand_repeats(tokens: List[str]) -> List[str]:
    expanded, i, n = [], 0, len(tokens)
    while i < n:
        t = tokens[i]
        if t.startswith("measure:repeat_open"):
            j = i+1
            while j < n and not tokens[j].startswith("measure:repeat_close"):
                j += 1
            if j < n and (m := re.match(r"measure:repeat_close:(\d+)", tokens[j])):
                count = int(m.group(1))
                for _ in range(count):
                    expanded.extend(tokens[i+1:j])
                i = j + 1
                continue
        expanded.append(t)
        i += 1
    return expanded

def process_raw_acoustic_solo_tokens(tokens: Union[str, List[str]]):
    if isinstance(tokens, str):
        try:
            with open(tokens) as f:
                tokens = [l.strip() for l in f if l.strip()]
        except FileNotFoundError:
            raise ValueError("Provide encoded tokens or path to token file")
    header, body, footer, in_body = [], [], [], False
    for tok in tokens:
        if tok == "start": in_body = True; header.append(tok)
        elif tok == "end": in_body = False; footer.append(tok)
        elif in_body: body.append(tok)
        else: header.append(tok)
    expanded = expand_repeats(body)
    processed, group = [], []
    for tok in expanded:
        if tok.startswith("clean"): group.append(tok)
        elif tok.startswith(("note","bfs","nfx","wait")):
            if group:
                processed.extend(merge_tracks_and_prune(group)); group = []
            processed.append(tok)
    if group: processed.extend(merge_tracks_and_prune(group))
    return processed

def split_measures(tokens: List[str]) -> List[List[str]]:
    measures, current = [], []
    for t in tokens:
        if t == "new_measure":
            if current:
                measures.append(current)
                current = []
        else:
            current.append(t)
    if current: measures.append(current)
    return measures

def split_beats(measure: List[str]) -> List[List[str]]:
    beats, current = [], []
    for t in measure:
        if t.startswith("wait:"):
            if current:
                beats.append(current)
                current = []
        else:
            current.append(t)
    if current: beats.append(current)
    return beats

def main():
    examples_folder = "../examples"
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"

    # cleanup previous outputs
    for fname in os.listdir(examples_folder):
        if fname.endswith(f"_{mode}.json") or (mode == "full" and fname.endswith("_full.json")):
            os.remove(os.path.join(examples_folder, fname))

    for fn in os.listdir(examples_folder):
        if not fn.endswith(".txt"): continue
        path = os.path.join(examples_folder, fn)
        print(f"Processing {fn} (mode={mode})")
        tokens = process_raw_acoustic_solo_tokens(path)

        if mode == "-m":
            # measures only
            data = split_measures(tokens)
        elif mode == "-b":
            # beats across file (flatten measures then split)
            measures = split_measures(tokens)
            all_beats = []
            for measure in measures:
                all_beats.extend(split_beats(measure))
            data = all_beats
        else:
            # full token sequence
            data = tokens

        # write structure to JSON
        base, _ = os.path.splitext(fn)
        out_name = f"{base}_{mode}.json"
        with open(os.path.join(examples_folder, out_name), 'w') as f:
            json.dump(data, f, indent=2)
        print(f"  → Wrote {out_name}")

if __name__ == "__main__":
    main()
