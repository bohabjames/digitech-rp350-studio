"""Read-only MIDI port diagnostic.

Lists the MIDI input and output port names that the current MIDI backend
reports, plus relevant runtime and package versions. It exists to help
confirm which ports Windows exposes for the RP350.

Safety: this tool only enumerates ports. It never opens an input or output
port, transmits MIDI or SysEx, queries a device, or changes device state.
The only mido calls it makes are ``get_input_names()`` and
``get_output_names()``.

Mido with the python-rtmidi backend is the current candidate stack for this
prototype. It is not an approved choice for the main application.

Usage:
    python tools/midi_diagnostic.py [--json]

Exit codes:
    0  enumeration worked (zero ports is still a successful enumeration)
    2  the backend is missing or enumeration failed
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import platform
import sys
from dataclasses import asdict, dataclass, field
from types import ModuleType

INSTALL_HINT = "py -m pip install mido python-rtmidi"


@dataclass
class PortReport:
    """Result of enumerating one direction of MIDI ports."""

    names: list[str] = field(default_factory=list)
    error: str | None = None


@dataclass
class DiagnosticReport:
    """Everything the diagnostic found, in a JSON-friendly shape."""

    python_version: str = ""
    platform: str = ""
    mido_version: str | None = None
    python_rtmidi_version: str | None = None
    backend_name: str | None = None
    mido_available: bool = False
    inputs: PortReport = field(default_factory=PortReport)
    outputs: PortReport = field(default_factory=PortReport)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when mido was importable and both enumerations succeeded."""
        return self.mido_available and self.inputs.error is None and self.outputs.error is None


def load_mido() -> ModuleType:
    """Import mido. Split out so tests can replace it."""
    return importlib.import_module("mido")


def package_version(distribution: str) -> str | None:
    """Return an installed distribution's version without importing it."""
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return None


def describe_error(exc: BaseException) -> str:
    """One-line description of an exception."""
    message = str(exc).strip()
    return f"{type(exc).__name__}: {message}" if message else type(exc).__name__


def _backend_name(mido: ModuleType) -> str | None:
    try:
        name = mido.backend.name
    except Exception:  # noqa: BLE001 - a diagnostic must never crash on introspection
        return None
    return str(name) if name else None


def _enumerate(getter_name: str, mido: ModuleType) -> PortReport:
    try:
        names = list(getattr(mido, getter_name)())
    except Exception as exc:  # noqa: BLE001 - report any backend failure to the user
        return PortReport(error=describe_error(exc))
    return PortReport(names=[str(name) for name in names])


def collect_report() -> DiagnosticReport:
    """Gather the report. Enumerates ports only; never opens one."""
    report = DiagnosticReport(
        python_version=platform.python_version(),
        platform=f"{platform.platform()} ({sys.platform})",
        mido_version=package_version("mido"),
        python_rtmidi_version=package_version("python-rtmidi"),
    )

    if sys.platform != "win32":
        report.notes.append(
            "This diagnostic targets Windows; any ports listed are those of this operating system."
        )

    try:
        mido = load_mido()
    except ImportError as exc:
        report.notes.append(
            f"mido could not be imported ({describe_error(exc)}). Install it with: {INSTALL_HINT}"
        )
        return report

    report.mido_available = True
    report.backend_name = _backend_name(mido)
    report.inputs = _enumerate("get_input_names", mido)
    report.outputs = _enumerate("get_output_names", mido)

    for direction, result in (("input", report.inputs), ("output", report.outputs)):
        if result.error is None:
            continue
        report.notes.append(f"Could not list MIDI {direction} ports: {result.error}")
        if "rtmidi" in result.error.lower() or result.error.startswith("ImportError"):
            report.notes.append(
                "The MIDI backend may not be installed or loadable. "
                f"Try: {INSTALL_HINT}. The backend can be selected with the MIDO_BACKEND "
                "environment variable."
            )

    if report.ok and not report.inputs.names and not report.outputs.names:
        report.notes.append(
            "The backend works but reported no MIDI input or output ports. Check that the "
            "device is powered on and connected by USB (try another cable or port), then run "
            "this again. Another application using the device could also be a cause."
        )
    elif report.ok and not report.inputs.names:
        report.notes.append("No MIDI input ports were reported, although output ports exist.")
    elif report.ok and not report.outputs.names:
        report.notes.append("No MIDI output ports were reported, although input ports exist.")

    return report


def _format_ports(title: str, result: PortReport) -> list[str]:
    if result.error is not None:
        return [f"{title} ports: unavailable ({result.error})"]
    lines = [f"{title} ports ({len(result.names)}):"]
    if not result.names:
        lines.append("  (none)")
    lines.extend(f"  [{index}] {name}" for index, name in enumerate(result.names))
    return lines


def format_text(report: DiagnosticReport) -> str:
    """Human-readable report."""
    lines = [
        "RP350 Studio - MIDI port diagnostic (read-only: lists ports, opens nothing)",
        f"Python:        {report.python_version}",
        f"Platform:      {report.platform}",
        f"mido:          {report.mido_version or 'not installed'}",
        f"python-rtmidi: {report.python_rtmidi_version or 'not installed'}",
        f"Backend:       {report.backend_name or 'unknown'}",
        "",
    ]
    if report.mido_available:
        lines += _format_ports("Input", report.inputs)
        lines += _format_ports("Output", report.outputs)
    else:
        lines.append("Ports: not listed because mido is unavailable.")
    if report.notes:
        lines += ["", "Notes:"]
        lines += [f"- {note}" for note in report.notes]
    return "\n".join(lines)


def format_json(report: DiagnosticReport) -> str:
    """Machine-readable report."""
    data = asdict(report)
    data["ok"] = report.ok
    return json.dumps(data, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="List MIDI input and output ports (read-only; opens no ports)."
    )
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)

    report = collect_report()
    print(format_json(report) if args.json else format_text(report))
    return 0 if report.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
