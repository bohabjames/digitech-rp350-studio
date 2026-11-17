# Tasks

## Research and specification

- [ ] Analyze gdigi framing, packing, parameter serialization, and preset serialization.
- [ ] Review updater documentation while keeping bootloader operations out of scope.
- [ ] Build a reproducible offline analyzer for the supplied capture.
- [ ] Identify `0x3B` and `0x70` using source comparison and controlled captures.
- [ ] Confirm Windows MIDI input/output port names.
- [ ] Write/review RP350-specific protocol specification before live writes.

## Implementation — after validated specification

- [ ] Confirm Python dependencies and packaging approach.
- [ ] Implement offline SysEx parsing and sample capture coverage.
- [ ] Add MIDI port discovery and read-only monitoring.
- [ ] Plan reversible single-parameter hardware validation.
- [ ] Build editor and preset librarian.
- [ ] Add external LFOs and modulation routing after parameter control is validated.
- [ ] Package and document Windows application.
