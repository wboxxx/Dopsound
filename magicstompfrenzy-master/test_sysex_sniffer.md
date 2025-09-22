# SysEx Sniffer Test Guide

## Overview
The enhanced SysEx sniffer has been successfully integrated into MagicstompFrenzy. It will log every SysEx message sent to the Magicstomp device with parameter names and detailed information:

```
[2025-01-21 22:45:03] SYSEX OUT len=9  | PARAM: Delay Mix (offset=26, len=1)  F0 43 7D 40 55 42 20 00 1A F7
```

## How to Test

### 1. Build and Run MagicstompFrenzy
```bash
cd magicstompfrenzy-master
qmake
make
./magicstompfrenzy
```

### 2. Connect to Magicstomp Device
- Open Preferences and configure MIDI input/output ports
- Connect to your Magicstomp device

### 3. Test Parameter Changes
1. **Select a patch** from the patch list
2. **Adjust any parameter** in the effect editor (e.g., Delay Mix, Reverb Level, etc.)
3. **Watch the console output** - you should see SysEx messages logged to stderr

### 4. Expected Log Output
When you change a parameter (e.g., Delay Mix from 0 to 25), you should see output like:

```
[2025-01-21 22:45:03] SYSEX OUT len=9  | PARAM: Delay Mix (offset=26, len=1)  F0 43 7D 40 55 42 20 00 1A F7
[2025-01-21 22:45:04] SYSEX OUT len=9  | PARAM: Delay Mix (offset=26, len=1)  F0 43 7D 40 55 42 20 00 32 F7
[2025-01-21 22:45:05] SYSEX OUT len=9  | PARAM: Delay Mix (offset=26, len=1)  F0 43 7D 40 55 42 20 00 4B F7
[2025-01-21 22:45:06] SYSEX OUT len=9  | PARAM: Delay Mix (offset=26, len=1)  F0 43 7D 40 55 42 20 00 64 F7
```

### 5. Test Different Parameter Types
- **Effect parameters**: Change delay time, reverb level, etc.
- **Patch selection**: Double-click different patches
- **Bulk operations**: Send all patches, request all patches

## SysEx Message Format
The logged messages follow the Magicstomp SysEx format:
- `F0` - SysEx start
- `43` - Yamaha manufacturer ID
- `7D` - Magicstomp device ID
- `40` - Parameter change command
- `55 42` - Magicstomp identifier
- `20` - Data type (0x20 = parameter data)
- `00` - Parameter offset (0x00 = common data, 0x01 = effect data)
- `XX` - Parameter value(s)
- `F7` - SysEx end

## Features
- ✅ **Timestamp**: Each message includes precise timestamp
- ✅ **Length**: Shows exact byte count
- ✅ **Parameter Name**: Shows the actual parameter name (e.g., "Delay Mix", "Reverb Level")
- ✅ **Offset & Length**: Shows parameter offset and data length
- ✅ **Hex dump**: All bytes displayed in uppercase hex
- ✅ **Minimal overhead**: Logging doesn't affect real-time performance
- ✅ **stderr output**: Logs go to stderr as requested
- ✅ **No message modification**: Original SysEx data is unchanged
- ✅ **Parameter matching**: Easy to match parameter changes with SysEx messages

## Troubleshooting
- If no output appears, check that MIDI output is properly configured
- Ensure the Magicstomp device is connected and recognized
- Verify that parameter changes are actually being sent (check MIDI activity)
- Look for any error messages in the console output
