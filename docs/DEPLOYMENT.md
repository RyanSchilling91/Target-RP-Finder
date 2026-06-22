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
1. Registry — HKCU/HKLM PythonCore InstallPath, versions 3.14→3.10
2. Folder scan — LOCALAPPDATA\Programs\Python, PROGRAMFILES\Python, C:\
3. PATH — `where python` / `where python3`, version-validated

A Python found but too old aborts with an explicit message, not a
silent fallthrough.

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

`timestamp | username | computername | action | result`

`action` is `SETUP` or `LAUNCH`. `result` is `SUCCESS`.

### Diagnostic routing
- Setup failed → read launcher.log, filter `action = SETUP`
- App won't launch → read launcher.log, filter `action = LAUNCH`
- No LAUNCH line at all → setup never completed, or venv missing

Entries older than 30 days are pruned on every write.

## Must never happen
- venv built inside the project folder instead of LOCALAPPDATA
- setup.log / runapp.log created — there is one shared log
- `APP_FOLDER` differing between RunSetup.vbs and RunApp.vbs
- PYTHONPATH omitting Trinity while the data model expects it
- uvicorn bound to anything other than 127.0.0.1

## Verification criteria
- [ ] RunSetup.vbs and RunApp.vbs share one `APP_FOLDER` value
- [ ] venv resolves under %LOCALAPPDATA%\<AppFolder>\.venv
- [ ] PYTHONPATH=src;Trinity matches DATA_MODEL.md Trinity contract
- [ ] uvicorn target `<package>.main:app` exists and imports
- [ ] logs/launcher.log written with correct action on each stage