# Project status

**Stage:** Research and protocol validation  
**Application implementation:** Not started  
**Physical RP350 verification:** Pending

## Confirmed

- Target: DigiTech RP350 connected to Windows over USB.
- The RP350 manual documents USB for X-Edit communication and audio streaming.
- Supplied SysEx capture: 3,174 bytes, 151 framed messages, common header `F0 00 00 10 00 5E 03`.
- Command counts: 141 `0x41`, five `0x3B`, five `0x70`.
- All 151 frames pass the XOR checksum check used by gdigi. This does not establish message meaning or direction.

## Hypotheses and unknowns

- Repeated tentative fields `0x2009 / 0x1A` appear with changing trailing bytes; identity, value encoding, and cause are unknown.
- gdigi uses `0x41` for parameter-value communication, but does not list RP350 support.
- Meanings of `0x3B` and `0x70`, capture direction, and timing remain unverified.

## Next steps

1. Compare capture framing and serialization with gdigi; document differences.
2. Identify `0x3B` and `0x70` from source and controlled captures.
3. Correlate a capture with one known action and record the pedal state.
4. Review an RP350-specific protocol specification before live writes.

## Developer tooling

- Lint (Ruff) and test (pytest) baseline with a Windows GitHub Actions workflow; see [docs/development/quality_checks.md](docs/development/quality_checks.md). It locks in no application runtime dependencies.
- Checked locally on Linux only; the Windows CI matrix is unproven until the workflow runs on GitHub. No hardware involved.

## Hardware checks

| Check | Status |
|---|---|
| Confirm Windows MIDI ports and names | Pending |
| Correlate one changing value to known pedal/UI action | Pending |
| Validate documented parameter read/write | Pending |
