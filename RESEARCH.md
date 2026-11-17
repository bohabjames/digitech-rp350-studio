# Research notes

These notes are preliminary, not an implementation specification. ChatGPT owns research and technical direction. Preserve fact/hypothesis labels.

## Sources

- RP350 manual: https://digitech.com/wp-content/uploads/2022/09/RP350_Manual18-0436V-A_original.pdf
- gdigi: https://github.com/desowin/gdigi
- RP Series Firmware Updater: https://github.com/codeon314/Digitech-RP-Series-Firmware-Updater

## USB and gdigi

The RP350 manual documents USB for X-Edit communication and audio streaming. The user reports Windows exposes MIDI input/output ports named **DigiTech RP350 MIDI**.

gdigi's README lists RP150, RP155, RP250, RP255, RP355, RP500, RP1000, GNX3000, and GNX4K; it does not list RP350. Its source is useful for DigiTech framing, packing, XOR checksum, and parameter serialization, but model-specific application remains unverified.

## Supplied capture

`midi DIGI TECH 350 1st test.syx` — 3,174 bytes; SHA-256 `BAAED1E3D7336B7B48FC996E8256F335873741027C330A8ADD9CED9D4F9351E8`.

Observed: 151 frames, common header `F0 00 00 10 00 5E 03`; 141 `0x41`, five `0x3B`, five `0x70`; all pass gdigi's XOR checksum calculation.

**Hardware observation from user:** Replaying this file through a Windows MIDI SysEx utility changes a setting on the RP350. This establishes that replaying the capture can affect the pedal, but does not identify the setting or isolate which message causes the change.

Hypothesis: Many `0x41` frames share tentative fields `0x2009 / 0x1A` with changing bytes. Device-specific meaning and value encoding are not established. A flattened .syx has no timestamps or direction metadata.

## Firmware updater boundary

Updater research may inform shared transport/discovery concepts. Its firmware-update and bootloader operations are out of scope; do not port or invoke firmware-writing behavior.

## Evidence rule

Record the source, model applicability, confidence, and required hardware check for every protocol claim. Do not promote hypotheses to facts without review.
