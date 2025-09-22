# MagicstompFrenzy Reference Files

This directory contains key files from the [MagicstompFrenzy](https://github.com/dulnikovsky/magicstompfrenzy) repository for debugging and reference purposes.

## Credits

**Original Repository:** [dulnikovsky/magicstompfrenzy](https://github.com/dulnikovsky/magicstompfrenzy)
**License:** GPL-3.0
**Author:** dulnikovsky

## Files Included

### Core Implementation Files
- `mainwindow.cpp` - Main MIDI communication and SysEx message handling
- `magicstomp.h` - Patch structure definitions and parameter offsets
- `knobparameters.h` - Complete mapping of effect parameters to offsets
- `preferencesdialog.cpp` - MIDI configuration and channel settings

### Purpose
These files are used as reference for:
1. Understanding SysEx message format for real-time parameter control
2. Debugging MIDI communication issues
3. Mapping effect parameters to their memory offsets
4. Implementing checksum calculations

## Usage in Our Project

Our `realtime_magicstomp.py` implementation is based on the SysEx format and checksum calculation found in these files, specifically:

- **SysEx Header:** `F0 43 7D 40 55 42` (from mainwindow.cpp)
- **Checksum Calculation:** Additive with negation and 7-bit mask (from mainwindow.cpp)
- **Parameter Offsets:** Complete mapping from knobparameters.h
- **MIDI Channel:** OMNI (0) default from preferencesdialog.cpp

## License Compliance

These files are included for reference and debugging purposes only. The original GPL-3.0 license applies to the MagicstompFrenzy repository.


