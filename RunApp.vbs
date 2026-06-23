Option Explicit

Const APP_FOLDER = "TargetRPFinder"
Const APP_URL = "http://127.0.0.1:8000"
Const HEALTH_URL = "http://127.0.0.1:8000/health"

Dim oShell, oFSO
Set oShell = CreateObject("WScript.Shell")
Set oFSO = CreateObject("Scripting.FileSystemObject")

Dim repoRoot
repoRoot = oFSO.GetParentFolderName(WScript.ScriptFullName)

oShell.CurrentDirectory = repoRoot

' Check venv exists
Dim strVenv
strVenv = oShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\" & APP_FOLDER & "\.venv"

If Not oFSO.FileExists(strVenv & "\Scripts\python.exe") Then
    MsgBox "Target RP Finder has not been set up on this computer." & Chr(13) & Chr(10) & Chr(13) & Chr(10) & _
           "Please double-click RunSetup.vbs first.", _
           vbExclamation, "Target RP Finder"
    WriteLauncherLog repoRoot, "LAUNCH", "FAILURE", "venv not found at " & strVenv
    WScript.Quit 1
End If

' Set PYTHONPATH
oShell.Environment("Process")("PYTHONPATH") = "src;Trinity"

' Launch FastAPI
Dim strVenvPython
strVenvPython = strVenv & "\Scripts\python.exe"

Dim strCmd
strCmd = Chr(34) & strVenvPython & Chr(34) & _
         " -m uvicorn target_rp_finder.main:app --host 127.0.0.1 --port 8000"

oShell.Run strCmd, 1, False

' Wait for FastAPI to start, then verify it actually responds before
' declaring success — open the browser regardless either way.
WScript.Sleep 5000

Dim isResponding, attempt
isResponding = False
For attempt = 1 To 3
    If IsAppResponding(HEALTH_URL) Then
        isResponding = True
        Exit For
    End If
    WScript.Sleep 2000
Next

oShell.Run APP_URL, 0, False

If isResponding Then
    WriteLauncherLog repoRoot, "LAUNCH", "SUCCESS", "uvicorn responding on 127.0.0.1:8000"
Else
    WriteLauncherLog repoRoot, "LAUNCH", "FAILURE", "uvicorn not responding on 127.0.0.1:8000 after 11s"
End If

' -----------------------------------------------------------------------
Function IsAppResponding(url)
    On Error Resume Next
    Dim http
    Set http = CreateObject("WinHttp.WinHttpRequest.5.1")
    http.SetTimeouts 1000, 1000, 1000, 1000
    http.Open "GET", url, False
    http.Send
    If Err.Number = 0 And http.Status = 200 Then
        IsAppResponding = True
    Else
        IsAppResponding = False
    End If
    Err.Clear
    On Error GoTo 0
End Function

Sub WriteLauncherLog(rootPath, actionName, result, detail)
    Dim fso, logDir, logPath, stream
    Set fso = CreateObject("Scripting.FileSystemObject")
    logDir = rootPath & "\logs"
    logPath = logDir & "\launcher.log"

    If Not fso.FolderExists(logDir) Then
        fso.CreateFolder logDir
    End If

    PruneOldEntries fso, logPath

    Set stream = fso.OpenTextFile(logPath, 8, True)
    stream.WriteLine FormatStamp(Now) & " | " & _
        oShell.ExpandEnvironmentStrings("%USERNAME%") & " | " & _
        oShell.ExpandEnvironmentStrings("%COMPUTERNAME%") & " | " & _
        actionName & " | " & result & " | " & detail
    stream.Close
End Sub

Sub PruneOldEntries(fso, logPath)
    If Not fso.FileExists(logPath) Then Exit Sub
    Dim tmpPath, inFile, outFile, line, parts, ts
    tmpPath = logPath & ".tmp"
    Set inFile = fso.OpenTextFile(logPath, 1)
    Set outFile = fso.OpenTextFile(tmpPath, 2, True)
    Do While Not inFile.AtEndOfStream
        line = inFile.ReadLine
        parts = Split(line, " | ")
        If UBound(parts) >= 0 Then
            On Error Resume Next
            ts = CDate(parts(0))
            On Error GoTo 0
            If IsDate(ts) Then
                If DateDiff("d", ts, Now) <= 30 Then
                    outFile.WriteLine line
                End If
            End If
        End If
    Loop
    inFile.Close
    outFile.Close
    fso.DeleteFile logPath, True
    fso.MoveFile tmpPath, logPath
End Sub

Function FormatStamp(dt)
    FormatStamp = Year(dt) & "-" & _
        Right("0" & Month(dt), 2) & "-" & _
        Right("0" & Day(dt), 2) & " " & _
        Right("0" & Hour(dt), 2) & ":" & _
        Right("0" & Minute(dt), 2) & ":" & _
        Right("0" & Second(dt), 2)
End Function
