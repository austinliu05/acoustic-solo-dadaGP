"""
Goal: raw tokens --> mergetracks

"""

import logging
import re
from typing import Dict, List, Tuple, Union

_LOGGER = logging.getLogger(__name__)


def get_string_tunings(tokens: List[str]) -> List[str]:
    """
    Extracts string tunings from the provided tokens.

    :param tokens: List of tokens from which to extract string tunings.
    :type tokens:
    :return: tuning of the song / tab
    :rtype:
    """
    if tokens[9] == "start":
        note_tuning = False
    elif tokens[3] == "start":
        note_tuning = True
    else:
        note_tuning = True
        _LOGGER.warning("'start' token not found in expected positions.")

    if note_tuning:
        string_tuning_dict = {}
        while len(string_tuning_dict) < 6:
            for token in tokens:
                if token.startswith("clean") and "note" in token:
                    start = token.index("note") + len("note")
                    guitar_string = int(token[start + 2])
                    tuning = token.split(":")[-1]
                    string_tuning_dict[guitar_string] = tuning

        return [string_tuning_dict[i] for i in range(1, 7)]
    else:
        return tokens[
            3:9
        ]  # Assuming the first 6 tokens after "start" are the string tunings


def merge_tracks_and_prune(notes: List[str]) -> List[str]:

    processed_notes = [re.sub(r"clean\d+:", "", token).strip() for token in notes]

    # for token in notes:
    #     # Remove any track prefix ("clean0:" or "clean1:" etc).
    #     cleaned_token = re.sub(r"clean\d+:", "", token)
    #     processed_notes.append(cleaned_token)

    if set(processed_notes) == {"rest"}:
        return ["rest"]
    else:
        return sort_notes([note for note in processed_notes if note != "rest"])


def sort_notes(pruned_notes: List[str]) -> List[str]:
    # Define a key function for sorting based on "s<number>:" in the token.
    def extract_s_number(s):
        match = re.search(r"s(\d+):", s)
        # If not found, push token to the end.
        return int(match.group(1)) if match else float("inf")

    sorted_notes = sorted(pruned_notes, key=extract_s_number)
    return sorted_notes


def tracks_check(tokens: List[str], merge_track: bool = True) -> List[str]:
    processed = []
    if not merge_track:
        # only remain clean0
        for token in tokens:
            if token.startswith("clean"):
                if token[5] == "0":
                    processed.append(token.replace("clean0:", ""))
                else:
                    continue
            else:
                processed.append(token)
    else:
        current_group = []
        for token in tokens:
            # Group any 'clean' tracks
            if token.startswith("clean"):
                current_group.append(token)
                continue
            else:
                if current_group:
                    merged = merge_tracks_and_prune(current_group)
                    processed.extend(merged)
                    current_group = []

                processed.append(token)

        if current_group:
            merged = merge_tracks_and_prune(current_group)
            processed.extend(merged)

    return processed


def process_tokens(
    tokens: Union[str, List[str]], merge_tracks: bool = True
) -> Dict[str, Union[List[str], List[bool], List[List[int]], List[List[List[int]]]]]:
    """

    :param tokens: output from .encoder.guitarpro2tokens
    :type tokens: str (path to txt file) or list of tokens
    :return: {
        "tokens": [<tokens after track merge>],
        "instrumental": [<bool indicate if token at that index is instrumental or not>],
        ""
    }
    :rtype:
    """
    results = {}
    if isinstance(tokens, str):
        with open(tokens, "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
    # results["original"] = tokens
    results["tuning"] = get_string_tunings(tokens)
    # step 1. merge tracks
    results["tokens"] = tracks_check(tokens, merge_tracks)

    return results


def process_raw_tokens(tokens: Union[str, List[str]]) -> Dict[str, Dict]:
    """
    Processes raw tokens from a file or a list of strings.
    - Merges tracks and removes clean prefixes.
    - Expands repeat measures.
    """
    if isinstance(tokens, str):
        with open(tokens, "r") as f:
            tokens = [line.strip() for line in f if line.strip()]

    results = {}
    # get string tunings
    results["tuning"] = get_string_tunings(tokens)
    # get original measures
    raw_measures = []
    current_measure = []
    return results


def raw_tokens_splits(tokens):
    pass


class GpSongTokensProcessor:
    """
    Note token pipeline:
    1. merge tracks & remove clean prefixes
    """

    def __init__(self, tokens: Union[str, List[str]]):
        """
        :param tokens:
        :type tokens:
        """
        if isinstance(tokens, str):
            with open(tokens, "r") as f:
                self.tokens = [line.strip() for line in f if line.strip()]
        elif isinstance(tokens, list):
            self.tokens = tokens
        else:
            raise ValueError(
                "A path to token txt file or a list of tokens is required."
            )

        self.get_string_tunings()
        self.measures = None
        self.beats = None
        self.string_tunings = None

    def split_measures(self):
        """
        Extracts measures from the tokens.
        """
        token_measures = []
        id_measures = []
        current_measure_tokens = []
        current_measure_token_ids = []
        current_measure_index = 0
        last_measure_index = 0
        in_repeat = False
        repeat_start_index = -1

        for i, token in enumerate(self.tokens):
            if token_measures == [] and current_measure_tokens == []:
                if token != "new_measure":
                    continue
            if token == "measure:repeat_open":
                in_repeat = True
                repeat_start_index = current_measure_index
            elif token == "new_measure":
                token_measures.append(current_measure_tokens)
                id_measures.append(current_measure_token_ids)
                current_measure_index += 1


def is_instrumental(token: str) -> bool:
    return token.startswith("note:")


def strip_non_instrumental(tokens: List[str]) -> Tuple[List[str], Dict[int, str]]:
    """
    Returns:
      - pure_tokens:    [ all tokens t where is_instrumental(t) is True ]
      - removed_map:    { original_index: removed_token } for each token
                        where is_instrumental(token) is False.
    """
    pure_tokens: List[str] = []
    removed_map: Dict[int, str] = {}

    for idx, tok in enumerate(tokens):
        if is_instrumental(tok):
            pure_tokens.append(tok)
        else:
            removed_map[idx] = tok
    return pure_tokens, removed_map


def restore_non_instrumental(
    pure_tokens: List[str], removed_map: Dict[int, str]
) -> List[str]:
    """
    Rebuilds a full token list.

    - Places each removed_map[idx] at index `idx`.
    - Fills the remaining None slots (in ascending index order) with the
        items from pure_tokens, in order.
    """
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


def expand_repeats(tokens: List[str]) -> List[str]:
    """
    Scan through tokens. Whenever "measure:repeat_open" is found, collect everything
    up to the matching "measure:repeat_close:<count>" and repeat those inner tokens <count> times.
    Drop the measure markers themselves.
    """
    expanded = []
    i = 0
    n = len(tokens)

    while i < n:
        token = tokens[i]
        if token.startswith("measure:repeat_open"):
            j = i + 1
            while j < n and not tokens[j].startswith("measure:repeat_close"):
                j += 1
            if j >= n:
                expanded.append(token)
                i += 1
                continue

            # Extract repeat count from "measure:repeat_close:<count>"
            repeat_close_token = tokens[j]
            m = re.match(r"measure:repeat_close:(\d+)", repeat_close_token)
            if not m:
                expanded.append(token)
                i += 1
                continue

            count = int(m.group(1))
            inner_tokens = tokens[i + 1 : j]

            for _ in range(count):
                expanded.extend(inner_tokens)

            i = j + 1
        else:
            # Not a repeat marker, keep as-is
            expanded.append(token)
            i += 1

    return expanded


def process_raw_acoustic_solo_tokens(tokens: Union[str, List[str]]):
    if isinstance(tokens, str):
        try:
            with open(tokens, "r") as f:
                tokens = [t.strip() for t in f.readlines() if t.strip()]
        except FileNotFoundError:
            raise ValueError(
                "Please provide either encoded tokens or the path to the token file"
            )

    # Split tokens into header, body, and footer.
    header = []
    body = []
    footer = []
    in_body = False

    for token in tokens:
        if token == "start":
            in_body = True
            header.append(token)
        elif token == "end":
            in_body = False
            footer.append(token)
        elif in_body:
            body.append(token)
        else:
            # Tokens before "start" go to header; tokens after "end" go to footer.
            if not in_body:
                header.append(token)
            else:
                footer.append(token)

    expanded_body = expand_repeats(body)

    # Process body tokens by grouping consecutive 'clean' tokens,
    processed = []
    current_group = []

    prefixes = ("note", "bfs", "nfx", "wait")
    for token in expanded_body:
        # Group any 'clean' tracks
        if token.startswith("clean"):
            current_group.append(token)
            continue

        # Skip tokens that don't start with one of the desired prefixes
        if not token.startswith(prefixes):
            continue

        if current_group:
            merged = merge_tracks_and_prune(current_group)
            processed.extend(merged)
            current_group = []

        processed.append(token)

    if current_group:
        merged = merge_tracks_and_prune(current_group)
        processed.extend(merged)

    return processed


# def main():
#     examples_folder = "examples"
#
#     # Clean up any previously processed files
#     for fname in os.listdir(examples_folder):
#         if "processed" in fname:
#             path = os.path.join(examples_folder, fname)
#             if os.path.isfile(path):
#                 os.remove(path)
#
#     if not os.path.isdir(examples_folder):
#         print(f"The folder '{examples_folder}' does not exist.")
#         return
#
#     for filename in os.listdir(examples_folder):
#         if not filename.endswith(".txt"):
#             continue
#
#         filepath = os.path.join(examples_folder, filename)
#         if not os.path.isfile(filepath):
#             continue
#
#         print(f"\nProcessing file: {filename}")
#         try:
#             # Get a “fully processed” list:
#             processed_tokens: List[str] = process_raw_acoustic_solo_tokens(filepath)
#
#             # Strip out all non‐instrumental tokens
#             pure_tokens, removed_map = strip_non_instrumental(processed_tokens)
#             base_name, ext = os.path.splitext(filename)
#             predicted_pure = pure_tokens.copy()
#
#             # Re‐insert the non‐instrumental tokens in exactly the same spots:
#             reconstructed = restore_non_instrumental(predicted_pure, removed_map)
#
#             base_name, ext = os.path.splitext(filename)
#             processed_filename = f"{base_name}_processed{ext}"
#             with open(os.path.join(examples_folder, processed_filename), "w") as f_proc:
#                 f_proc.write("\n".join(processed_tokens))
#             print(f"  → Fully processed tokens saved to: {processed_filename}")
#
#             reconstructed_filename = f"{base_name}_reconstructed{ext}"
#             with open(os.path.join(examples_folder, reconstructed_filename), "w") as f_recon:
#                 f_recon.write("\n".join(reconstructed))
#             print(f"  → Reconstructed tokens saved to: {reconstructed_filename}")
#
#         except Exception as e:
#             print(f"An error occurred while processing {filename}: {e}")
#
#
# if __name__ == "__main__":
#     main()
