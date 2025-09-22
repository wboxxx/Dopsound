# MagicstompFrenzy Reference - Credits and Usage

## Original Project

**MagicstompFrenzy** - Editor for Yamaha Magicstomp Guitar Effect Processor
- **Repository**: [https://github.com/dulnikovsky/magicstompfrenzy](https://github.com/dulnikovsky/magicstompfrenzy)
- **Author**: dulnikovsky (Robert Vetter)
- **License**: GPL-3.0
- **Description**: A comprehensive editor for the Yamaha Magicstomp multieffect processor

## Files Used in Our Implementation

### Core Implementation Files
1. **`mainwindow.cpp`** - Main MIDI communication and SysEx message handling
   - `parameterChanged()` function for real-time parameter modification
   - `calcChecksum()` function for SysEx message validation
   - SysEx header definitions and message construction logic

2. **`magicstomp.h`** - Patch structure definitions and parameter offsets
   - `MagistompPatchDesc` enum with patch layout constants
   - `EffectTypeId` enum with all effect type identifiers
   - Control potentiometer offset definitions (Control1=2, Control2=4, Control3=6)

3. **`knobparameters.h`** - Complete mapping of effect parameters to offsets
   - Comprehensive parameter mappings for all Magicstomp effects
   - Human-readable parameter names mapped to memory offsets
   - Key mappings used: AmpMultiFlange, MonoDelay, Reverb, Compressor, etc.

4. **`preferencesdialog.cpp`** - MIDI configuration and channel settings
   - MIDI channel configuration (default: OMNI/0)
   - MIDI port selection logic
   - Control Change parameter mapping

## Key Information Extracted

### SysEx Message Format
```
Header: F0 43 7D 40 55 42 20 [section] [offset] [data...] [checksum] F7
- F0: SysEx start
- 43: Yamaha manufacturer ID
- 7D: Device ID
- 40: Parameter send command
- 55 42: Magicstomp ID
- 20: Parameter modification flag
- [section]: 0x00 (common) or 0x01 (effect)
- [offset]: Parameter offset within section
- [data]: Parameter value(s)
- [checksum]: Calculated checksum
- F7: SysEx end
```

### Checksum Calculation
```cpp
char calcChecksum(const char *data, int dataLength)
{
    char checkSum = 0;
    for (int i = 0; i < dataLength; ++i)
    {
        checkSum += *data++;
    }
    return ((-checkSum) & 0x7f);
}
```

### MIDI Configuration
- **Default Channel**: 0 (OMNI - listens to all channels)
- **Port Detection**: Automatic detection of Magicstomp USB MIDI ports
- **Real-time Control**: Immediate parameter changes without patch reload

### Parameter Offsets (Key Examples)
- **Control1**: Offset 2 (Physical potentiometer 1 assignment)
- **Control2**: Offset 4 (Physical potentiometer 2 assignment)
- **Control3**: Offset 6 (Physical potentiometer 3 assignment)
- **Delay Level**: Offset 67 (DLVL)
- **High Pass Filter**: Offset 71 (DHPF)
- **Flanger Depth**: Offset 53
- **Compressor Threshold**: Offset 0

## Implementation in Our Project

Our `realtime_magicstomp.py` implementation is directly based on the MagicstompFrenzy code:

1. **SysEx Format**: Exact header and message structure
2. **Checksum Algorithm**: Identical additive checksum with negation
3. **Parameter Mapping**: Direct use of offset mappings from knobparameters.h
4. **MIDI Channel**: OMNI (0) default configuration
5. **Section Logic**: Automatic common vs. effect section determination

## License Compliance

- **Original License**: GPL-3.0
- **Our Usage**: Reference and implementation based on public source code
- **Attribution**: Full credit given to original author and repository
- **No Direct Copying**: Our implementation is a Python adaptation, not a direct copy

## Acknowledgments

Special thanks to **dulnikovsky (Robert Vetter)** for creating and maintaining MagicstompFrenzy, which provided the essential technical documentation and implementation details needed for our real-time parameter control system.

Without this excellent reference implementation, our real-time Magicstomp control system would not have been possible.


