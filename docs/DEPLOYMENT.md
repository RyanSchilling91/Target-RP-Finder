# DEPLOYMENT.md

**Doc class: CONTRACT DOC** — a house standard, stamped and
confirmed at project-init, not interviewed like planning docs.
The two-stage VBS launcher is the default for every app unless a
project explicitly overrides it (override logged in
ASSUMPTIONS_AND_OPEN_QUESTIONS.md).

Verification layer for how this app is set up and launched on a
target machine. Answers: "does the deployment match the contract?"

## Launcher — two-stage VBS

| Stage | File | Responsibility |
|---|---|---|
| Setup | RunSetup.vbs | Find Python 3.10+, build venv, install requirements |
| Launch | RunApp.vbs | Verify venv, set PYTHONPATH, start uvicorn, open browser |

Setup runs once per machine. Launch runs every time the user opens
the app. Launch refuses to run if setup has not completed.

## venv location — off-project, on-machine

`%LOCALAPPDATA%\<AppFolder>\.venv`

The venv is NOT in the project folder. It is built on the target
machine under LOCALAPPDATA. `<AppFolder>` is the `APP_FOLDER`
constant, identical in both VBS files. Setup creates the parent
folder if absent and aborts if `.venv\Scripts\python.exe` does not
exist after creation.

## Python discovery (RunSetup.vbs)

Three layers, newest acceptable version wins, 3.10 minimum:
1. Registry — plain `WScript.Shell.RegRead` against explicit
   version-keyed paths (HKCU/HKLM/WOW6432Node ×
   `Software\Python\PythonCore\<ver>\InstallPath\`), versions
   3.14→3.10. Never WMI (`StdRegProv`) — commonly blocked by group
   policy on managed machines and fails silently.
2. Folder scan — LOCALAPPDATA\Programs\Python, PROGRAMFILES\Python, C:\,
   any `python3*` subfolder.
3. PATH — `where python` / `where python3`, version-validated.

Version checks redirect `python -c "..."` output to a temp file and
read it back — never `WScript.Shell.Exec` for stdout capture, same
lockdown risk as WMI.

A Python found but too old aborts with an explicit message, not a
silent fallthrough.

## Dependency pinning (requirements.txt)

No exact version pins unless a specific compatibility reason
requires one. A pin can lack a prebuilt wheel for whatever Python
version is actually on the target machine, forcing pip to build from
source — which fails behind TLS-intercepting corporate proxies. This
is what caused the original setup failure on this project (pinned
`fastapi==0.104.1`/`pydantic==2.5.0` had no Python 3.13 wheel,
pip tried to build `pydantic-core` from source, and the build hit an
SSL error against the network's proxy certificate). Fixed by
unpinning.

## Entry point (RunApp.vbs)

- `PYTHONPATH = src;Trinity` — both src and the Trinity backend
  are import roots. This MUST match the Trinity persistence
  contract in DATA_MODEL.md.
- Command: `python -m uvicorn <package>.main:app --host 127.0.0.1 --port 8000`
- Host/port: localhost only, 8000.
- Browser opens `http://127.0.0.1:8000` after a 5-second sleep.

## Logs — ONE shared file

`<repoRoot>\logs\launcher.log`

Both stages write to the SAME file. There is no separate setup.log
or runapp.log. Entries are pipe-delimited:

`timestamp | username | computername | action | result | detail`

`action` is `SETUP` or `LAUNCH`. `result` is `SUCCESS` or `FAILURE`.
`detail` carries the diagnostic payload, never left blank:
- SETUP success: `python=<path> version=<X.Y.Z> venv=<path>`
- SETUP failure: `no Python 3.10+ found`, or `pip exit=<code>`
- LAUNCH success: `uvicorn responding on 127.0.0.1:8000`
- LAUNCH failure: `venv not found at <path>`, or `uvicorn not
  responding on 127.0.0.1:8000 after Ns`

### Diagnostic routing
- Setup failed → read launcher.log, filter `action = SETUP`, read `detail`
- App won't launch → read launcher.log, filter `action = LAUNCH`, read `detail`
- No LAUNCH line at all → setup never completed, or venv missing
- LAUNCH SUCCESS but app unreachable in browser → uvicorn process died
  after the health check; check Task Manager for a lingering python.exe

Entries older than 30 days are pruned on every write.

## Must never happen
- venv built inside the project folder instead of LOCALAPPDATA
- setup.log / runapp.log created — there is one shared log
- `APP_FOLDER` differing between RunSetup.vbs and RunApp.vbs
- PYTHONPATH omitting Trinity while the data model expects it
- uvicorn bound to anything other than 127.0.0.1
- Python discovery via WMI (`StdRegProv`) or stdout capture via
  `WScript.Shell.Exec` — both fail silently under locked-down policy
- `requirements.txt` pinned to exact versions without a documented
  compatibility reason
- A log entry written with `result = SUCCESS` without an actual
  check (pip exit code, uvicorn health probe) backing it

## Verification criteria
- [ ] RunSetup.vbs and RunApp.vbs share one `APP_FOLDER` value
- [ ] venv resolves under %LOCALAPPDATA%\<AppFolder>\.venv
- [ ] PYTHONPATH=src;Trinity matches DATA_MODEL.md Trinity contract
- [ ] uvicorn target `<package>.main:app` exists and imports
- [ ] logs/launcher.log written with correct action, result, and
      non-blank detail on each stage
- [ ] requirements.txt has no unjustified version pins