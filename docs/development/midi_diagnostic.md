# Windows MIDI device diagnostic

`tools/midi_diagnostic.py` lists the MIDI input and output port names that Windows exposes through the current backend, so we can confirm what the RP350 appears as. It is an isolated developer tool, not part of the application.

## Safety

The tool is **read-only**. It only calls `get_input_names()` and `get_output_names()`. It never opens an input or output port, sends MIDI or SysEx, queries the pedal, or changes device state. It contains no firmware-updater or bootloader functionality and makes no assumptions about the RP350 protocol. Tests enforce this with a fake backend that fails if anything other than enumeration is touched.

Mido with the python-rtmidi backend is the current candidate stack for this prototype. Using it here does not approve it for the main application.

## Install and run (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install mido python-rtmidi

python tools/midi_diagnostic.py
python tools/midi_diagnostic.py --json
```

Mido and python-rtmidi are installed by hand into your virtual environment and are not listed in any requirements file, because the application's runtime dependencies are undecided. With the RP350 connected by USB and powered on, run the tool, then run it again with the pedal disconnected and compare the lists.

## Output

The report shows Python, platform, mido and python-rtmidi versions, the backend name, and the numbered input and output port names, followed by notes that explain anything missing:

- mido not installed: the note gives the install command.
- backend missing or failing to load: the error is shown per direction, with a hint.
- no ports: the note suggests checking power, USB connection and whether another application is using the device.

The exit code is `0` when enumeration worked (even with zero ports) and `2` when mido or the backend is missing or enumeration failed. `--json` prints the same data for sharing; it includes your Python and Windows version strings and the port names.

## Tests

```powershell
python -m pip install pytest
python -m pytest tests/test_midi_diagnostic.py
```

The tests use mocked port enumeration and need no MIDI hardware, no backend, and no mido installation.

## Verification status

| What | Status |
|---|---|
| Logic, formatting, error handling, read-only behavior | Tested with mocks on Linux |
| Behavior with the real mido and python-rtmidi packages | Not tested |
| Windows run, including real port names | Not tested |
| Connected RP350 | Not tested; the hardware check "Confirm Windows MIDI ports and names" stays pending |
