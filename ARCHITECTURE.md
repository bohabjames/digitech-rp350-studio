# Architecture

## Components

- **Desktop interface:** Windows device selection, editing, presets, and connection status.
- **MIDI transport:** USB MIDI port discovery and safe message transport.
- **RP350 protocol:** Device-specific framing, checksums, parsing, and parameter/preset serialization. Implement only from reviewed specifications.
- **Parameter database:** Effect names, IDs, positions, ranges, conversions, and evidence/confidence.
- **Preset layer:** Local import/export and validated device transfer.
- **Modulation engine:** Independent software LFOs and routing; practical destination count/rate depends on verified device behavior.

## Proposed stack

Python 3 is the current direction. PySide6, Mido/python-rtmidi, NumPy, and JSON are candidates, not locked decisions. Confirm Windows MIDI/SysEx support before implementation.

## Boundaries

Keep normal editor communication separate from firmware-update protocols. Do not implement flashing or send undocumented bootloader commands. Do not assume gdigi's RP350-external parameter maps or value encoding apply unchanged. Keep UI independent from transport and protocol.
