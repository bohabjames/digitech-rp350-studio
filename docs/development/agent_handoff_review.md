# Agent handoff review

Review-only assessment of the project documentation before implementation begins. It changes no existing instructions, makes no protocol decisions, and uses no external research or hardware.

**Reviewed:** `AGENTS.md`, `CLAUDE.md`, `PROJECT_STATUS.md`, `README.md`, `ARCHITECTURE.md`, plus `TASKS.md` and `RESEARCH.md` (not in the requested list, but both are in the repository and affect the findings).

**Labels used:** **[Fact]** observed in the repository as of commit `16cae3e`; **[Rec]** recommendation, not a decision; **[Open]** unresolved question.

## 1. Conflicts and ambiguities

1. **[Fact]** `README.md` says Codex "implements the Python application", while `ARCHITECTURE.md` calls Python 3 "the current direction" and lists PySide6, Mido/python-rtmidi, NumPy and JSON as "candidates, not locked decisions". The README reads as more settled than the architecture.
2. **[Fact]** `AGENTS.md` tells agents to read "relevant reviewed specifications" before coding. No specification exists in the repository, and no document defines what "reviewed" means or who reviews. Until one exists, the instruction cannot be satisfied.
3. **[Fact]** The required reading lists differ. `AGENTS.md` lists itself, `PROJECT_STATUS.md` and `ARCHITECTURE.md`; `CLAUDE.md` lists `AGENTS.md`, `PROJECT_STATUS.md` and the specification but omits `ARCHITECTURE.md`. Neither mentions `TASKS.md` or `RESEARCH.md`.
4. **[Fact]** `PROJECT_STATUS.md` says "Application implementation: Not started", and `TASKS.md` places "Add MIDI port discovery and read-only monitoring" under "Implementation — after validated specification". `TASKS.md` also lists "Confirm Windows MIDI input/output port names" under research, and `PROJECT_STATUS.md` has a matching pending hardware check. It is unclear whether a port-listing diagnostic counts as research tooling or as application implementation.
5. **[Fact]** Next steps are tracked in two places. `PROJECT_STATUS.md` has four "Next steps" and `TASKS.md` has a longer checklist. They overlap but are not identical (for example, "Confirm Windows MIDI port names" is in `TASKS.md` and the hardware table but not in "Next steps"), and neither states which one is authoritative.
6. **[Fact]** `README.md` states the goal of communicating "over USB MIDI/SysEx". `RESEARCH.md` says the manual documents USB for X-Edit communication and audio streaming, and that Windows MIDI port visibility "remains unverified". The goal is stated before the premise is confirmed.
7. **[Fact]** `RESEARCH.md` describes a supplied capture file (`midi DIGI TECH 350 1st test.syx`, with a SHA-256), and `TASKS.md` wants an offline analyzer for it. The file is not in the repository.
8. **[Fact]** `AGENTS.md` says to "coordinate ownership before parallel edits" but defines no mechanism (no owner table, no CODEOWNERS file, no claim convention).

## 2. Missing decisions that could block implementation

- **[Open]** Python version(s) to support, packaging and dependency tooling (`pyproject.toml`, requirements files, or other), and package/source layout. No Python configuration exists yet.
- **[Open]** Who approves a specification, how approval is recorded, and where specifications live (no `docs/` or spec directory existed before this review).
- **[Open]** Whether Mido/python-rtmidi is approved for the main application or only for prototypes. `ARCHITECTURE.md` says "Confirm Windows MIDI/SysEx support before implementation", with no test or owner for that confirmation.
- **[Open]** Capture handling: whether captures are committed, where, and in what format. The existing capture is flattened `.syx` with no timestamps or direction metadata (`RESEARCH.md`), so future hardware sessions need a defined recording format.
- **[Open]** How hardware test results are recorded and who runs them. `PROJECT_STATUS.md` has a hardware checks table but no procedure, owner, or evidence format.
- **[Open]** Branch, review and merge policy: whether Codex merges Claude's pull requests, whether CI must pass, and whether the default branch is protected.
- **[Open]** Evidence/confidence schema for the parameter database. `ARCHITECTURE.md` says it tracks "evidence/confidence" and `RESEARCH.md` requires source, applicability, confidence and hardware check per claim, but no format is defined.
- **[Open]** Licence. None is present.

## 3. Likely file ownership conflicts

| File or area | Why it conflicts |
|---|---|
| `PROJECT_STATUS.md` | `AGENTS.md` and `CLAUDE.md` require every agent to update it for every change, so every pull request edits the same file. Expect merge conflicts. |
| `TASKS.md` | Checkbox updates from several agents; no stated owner. |
| `RESEARCH.md` | Owned by ChatGPT per its header. Other agents are told to preserve fact/hypothesis labels but have no process for proposing corrections. |
| `pyproject.toml`, requirements, lint/test config | Wanted by the quality-baseline work, a diagnostic tool and Codex's application. First to add it decides the stack. |
| `tests/`, `conftest.py`, `.github/workflows/` | Shared by every code contributor; no layout convention. |
| Port discovery code | `ARCHITECTURE.md` assigns port discovery to the "MIDI transport" component, which Codex will own. A standalone diagnostic risks duplicating it. |
| `README.md` | Contains role definitions and the project goals; any setup docs will land here by default. |

## 4. Proposed development conventions

Small set, intended to reduce duplicated work and context/token use. These are recommendations only.

1. **Single task source.** `TASKS.md` lists work; `PROJECT_STATUS.md` records state. Remove or point duplicated "Next steps" at `TASKS.md`.
2. **Status without conflicts.** Each pull request includes a short "Status impact" section (changes, checks run, hardware checks still needed). Only one agent (suggested: Codex) folds these into `PROJECT_STATUS.md`, or each agent edits a distinct section.
3. **Path ownership table.** A short table in `AGENTS.md` (or CODEOWNERS) mapping paths to owners, and an issue convention that names allowed and forbidden paths for isolated tasks.
4. **One issue, one branch, one pull request.** The pull request states what was tested on Windows, what was tested only with mocks, and what was not tested on hardware.
5. **Evidence tags.** Use `[Confirmed]`, `[Hypothesis]`, `[Unverified]` with a source in every document, matching the rule already in `RESEARCH.md`.
6. **Read-only by construction.** Any code that can emit bytes to the device sits behind one explicit, spec-gated transport path. Diagnostics and monitors use code paths that cannot transmit.
7. **Reading list per task type.** Give each agent a minimal list (for example `AGENTS.md`, `PROJECT_STATUS.md`, the one relevant spec) instead of "read everything". Reference captures by path and hash; do not paste hex dumps into issues or pull requests.

## 5. Questions to resolve before the first application code

1. Does the RP350 appear as a MIDI input and output on the user's Windows machine, and under what names? (Hardware check pending.)
2. Can another application use the same ports while X-Edit or another editor is running, or do they need exclusive access?
3. Is the first code the offline SysEx parser (the first implementation item in `TASKS.md`), and what minimum reviewed framing/checksum description does it need beforehand?
4. What counts as a "reviewed specification", who signs it off, and where does it live?
5. Which Python versions, packaging approach and source layout will be used, and who creates the first `pyproject.toml`?
6. Is Mido/python-rtmidi approved for the main application, or only for exploratory tools?
7. Should the supplied capture be committed, and what format should future captures use to include timestamps and direction?
8. Is read-only monitoring (opening an input port) considered safe before the protocol specification is reviewed, or is enumeration the only pre-specification activity?
9. Who runs hardware tests, and how are results recorded?
10. What is the review and merge policy for pull requests from secondary developers?
