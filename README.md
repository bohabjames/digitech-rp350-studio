# DigiTech RP350 Studio

A Windows desktop editor and external modulation tool for the DigiTech RP350 guitar effects processor.

## Goals

- Build an editor and preset librarian for the RP350.
- Communicate over USB MIDI/SysEx using behavior verified against the RP350.
- Explore software LFOs and modulation routing after parameter control is understood.
- Keep protocol facts, hypotheses, and hardware verification separate.

## Status

The project is in the research and protocol-validation stage. See [PROJECT_STATUS.md](PROJECT_STATUS.md).

## Roles

- **ChatGPT — Research and technical lead:** investigates hardware/protocol behavior, writes specifications and plans, and reviews technical decisions.
- **Codex — Primary developer:** implements the Python application from approved specifications and maintains project status.
- **Claude — Secondary developer and reviewer:** reviews work and may implement assigned, isolated features.

## Safety boundary

Firmware flashing and unverified bootloader commands are out of scope. Do not turn protocol hypotheses into implementation facts without review and RP350 validation.