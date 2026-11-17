"""Tests for tools/midi_diagnostic.py.

These use mocked MIDI enumeration only. No MIDI hardware, backend or mido
installation is required.
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

TOOL_PATH = Path(__file__).resolve().parents[1] / "tools" / "midi_diagnostic.py"


def _load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("midi_diagnostic", TOOL_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # Dataclasses look the module up in sys.modules while it executes.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


diag = _load_tool()


class StrictFakeMido:
    """Fake mido that permits enumeration and fails on anything else.

    Opening a port, sending a message or touching any other attribute raises,
    which proves the diagnostic stays read-only.
    """

    _ALLOWED = {"get_input_names", "get_output_names", "backend"}

    def __init__(self, inputs=(), outputs=(), input_error=None, output_error=None):
        self._inputs = list(inputs)
        self._outputs = list(outputs)
        self._input_error = input_error
        self._output_error = output_error
        self.backend = SimpleNamespace(name="mido.backends.rtmidi")
        self.calls: list[str] = []

    def get_input_names(self):
        self.calls.append("get_input_names")
        if self._input_error:
            raise self._input_error
        return self._inputs

    def get_output_names(self):
        self.calls.append("get_output_names")
        if self._output_error:
            raise self._output_error
        return self._outputs

    def __getattr__(self, name):
        # Only called for attributes that do not exist normally.
        raise AssertionError(f"diagnostic touched forbidden mido attribute: {name}")


@pytest.fixture
def use_mido(monkeypatch):
    def install(fake):
        monkeypatch.setattr(diag, "load_mido", lambda: fake)
        return fake

    return install


@pytest.fixture(autouse=True)
def fixed_versions(monkeypatch):
    versions = {"mido": "1.3.3", "python-rtmidi": "1.5.8"}
    monkeypatch.setattr(diag, "package_version", versions.get)


def test_lists_input_and_output_ports(use_mido):
    use_mido(StrictFakeMido(inputs=["In A", "In B"], outputs=["Out A"]))

    report = diag.collect_report()

    assert report.ok
    assert report.inputs.names == ["In A", "In B"]
    assert report.outputs.names == ["Out A"]
    assert report.backend_name == "mido.backends.rtmidi"
    assert report.mido_version == "1.3.3"
    assert report.python_rtmidi_version == "1.5.8"


def test_only_enumerates_and_never_opens_ports(use_mido):
    fake = use_mido(StrictFakeMido(inputs=["In"], outputs=["Out"]))

    diag.collect_report()

    assert sorted(fake.calls) == ["get_input_names", "get_output_names"]


def test_duplicate_port_names_are_preserved_in_order(use_mido):
    use_mido(StrictFakeMido(inputs=["Same", "Same"], outputs=[]))

    report = diag.collect_report()

    assert report.inputs.names == ["Same", "Same"]


def test_mido_not_installed_explains_how_to_install(monkeypatch):
    def missing():
        raise ModuleNotFoundError("No module named 'mido'")

    monkeypatch.setattr(diag, "load_mido", missing)

    report = diag.collect_report()

    assert not report.ok
    assert not report.mido_available
    assert any("pip install mido python-rtmidi" in note for note in report.notes)
    assert "not listed because mido is unavailable" in diag.format_text(report)


def test_backend_load_failure_is_reported_for_both_directions(use_mido):
    error = ImportError("No module named 'rtmidi'")
    use_mido(StrictFakeMido(input_error=error, output_error=error))

    report = diag.collect_report()

    assert not report.ok
    assert report.inputs.error == "ImportError: No module named 'rtmidi'"
    assert report.outputs.error == report.inputs.error
    assert any("backend may not be installed" in note for note in report.notes)


def test_one_direction_failing_keeps_the_other(use_mido):
    use_mido(StrictFakeMido(outputs=["Out A"], input_error=RuntimeError("boom")))

    report = diag.collect_report()

    assert not report.ok
    assert report.inputs.error == "RuntimeError: boom"
    assert report.outputs.names == ["Out A"]
    text = diag.format_text(report)
    assert "Input ports: unavailable (RuntimeError: boom)" in text
    assert "[0] Out A" in text


def test_no_ports_gives_an_explanation(use_mido):
    use_mido(StrictFakeMido())

    report = diag.collect_report()

    assert report.ok
    assert any("reported no MIDI input or output ports" in note for note in report.notes)
    assert "(none)" in diag.format_text(report)


def test_inputs_without_outputs_gets_a_specific_note(use_mido):
    use_mido(StrictFakeMido(inputs=["In A"]))

    report = diag.collect_report()

    assert any("No MIDI output ports were reported" in note for note in report.notes)


def test_non_windows_platform_is_noted(use_mido, monkeypatch):
    use_mido(StrictFakeMido(inputs=["In"], outputs=["Out"]))
    monkeypatch.setattr(diag.sys, "platform", "linux")

    report = diag.collect_report()

    assert any("targets Windows" in note for note in report.notes)


def test_backend_name_unavailable_is_tolerated(use_mido):
    fake = use_mido(StrictFakeMido(inputs=["In"], outputs=["Out"]))
    fake.backend = None

    report = diag.collect_report()

    assert report.ok
    assert report.backend_name is None
    assert "Backend:       unknown" in diag.format_text(report)


def test_text_report_lists_indexed_ports(use_mido):
    use_mido(StrictFakeMido(inputs=["In A"], outputs=["Out A", "Out B"]))

    text = diag.format_text(diag.collect_report())

    assert "Input ports (1):" in text
    assert "  [0] In A" in text
    assert "Output ports (2):" in text
    assert "  [1] Out B" in text
    assert "read-only" in text


def test_json_report_round_trips(use_mido):
    use_mido(StrictFakeMido(inputs=["In A"], outputs=["Out A"]))

    data = json.loads(diag.format_json(diag.collect_report()))

    assert data["ok"] is True
    assert data["inputs"]["names"] == ["In A"]
    assert data["outputs"]["names"] == ["Out A"]
    assert data["backend_name"] == "mido.backends.rtmidi"


def test_package_version_returns_none_when_not_installed(monkeypatch):
    real = _load_tool()

    def not_found(_name):
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(real.importlib.metadata, "version", not_found)

    assert real.package_version("definitely-not-installed") is None


def test_main_exit_codes(use_mido, capsys):
    use_mido(StrictFakeMido(inputs=["In"], outputs=["Out"]))
    assert diag.main([]) == 0
    assert "Input ports (1):" in capsys.readouterr().out

    use_mido(StrictFakeMido(input_error=RuntimeError("boom")))
    assert diag.main(["--json"]) == 2
    assert json.loads(capsys.readouterr().out)["ok"] is False


def test_main_exit_code_when_mido_missing(monkeypatch, capsys):
    def missing():
        raise ImportError("nope")

    monkeypatch.setattr(diag, "load_mido", missing)

    assert diag.main([]) == 2
    assert "pip install mido python-rtmidi" in capsys.readouterr().out
