from logging import getLogger

from ._version import __version__
from .const import PKG_NAME

_LOGGER = getLogger(PKG_NAME)

# Constants
from .const import instrument_groups, supported_times, wait_token_list2
from .decoder import asdadagp_decode, tokens2guitarpro

# Main functions
from .encoder import asdadagp_encode, guitarpro2tokens
from .processor import process_raw_acoustic_solo_tokens, process_tokens

# Utility functions
from .utils import convert_spn_to_common, get_fret, get_tuning_type

__all__ = [
    # Version and logging
    "__version__",
    "_LOGGER",
    "PKG_NAME",
    # Main functions
    "asdadagp_encode",
    "guitarpro2tokens",
    "asdadagp_decode",
    "tokens2guitarpro",
    "process_tokens",
    "process_raw_acoustic_solo_tokens",
    # Utility functions
    "get_tuning_type",
    "get_fret",
    "convert_spn_to_common",
    # Constants
    "instrument_groups",
    "supported_times",
    "wait_token_list2",
]
