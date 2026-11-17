# Project status

**Stage:** Research and protocol validation  
**Application implementation:** Not started  
**Physical RP350 verification:** Partial; see observations below.

## Confirmed

- Target: DigiTech RP350 connected to Windows over USB.
- User reports Windows exposes MIDI input/output ports named **DigiTech RP350 MIDI**.
- User reports replaying the supplied SysEx capture with a Windows MIDI SysEx utility changes a setting on the pedal. This confirms the capture can cause a device change when replayed; exact message-to-parameter mapping is not yet established.
- The RP350 manual documents USB for X-Edit communication and audio streaming.
- Supplied SysEx capture: 3,174 bytes, 151 framed messages, common header `F0 00 00 10 00 5E 03`.
- Command counts: 141 `0x41`, five `0x3B`, five `0x70`.
- All 151 frames pass the XOR checksum check used by gdigi. This does not establish message meaning or direction.

## Hypotheses and unknowns

- Repeated tentative fields `0x2009 / 0x1A` appear with changing trailing bytes; identity, value encoding, and cause are unknown.
- gdigi uses `0x41` for parameter-value communication, but does not list RP350 support.
- Meanings of `0x3B` and `0x70`, capture direction, and timing remain unverified.
- The setting changed by replay has not yet been identified by name or matched to a specific message.

## Next steps

1. Record pedal state and identify the setting changed by replay.
2. Capture a controlled one-parameter change and compare it with the supplied file.
3. Identify `0x3B` and `0x70` from source and controlled captures.
4. Review an RP350-specific protocol specification before implementing live writes.

## Developer tooling

- Lint (Ruff) and test (pytest) baseline with a Windows GitHub Actions workflow; see [docs/development/quality_checks.md](docs/development/quality_checks.md). It locks in no application runtime dependencies.
- Checked locally on Linux, and the workflow (`windows-latest`, Python 3.11 and 3.13) passed on its pull request. Not yet run on a developer's own Windows machine. No hardware involved.
- The read-only port-listing aid is [docs/development/midi_diagnostic.md](docs/development/midi_diagnostic.md) (`tools/midi_diagnostic.py)); it has been superseded for basic device visibility by the user's Windows observation.

## Hardware checks

| Check | Status |
|---|---|
| Windows exposes DigiTech RP350 MIDI input/output ports | Confirmed by user |
| Replaying supplied SysEx changes a pedal setting | Confirmed by user; exact setting/message mapping unknown |
| Correlate one changing value to a named setting | Pending |
| Validate a documented parameter read/write | Pending |
