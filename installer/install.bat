@echo off
setlocal EnableDelayedExpansion
title text2midi - One-Touch Installer
color 0B
cd /d "%~dp0.."
set "PROJECT_DIR=%CD%"
set "INSTALLER_DIR=%PROJECT_DIR%\installer"

:: ================================================================
::  text2midi  -  AI-Powered MIDI Composer
::  One-Touch Installer for Windows
::  ---------------------------------------------------------------
::  This script is designed for people with ZERO technical
::  background.  Every step has multiple fallbacks.  If something
::  fails the user always gets a clear, friendly message and an
::  option to retry, skip, or quit.
:: ================================================================
echo.
echo  ================================================================
echo     text2midi - AI-Powered MIDI Composer
echo     One-Touch Installer
echo  ================================================================
echo.

:: ── Consent ────────────────────────────────────────────────────────
echo  This installer will set up everything you need:
echo.
echo    1. Python 3.12   (programming runtime  - if not installed)
echo    2. uv            (fast package manager - if not installed)
echo    3. App libraries  (downloaded into a local folder)
echo    4. AI provider    (optional - you can skip and set up later)
echo    5. Launcher       (text2midi.exe you can double-click)
echo    6. VST3 Plugin    (optional - for use inside DAWs)
echo.
echo  Your personal files are NEVER touched.
echo  App config is stored in: %%LOCALAPPDATA%%\text2midi\
echo.
set /p "CONSENT=  Press ENTER to continue (or type Q to quit): "
if /i "!CONSENT!"=="q" (
    echo.
    echo  No problem -- run install.bat whenever you are ready.
    timeout /t 3 >nul
    exit /b 0
)

:: ── Network check ──────────────────────────────────────────────────
echo.
echo  [..] Checking internet connection...
set "NET_OK=0"
ping -n 1 -w 4000 dns.google >nul 2>&1 && set "NET_OK=1"
if "!NET_OK!"=="0" ping -n 1 -w 4000 8.8.8.8 >nul 2>&1 && set "NET_OK=1"
if "!NET_OK!"=="0" ping -n 1 -w 4000 1.1.1.1 >nul 2>&1 && set "NET_OK=1"

if "!NET_OK!"=="1" (
    echo  [OK] Internet connection verified.
) else (
    echo.
    echo  [WARNING] No internet connection detected.
    echo            The installer needs internet to download components.
    echo            text2midi also needs internet to use AI features.
    echo.
    set /p "NETRETRY=  Press R to retry, C to continue anyway, Q to quit: "
    if /i "!NETRETRY!"=="q" exit /b 0
    if /i "!NETRETRY!"=="r" (
        ping -n 1 -w 4000 dns.google >nul 2>&1
        if !errorlevel! equ 0 (
            echo  [OK] Connected!
        ) else (
            echo  [..] Still no connection. Continuing -- some steps may fail.
        )
    )
)

:: ================================================================
::  STEP 1 / 6  —  Python Runtime
:: ================================================================
echo.
echo  ──────────────────────────────────────────────────────────────
echo   Step 1 of 6 : Python Runtime
echo  ──────────────────────────────────────────────────────────────
set "PYTHON_CMD="
set "PYTHON_OK=0"

:: Scan PATH for a suitable Python (3.11+)
for %%P in (python python3 py) do (
    if "!PYTHON_OK!"=="0" (
        where %%P >nul 2>&1
        if !errorlevel! equ 0 (
            for /f "tokens=2 delims= " %%V in ('%%P --version 2^>^&1') do (
                for /f "tokens=1,2 delims=." %%A in ("%%V") do (
                    set "PY_MAJ=%%A"
                    set "PY_MIN=%%B"
                    if !PY_MAJ! geq 3 if !PY_MIN! geq 11 (
                        set "PYTHON_CMD=%%P"
                        set "PYTHON_OK=1"
                        echo  [OK] Found Python %%V
                    )
                )
            )
        )
    )
)

if "!PYTHON_OK!"=="1" goto :python_ready

echo  [..] Python 3.11+ not found. Installing...
echo.

:: -- Fallback 1: winget (built into Windows 10/11) -----------------
where winget >nul 2>&1
if %errorlevel% equ 0 (
    echo  [..] Attempting install via Windows Package Manager (winget)...
    winget install --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements -s winget >nul 2>&1
    if !errorlevel! equ 0 (
        :: Refresh PATH for this session
        set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;!PATH!"
        python --version >nul 2>&1
        if !errorlevel! equ 0 (
            set "PYTHON_CMD=python"
            set "PYTHON_OK=1"
            echo  [OK] Python 3.12 installed via winget.
            goto :python_ready
        )
    )
    echo  [..] winget did not succeed -- trying direct download...
)

:: -- Fallback 2: Download from python.org --------------------------
echo  [..] Downloading Python 3.12 from python.org...

:: Pick the right installer for the CPU architecture
set "PY_URL=https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe"
if "%PROCESSOR_ARCHITECTURE%"=="ARM64" (
    set "PY_URL=https://www.python.org/ftp/python/3.12.9/python-3.12.9-arm64.exe"
)

set "PY_INSTALLER=%TEMP%\text2midi_python_installer.exe"

:: Download with TLS 1.2 enforced — two attempts
set "DL_OK=0"
for /L %%A in (1,1,2) do (
    if "!DL_OK!"=="0" (
        if %%A gtr 1 (
            echo  [..] Retrying download...
            timeout /t 3 /nobreak >nul
        )
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; try{Invoke-WebRequest -Uri '!PY_URL!' -OutFile '!PY_INSTALLER!' -UseBasicParsing -ErrorAction Stop}catch{}" 2>nul
        if exist "!PY_INSTALLER!" set "DL_OK=1"
    )
)

if "!DL_OK!"=="0" (
    echo.
    echo  [ERROR] Could not download Python.
    echo          Please install Python 3.11+ manually from:
    echo          https://www.python.org/downloads/
    echo.
    echo          IMPORTANT: Tick "Add Python to PATH" during install!
    echo          Then close this window and run install.bat again.
    echo.
    pause
    exit /b 1
)

:: Basic size sanity check (legit installer is > 20 MB)
for %%F in ("!PY_INSTALLER!") do set "PY_SIZE=%%~zF"
if !PY_SIZE! lss 20000000 (
    echo  [ERROR] Downloaded file looks too small (!PY_SIZE! bytes).
    echo          It may be corrupt. Please install Python manually:
    echo          https://www.python.org/downloads/
    del "!PY_INSTALLER!" 2>nul
    pause
    exit /b 1
)

echo  [..] Installing Python 3.12 (may take a minute)...
"!PY_INSTALLER!" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
if !errorlevel! neq 0 (
    echo  [..] Silent install returned a non-zero code -- launching graphical installer...
    echo       Please tick "Add Python to PATH" and click Install.
    "!PY_INSTALLER!" PrependPath=1 Include_pip=1
)

:: Clean up installer
del "!PY_INSTALLER!" 2>nul

:: Refresh PATH for this session
set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;!PATH!"

python --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=python"
    set "PYTHON_OK=1"
    echo  [OK] Python 3.12 installed.
) else (
    echo.
    echo  [NOTE] Python was installed but is not visible in this window yet.
    echo         Please CLOSE this window and double-click install.bat again
    echo         so the new PATH takes effect.
    echo.
    pause
    exit /b 1
)

:python_ready
echo.

:: ================================================================
::  STEP 2 / 6  —  uv Package Manager
:: ================================================================
echo  ──────────────────────────────────────────────────────────────
echo   Step 2 of 6 : Package Manager (uv)
echo  ──────────────────────────────────────────────────────────────

where uv >nul 2>&1
if %errorlevel% equ 0 (
    echo  [OK] uv is already installed.
    goto :uv_ready
)

echo  [..] Installing uv (fast Python package manager)...

:: Security: download to a temp file first, verify content, then run
set "UV_PS=%TEMP%\text2midi_uv_install.ps1"
powershell -Command "[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; try{Invoke-WebRequest -Uri 'https://astral.sh/uv/install.ps1' -OutFile '!UV_PS!' -UseBasicParsing -ErrorAction Stop}catch{}" 2>nul

if exist "!UV_PS!" (
    :: Basic integrity check — the installer should mention 'astral'
    findstr /i "astral" "!UV_PS!" >nul 2>&1
    if !errorlevel! equ 0 (
        powershell -ExecutionPolicy RemoteSigned -File "!UV_PS!" 2>nul
        if !errorlevel! neq 0 (
            :: Some corporate machines block RemoteSigned — try Bypass
            powershell -ExecutionPolicy Bypass -File "!UV_PS!" 2>nul
        )
    ) else (
        echo  [..] Installer content did not pass verification -- using pip fallback.
    )
    del "!UV_PS!" 2>nul
)

:: Add common uv install locations to this session's PATH
set "PATH=%USERPROFILE%\.local\bin;%LOCALAPPDATA%\uv;%CARGO_HOME%\bin;%USERPROFILE%\.cargo\bin;!PATH!"

where uv >nul 2>&1
if %errorlevel% equ 0 (
    echo  [OK] uv installed.
    goto :uv_ready
)

:: Fallback: pip install uv
echo  [..] Primary installer did not work -- trying pip...
!PYTHON_CMD! -m pip install uv --quiet 2>nul
if !errorlevel! neq 0 (
    !PYTHON_CMD! -m pip install uv 2>nul
)

where uv >nul 2>&1
if %errorlevel% equ 0 (
    echo  [OK] uv installed via pip.
) else (
    :: Final check in Scripts dir
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\Scripts\uv.exe" (
        set "PATH=%LOCALAPPDATA%\Programs\Python\Python312\Scripts;!PATH!"
        echo  [OK] uv found in Python Scripts folder.
    ) else (
        echo.
        echo  [ERROR] Could not install uv.
        echo          Please try manually:  pip install uv
        echo          Then run install.bat again.
        pause
        exit /b 1
    )
)

:uv_ready
echo.

:: ================================================================
::  STEP 3 / 6  —  Dependencies
:: ================================================================
echo  ──────────────────────────────────────────────────────────────
echo   Step 3 of 6 : Installing App Dependencies
echo  ──────────────────────────────────────────────────────────────
echo  [..] This may take 2-3 minutes on first run...

cd /d "%PROJECT_DIR%"

set "DEP_OK=0"
for /L %%N in (1,1,3) do (
    if "!DEP_OK!"=="0" (
        if %%N gtr 1 (
            echo  [..] Attempt %%N of 3 -- retrying after a short pause...
            timeout /t 5 /nobreak >nul
        )
        uv sync 2>nul
        if !errorlevel! equ 0 set "DEP_OK=1"
    )
)

if "!DEP_OK!"=="1" (
    echo  [OK] All dependencies installed.
) else (
    echo.
    echo  [ERROR] Dependency installation failed after 3 attempts.
    echo          This is usually caused by a flaky internet connection.
    echo.
    echo          You can retry manually later by running:
    echo            cd "%PROJECT_DIR%"
    echo            uv sync
    echo.
    echo          The installer will keep going so the launcher is still
    echo          created -- but the app may not run until dependencies
    echo          are installed.
)
echo.

:: ================================================================
::  STEP 4 / 6  —  AI Provider Setup  (OPTIONAL)
:: ================================================================
echo  ──────────────────────────────────────────────────────────────
echo   Step 4 of 6 : AI Provider Setup  (optional)
echo  ──────────────────────────────────────────────────────────────
echo.
echo  text2midi uses an AI model to turn your words into music.
echo  You need a free API key from one of these providers:
echo.
echo    Groq        (recommended)  https://console.groq.com/keys
echo    Google       Gemini        https://aistudio.google.com/apikey
echo    OpenRouter                 https://openrouter.ai/keys
echo.
echo  Groq is the easiest -- sign up, create a key, paste it below.
echo  No credit card required.
echo.
set /p "SETUP_CHOICE=  Press ENTER to set up now, or S to skip for later: "

if /i "!SETUP_CHOICE!"=="s" (
    echo.
    echo  [OK] Skipped -- no problem!  You can set up anytime:
    echo       - Run:  uv run python main.py --setup
    echo       - Or press Ctrl+S inside the app
    echo.
) else (
    echo.
    uv run python -c "from src.config.setup_wizard import run_setup_wizard; run_setup_wizard()" 2>nul
    if !errorlevel! neq 0 (
        echo.
        echo  [NOTE] The setup wizard had a hiccup, but do not worry!
        echo         You can configure your AI provider any time:
        echo           uv run python main.py --setup
        echo           Or press Ctrl+S inside the app
    )
    echo.
)

:: ================================================================
::  STEP 5 / 6  —  Create Launcher
:: ================================================================
echo  ──────────────────────────────────────────────────────────────
echo   Step 5 of 6 : Creating Launcher
echo  ──────────────────────────────────────────────────────────────

:: Try building a real .exe (small ~5 MB wrapper)
echo  [..] Building text2midi.exe...
uv run python "%INSTALLER_DIR%\build_launcher.py" 2>nul

if exist "%PROJECT_DIR%\text2midi.exe" (
    echo  [OK] text2midi.exe created!
    set "LAUNCHER=%PROJECT_DIR%\text2midi.exe"
    goto :launcher_ready
)

:: Fallback: .bat launcher (always works, no dependencies)
echo  [..] .exe build skipped -- creating batch launcher instead...
(
    echo @echo off
    echo title text2midi - AI-Powered MIDI Composer
    echo cd /d "%PROJECT_DIR%"
    echo set "PATH=%%USERPROFILE%%\.local\bin;%%LOCALAPPDATA%%\uv;%%CARGO_HOME%%\bin;%%USERPROFILE%%\.cargo\bin;%%PATH%%"
    echo uv run python main_tui.py
    echo if %%errorlevel%% neq 0 (
    echo     echo.
    echo     echo   Something went wrong.  Try running: uv run python main.py --setup
    echo     pause
    echo ^)
) > "%PROJECT_DIR%\text2midi.bat"
echo  [OK] text2midi.bat created.
set "LAUNCHER=%PROJECT_DIR%\text2midi.bat"

:launcher_ready

:: Desktop shortcut
set "DESKTOP=%USERPROFILE%\Desktop"
if exist "%DESKTOP%" (
    powershell -Command "try{$ws=New-Object -ComObject WScript.Shell;$s=$ws.CreateShortcut('%DESKTOP%\text2midi.lnk');$s.TargetPath='!LAUNCHER!';$s.WorkingDirectory='%PROJECT_DIR%';$s.Description='text2midi - AI-Powered MIDI Composer';$s.Save();Write-Output 'ok'}catch{}" 2>nul | findstr "ok" >nul 2>&1
    if !errorlevel! equ 0 (
        echo  [OK] Desktop shortcut created!
    )
)

:: ── Cleanup stray temp files ───────────────────────────────────────
del "%TEMP%\text2midi_*.exe" 2>nul
del "%TEMP%\text2midi_*.ps1" 2>nul

echo.
:: ================================================================
::  STEP 6 / 6  —  VST3 Plugin Installation  (OPTIONAL)
:: ================================================================
echo  ──────────────────────────────────────────────────────────────
echo   Step 6 of 6 : VST3 Plugin for DAW  (optional)
echo  ──────────────────────────────────────────────────────────────
echo.
echo  If you use a DAW (Ableton Live, FL Studio, Bitwig, Reaper)
echo  you can install the text2midi VST3 plugin to generate MIDI
echo  directly inside your DAW.
echo.
echo  This step will:
echo    - Copy the VST3 plugin to the system VST3 folder
echo    - Install the backend server that the plugin talks to
echo.
set /p "VST_CHOICE=  Press ENTER to install VST3 plugin, or S to skip: "

if /i "!VST_CHOICE!"=="s" (
    echo.
    echo  [OK] Skipped VST3 plugin installation.
    echo       You can install it later by running:
    echo         installer\install_vst.bat
    echo.
    goto :vst_done
)

echo.
echo  [..] Installing VST3 plugin...

:: ── Check if pre-built VST3 bundle exists ──────────────────────
set "VST3_SOURCE="
set "VST3_DEST=%CommonProgramFiles%\VST3\text2midi.vst3"

:: Check build output first
if exist "%PROJECT_DIR%\vst-plugin\build\text2midi_artefacts\Release\VST3\text2midi.vst3" (
    set "VST3_SOURCE=%PROJECT_DIR%\vst-plugin\build\text2midi_artefacts\Release\VST3\text2midi.vst3"
)
:: Then check Debug build
if "!VST3_SOURCE!"=="" (
    if exist "%PROJECT_DIR%\vst-plugin\build\text2midi_artefacts\Debug\VST3\text2midi.vst3" (
        set "VST3_SOURCE=%PROJECT_DIR%\vst-plugin\build\text2midi_artefacts\Debug\VST3\text2midi.vst3"
    )
)

if "!VST3_SOURCE!"=="" (
    echo  [NOTE] Pre-built VST3 plugin not found.
    echo         The VST3 plugin must be compiled from C++ source first.
    echo         See: vst-plugin\BUILDING.md for build instructions.
    echo.
    echo         After building, run:  installer\install_vst.bat
    echo.
    goto :vst_done
)

:: ── Copy VST3 plugin (needs admin for Program Files) ───────────
echo  [..] Copying text2midi.vst3 to %VST3_DEST%...

:: Try direct copy first (works if user has admin privileges in this session)
xcopy /E /I /Y "!VST3_SOURCE!" "!VST3_DEST!" >nul 2>&1
if !errorlevel! equ 0 (
    echo  [OK] VST3 plugin installed to: !VST3_DEST!
    goto :vst_backend
)

:: Need elevation — write a temp script and run it as admin
set "VST_COPY_SCRIPT=%TEMP%\text2midi_vst_copy.bat"
echo @echo off > "!VST_COPY_SCRIPT!"
echo xcopy /E /I /Y "!VST3_SOURCE!" "!VST3_DEST!" >> "!VST_COPY_SCRIPT!"
echo  [..] Requesting administrator privileges to copy to Program Files...
powershell -Command "Start-Process cmd -ArgumentList '/c \"%VST_COPY_SCRIPT%\"' -Verb RunAs -Wait" 2>nul
del "!VST_COPY_SCRIPT!" 2>nul

:: Verify the copy succeeded — check the destination folder exists and has files
if exist "!VST3_DEST!" (
    dir /B "!VST3_DEST!" 2>nul | findstr /R "." >nul 2>&1
    if !errorlevel! equ 0 (
        echo  [OK] VST3 plugin installed to: !VST3_DEST!
        goto :vst_backend
    )
)

echo  [WARNING] Could not copy VST3 plugin to system folder.
echo            You can copy it manually:
echo            From: !VST3_SOURCE!
echo            To:   !VST3_DEST!
goto :vst_done

:vst_backend
:: ── Install backend server ─────────────────────────────────────
set "BACKEND_SOURCE=%PROJECT_DIR%\vst-plugin\python-backend\dist\text2midi-backend"
set "BACKEND_DEST=%ProgramFiles%\text2midi"

if exist "!BACKEND_SOURCE!\text2midi-backend.exe" (
    echo  [..] Installing backend server to !BACKEND_DEST!...

    xcopy /E /I /Y "!BACKEND_SOURCE!" "!BACKEND_DEST!" >nul 2>&1
    if !errorlevel! neq 0 (
        set "BE_COPY_SCRIPT=%TEMP%\text2midi_be_copy.bat"
        echo @echo off > "!BE_COPY_SCRIPT!"
        echo xcopy /E /I /Y "!BACKEND_SOURCE!" "!BACKEND_DEST!" >> "!BE_COPY_SCRIPT!"
        powershell -Command "Start-Process cmd -ArgumentList '/c \"%BE_COPY_SCRIPT%\"' -Verb RunAs -Wait" 2>nul
        del "!BE_COPY_SCRIPT!" 2>nul
    )

    if exist "!BACKEND_DEST!\text2midi-backend.exe" (
        echo  [OK] Backend server installed to: !BACKEND_DEST!
    ) else (
        echo  [NOTE] Backend server not copied -- it can run from the project folder.
    )
) else (
    echo  [NOTE] Backend server executable not found.
    echo         Build it with:  cd vst-plugin\python-backend ^& python build_backend.py
    echo         The VST3 plugin will try to find the server automatically.
)

echo.
echo  [OK] VST3 plugin installation complete!
echo       Rescan plugins in your DAW -- look for "text2midi" under Instruments.
echo.

:vst_done

:: ================================================================
::  Done!
:: ================================================================
echo.
echo  ================================================================
echo.
echo     Installation complete!
echo.
if exist "%PROJECT_DIR%\text2midi.exe" (
echo     To start making music:
echo       - Double-click  text2midi.exe  in the project folder
) else (
echo     To start making music:
echo       - Double-click  text2midi.bat  in the project folder
)
echo       - Or double-click the desktop shortcut (if created)
echo       - Or run:  uv run python main_tui.py
echo.
echo     To set up or change your AI provider later:
echo       uv run python main.py --setup    (from command line)
echo       Ctrl+S                            (inside the app)
echo.
echo     VST3 Plugin (for DAW users):
echo       - If installed, rescan plugins in your DAW
echo       - To install later:  installer\install_vst.bat
echo.
echo  ================================================================
echo.
pause
