# acoustic-solo-dadaGP

A modification of [DadaGP](https://github.com/dada-bots/dadaGP/tree/main) customized for gp files of acoustic solo. It supports gp files with alternative string tuning and/or more than 2 acoustic tracks.

---

## Table of Contents

1. [Background & Attribution](#background--attribution)  
2. [What's Changed](#whats-changed)  
3. [Features](#features)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Command Line Interface](#command-line-interface)
7. [API Reference](#api-reference)
8. [Contributing](#contributing)  
9. [License](#license)  

---

## Background & Attribution

This repo is a **fork** of [dadaGP](https://github.com/dada-bots/dadaGP) by `dada-bots`.

---

## What's Changed

- **Enhanced Acoustic Support**: Optimized for acoustic solo guitar files
- **Alternative Tunings**: Full support for various guitar tunings including Celtic tuning
- **Multi-track Processing**: Support for up to 3 clean/acoustic guitar tracks
- **Command Line Interface**: Easy-to-use CLI for file processing
- **Improved Token Processing**: Better handling of acoustic-specific musical elements

---

## Features

- **Guitar Pro File Processing**: Convert `.gp3`, `.gp4`, `.gp5`, and `.gpx` files to tokenized format
- **Alternative String Tunings**: Support for various guitar tunings (standard, drop D, Celtic, etc.)
- **Multi-track Support**: Handle multiple acoustic guitar tracks (up to 3)
- **Token-based Processing**: Advanced token system for representing musical elements
- **Track Merging**: Merge multiple tracks into a single representation
- **File Validation**: Validate Guitar Pro files for compatibility
- **Comprehensive CLI**: Full command-line interface for all operations

---

## Installation

### From PyPI (Recommended)

```bash
pip install acoustic-solo-dadaGP
```

### From Source

```bash
git clone https://github.com/austinliu05/acoustic-solo-dadaGP.git
cd acoustic-solo-dadaGP
pip install -e .
```

---

## Usage

### Command Line Interface

The package provides a comprehensive CLI with the following commands:

#### Encode Guitar Pro to Tokens

```bash
asdadagp encode input.gp5 output.txt --artist "Artist Name"
```

#### Decode Tokens to Guitar Pro

```bash
asdadagp decode input.txt output.gp5
```

#### Process Tokens

```bash
# Process with track merging
asdadagp process input.txt --merge-tracks --output processed.txt

# Process as acoustic solo
asdadagp process input.txt --acoustic-solo --output processed.txt

# Keep tracks separate
asdadagp process input.txt --no-merge-tracks --output processed.txt
```

#### Merge Tracks

```bash
# Merge multiple tracks into a single representation
asdadagp merge-tracks input.txt output.txt
```

**What it does:**
- Removes `cleanX:` prefixes from tokens (e.g., `clean0:note:s6:f0:D3` → `note:s6:f0:D3`)
- Combines multiple guitar tracks into a unified tab
- Preserves all musical content (notes, effects, timing)

#### Split Measures

```bash
# Split tokens into measures with structured output
asdadagp split-measures input.txt output.json
```

**What it does:**
- Splits tokens by `new_measure` boundaries
- Outputs structured JSON with:
  - `tokens`: Indexed mapping of all tokens
  - `measure_order`: Lists of token indices for each measure
  - `tuning`: Guitar string tuning information

#### Get File Information

```bash
# Guitar Pro file info
asdadagp info input.gp5

# Token file info
asdadagp info input.txt
```



### Python API

```python
from asdadagp import asdadagp_decode, asdadagp_encode, process_tokens

# Encode a Guitar Pro file
asdadagp_encode("input.gp5", "output.txt", "Artist Name")

# Decode tokens back to Guitar Pro
asdadagp_decode("input.txt", "output.gp5")

# Process tokens
processed = process_tokens(tokens, merge_tracks=True)
```

---

## Command Line Interface

### Available Commands

- **`encode`**: Convert Guitar Pro files to token format
- **`decode`**: Convert tokens back to Guitar Pro files
- **`process`**: Process tokens with various options
- **`merge-tracks`**: Merge multiple tracks in a token file
- **`split-measures`**: Split tokens into measures with structured output
- **`info`**: Display information about files

### Examples

```bash
# Basic encoding
asdadagp encode song.gp5 tokens.txt --artist "John Doe"

# Decoding with custom output
asdadagp decode tokens.txt output.gp5

# Process tokens and save to file
asdadagp process tokens.txt --merge-tracks --output processed.txt

# Merge multiple tracks in a token file
asdadagp merge-tracks input.txt output.txt

# Split tokens into measures with structured output
asdadagp split-measures input.txt output.json

# Get detailed file information
asdadagp info song.gp5
```

---

## API Reference

### Main Functions

#### `asdadagp_encode(input_file, output_file, artist_token)`
Convert a Guitar Pro file to token format.

#### `asdadagp_decode(input_file, output_file)`
Convert tokens back to a Guitar Pro file.

#### `process_tokens(tokens, merge_tracks=True)`
Process tokens with optional track merging.

#### `process_raw_acoustic_solo_tokens(tokens)`
Process tokens specifically for acoustic solo guitar.

#### `split_tokens_to_measures(tokens)`
Split a list of tokens into measures based on "new_measure" tokens.

#### `tokens_to_measures(tokens)`
Convert tokens to structured TokenMeasure objects with repeat information.



### Utility Functions

#### `get_tuning_type(tuning)`
Get the type of guitar tuning.

#### `get_fret(note, tuning)`
Get fret position for a note in a given tuning.

#### `convert_spn_to_common(note)`
Convert Scientific Pitch Notation to common notation.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This fork is released under the **MIT License**. See [LICENSE](LICENSE).

The original project `dadaGP` by `dada-bots` is also under MIT; see their [LICENSE](https://github.com/dada-bots/dadaGP?tab=MIT-1-ov-file).