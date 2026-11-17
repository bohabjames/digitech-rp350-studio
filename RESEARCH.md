# Research notes

These notes are preliminary, not an implementation specification. ChatGPT owns research and technical direction. Preserve fact/hypothesis labels.

## Sources

- RP350 manual: https://digitech.com/wp-content/uploads/2022/09/RP350_Manual18-0436V-A_original.pdf
- gdigi: https://github.com/desowin/gdigi
- RP Series Firmware Updater: https://github.com/codeon314/Digitech-RP-Series-Firmware-Updater

## USB and gdigi

The RP350 manual documents USB for X-Edit communication and audio streaming. The user reports Windows exposes MIDI input/output ports named **DigiTech RP350 MIDI**.

gdigi's README lists RP150, RP155, RP250, RP255, RP355, RP500, RP1000, GNX3000, and GNX4K; it does not list RP350. Its source is useful for DigiTech framing, packing, XOR checksum, and parameter serialization, but model-specific application remains unverified.

## Captures

### Initial startup

`rp350 x-edit start up.syx` — 2,617 bytes; 10 frames; all pass the XOR checksum calculation. Command counts: one each `0x02`, `0x09`, `0x11`, `0x2B`, `0x2C`, `0x2D`, `0x3B`, `0x7E`; two `0x22`. Includes long messages with readable effect/library labels and one long structured record. Exact command meanings are not yet validated for RP350.

### Analog Delay enable and Level +1

`rp 350 x-edit analog delay - level up one.syx` — 86 bytes, six frames: four `0x41` messages bracketed by two `0x7E` messages. All pass XOR checks. User action: enabled Analog Delay and increased its Level one step.

### Subsequent capture, two more upward steps

`rp 350 x-edit up two (from analog delay - level up one).syx` — 148 bytes, ten frames. It contains two repeated four-message groups, each bracketed by `0x7E` status messages. Comparing corresponding `0x41` messages:
- Three parameter records appear unchanged across the captures.
- One record has visible payload bytes `22 06 1A 66`, then `22 06 1A 68`, then `22 06 1A 6A` (checksum excluded).
- The user reports this capture represents two further Level steps from the prior capture. The changing record therefore tracks the Level action in these captures.

**Interpretation, provisional:** Under gdigi's message layout, these bytes appear consistent with parameter ID `0x2206`, position `0x1A`, value bytes progressing `0x66 -> 0x68 -> 0x6A`. gdigi defines ID 0x2206 as an effects-library level maximum, but gdigi does not list RP350. Treat the ID name and numeric scaling as a hypothesis pending RP350-specific confirmation. This is the first controlled mapping candidate; do not yet encode it as a confirmed general Analog Delay Level mapping.

### Original long capture

`midi DIGI TECH 350 1st test.syx` — 3,174 bytes; 151 frames; common header `F0 00 00 10 00 5E 03`; 141 `0x41`, five `0x3B`, five `0x70`; all pass gdigi's XOR checksum calculation. User reports replaying this file changes a setting on the pedal, but the exact setting/message is not identified.

## Firmware updater boundary

Updater research may inform shared transport/discovery concepts. Its firmware-update and bootloader operations are out of scope; do not port or invoke firmware-writing behavior.

## Evidence rule

Record the source, model applicability, confidence, and required hardware check for every protocol claim. Do not promote hypotheses to facts without review.
