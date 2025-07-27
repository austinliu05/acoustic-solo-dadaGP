"""
acoustic-solo-dadaGP - A modification of DadaGP customized for acoustic solo guitar files.

This package provides tools for processing Guitar Pro files, converting them to tokens,
and back to Guitar Pro format, specifically designed for acoustic solo guitar music.
"""

__version__ = "0.1.0"
__author__ = "Austin Liu"
__email__ = "austin_f_liu@brown.edu"

# Main functions
from .encoder import asdadagp_encode, guitarpro2tokens
from .decoder import asdadagp_decode, tokens2guitarpro
from .processor import process_tokens, process_raw_acoustic_solo_tokens

# Utility functions
from .utils import get_tuning_type, get_fret, convert_spn_to_common

# Constants
from .const import instrument_groups, supported_times, wait_token_list2

__all__ = [
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
