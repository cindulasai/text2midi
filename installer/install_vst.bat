@echo off
setlocal EnableDelayedExpansion
title text2midi - VST3 Plugin Installer
color 0B
cd /d "%~dp0.."
set "PROJECT_DIR=%CD%"

:: ================================================================
::  text2midi  —  VST3 Plugin Standalone Installer
::  ---------------------------------------------------------------
::  Installs just the VST3 plugin and backend server so you
::  can use text2midi directly inside your DAW.
::
::  After running this script, rescan plugins in your DAW
::  and look for "text2midi" under Instruments.
:: ================================================================

echo.
echo  ================================================================
echo     text2midi - VST3 Plugin Installer
echo  ================================================================
echo.
echo  This will install:
echo.
echo    1. text2midi.vst3  →  %CommonProgramFiles%\VST3\
echo    2. Backend server  →  %ProgramFiles%\text2midi\  (optional)
echo.
echo  After installation, rescan plugins in your DAW.
echo  The plugin appears under "Instruments" as "text2midi".
echo.
set /p "CONSENT=  Press ENTER to continue (or Q to quit): "
if /i "!CONSENT!"=="q" (
    echo.
    echo  No problem - run install_vst.bat whenever you are ready.
    timeout /t 3 >nul
    exit /b 0
)
echo.

:: ================================================================
::  STEP 1 / 3  —  Locate VST3 Build
:: ================================================================
echo  ──────────────────────────────────────────────────────────────
echo   Step 1 of 3 : Locating VST3 Plugin
echo  ──────────────────────────────────────────────────────────────

set "VST3_SOURCE="
set "VST3_DEST=%CommonProgramFiles%\VST3\text2midi.vst3"

:: Check Release build
if exist "%PROJECT_DIR%\vst-plugin\build\text2midi_artefacts\Release\VST3\text2midi.vst3" (
    set "VST3_SOURCE=%PROJECT_DIR%\vst-plugin\build\text2midi_artefacts\Release\VST3\text2midi.vst3"
    echo  [OK] Found Release build of text2midi.vst3
)

:: Check Debug build
if "!VST3_SOURCE!"=="" (
    if exist "%PROJECT_DIR%\vst-plugin\build\text2midi_artefacts\Debug\VST3\text2midi.vst3" (
        set "VST3_SOURCE=%PROJECT_DIR%\vst-plugin\build\text2midi_artefacts\Debug\VST3\text2midi.vst3"
        echo  [OK] Found Debug build of text2midi.vst3
    )
)

:: Check if already installed at destination (update scenario)
if "!VST3_SOURCE!"=="" (
    echo.
    echo  [ERROR] VST3 plugin build not found.
    echo.
    echo          The plugin must be compiled from C++ source first.
    echo          Follow these steps:
    echo.
    echo            1. Open a Developer Command Prompt for VS 2022
    echo            2. cd "%PROJECT_DIR%\vst-plugin"
    echo            3. cmake -B build -G "Visual Studio 17 2022" -A x64
    echo            4. cmake --build build --config Release
    echo.
    echo          Then run this script again.
    echo          For full instructions see: vst-plugin\BUILDING.md
    echo.
    pause
    exit /b 1
)
echo.

:: ================================================================
::  STEP 2 / 3  —  Install VST3 Plugin
:: ================================================================
echo  ──────────────────────────────────────────────────────────────
echo   Step 2 of 3 : Installing VST3 Plugin
echo  ──────────────────────────────────────────────────────────────

echo  [..] Destination: !VST3_DEST!

:: Remove old installation if present
if exist "!VST3_DEST!" (
    echo  [..] Removing previous installation...
    rmdir /S /Q "!VST3_DEST!" >nul 2>&1
    if exist "!VST3_DEST!" (
        :: need elevation to remove
        set "VST_RM_SCRIPT=%TEMP%\text2midi_vst_rm.bat"
        echo @echo off > "!VST_RM_SCRIPT!"
        echo rmdir /S /Q "!VST3_DEST!" >> "!VST_RM_SCRIPT!"
        powershell -Command "Start-Process cmd -ArgumentList '/c \"%VST_RM_SCRIPT%\"' -Verb RunAs -Wait" 2>nul
        del "!VST_RM_SCRIPT!" 2>nul
    )
)

:: Copy VST3 bundle
echo  [..] Copying text2midi.vst3...
xcopy /E /I /Y "!VST3_SOURCE!" "!VST3_DEST!" >nul 2>&1
if !errorlevel! equ 0 (
    echo  [OK] VST3 plugin installed to: !VST3_DEST!
    goto :vst_ok
)

:: Need admin privileges — write a temp script and run it as admin
echo  [..] Requesting administrator privileges...
set "VST_COPY_SCRIPT=%TEMP%\text2midi_vst_copy.bat"
echo @echo off > "!VST_COPY_SCRIPT!"
echo xcopy /E /I /Y "!VST3_SOURCE!" "!VST3_DEST!" >> "!VST_COPY_SCRIPT!"
powershell -Command "Start-Process cmd -ArgumentList '/c \"%VST_COPY_SCRIPT%\"' -Verb RunAs -Wait" 2>nul
del "!VST_COPY_SCRIPT!" 2>nul

:: Verify the copy succeeded
if exist "!VST3_DEST!" (
    dir /B "!VST3_DEST!" 2>nul | findstr /R "." >nul 2>&1
    if !errorlevel! equ 0 (
        echo  [OK] VST3 plugin installed to: !VST3_DEST!
        goto :vst_ok
    )
)

echo.
echo  [ERROR] Could not install VST3 plugin.
echo          Try running this script as Administrator, or copy manually:
echo.
echo          From: !VST3_SOURCE!
echo          To:   !VST3_DEST!
echo.
pause
exit /b 1

:vst_ok
echo.

:: ================================================================
::  STEP 3 / 3  —  Backend Server  (optional)
:: ================================================================
echo  ──────────────────────────────────────────────────────────────
echo   Step 3 of 3 : Backend Server  (optional)
echo  ──────────────────────────────────────────────────────────────
echo.
echo  The VST3 plugin needs a backend server for AI generation.
echo  The server runs in the background and the plugin auto-launches it.
echo.

set "BACKEND_SOURCE=%PROJECT_DIR%\vst-plugin\python-backend\dist\text2midi-backend"
set "BACKEND_DEST=%ProgramFiles%\text2midi"

if not exist "!BACKEND_SOURCE!\text2midi-backend.exe" (
    echo  [NOTE] Backend server executable not found.
    echo.
    echo         You can build it with:
    echo           cd vst-plugin\python-backend
    echo           python build_backend.py
    echo.
    echo         Alternatively, start the server manually:
    echo           cd vst-plugin\python-backend
    echo           python server.py
    echo.
    goto :backend_done
)

set /p "BACKEND_CHOICE=  Press ENTER to install backend server, or S to skip: "

if /i "!BACKEND_CHOICE!"=="s" (
    echo.
    echo  [OK] Skipped backend server installation.
    echo       You can start it manually: python vst-plugin\python-backend\server.py
    echo.
    goto :backend_done
)

echo.
echo  [..] Installing backend server to !BACKEND_DEST!...

:: Remove old backend if present
if exist "!BACKEND_DEST!" (
    rmdir /S /Q "!BACKEND_DEST!" >nul 2>&1
    if exist "!BACKEND_DEST!" (
        set "BE_RM_SCRIPT=%TEMP%\text2midi_be_rm.bat"
        echo @echo off > "!BE_RM_SCRIPT!"
        echo rmdir /S /Q "!BACKEND_DEST!" >> "!BE_RM_SCRIPT!"
        powershell -Command "Start-Process cmd -ArgumentList '/c \"%BE_RM_SCRIPT%\"' -Verb RunAs -Wait" 2>nul
        del "!BE_RM_SCRIPT!" 2>nul
    )
)

xcopy /E /I /Y "!BACKEND_SOURCE!" "!BACKEND_DEST!" >nul 2>&1
if !errorlevel! neq 0 (
    echo  [..] Requesting administrator privileges...
    set "BE_COPY_SCRIPT=%TEMP%\text2midi_be_copy.bat"
    echo @echo off > "!BE_COPY_SCRIPT!"
    echo xcopy /E /I /Y "!BACKEND_SOURCE!" "!BACKEND_DEST!" >> "!BE_COPY_SCRIPT!"
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%BE_COPY_SCRIPT%\"' -Verb RunAs -Wait" 2>nul
    del "!BE_COPY_SCRIPT!" 2>nul
)

if exist "!BACKEND_DEST!\text2midi-backend.exe" (
    echo  [OK] Backend server installed to: !BACKEND_DEST!
    echo.

    :: Offer to add to Windows startup
    set /p "STARTUP_CHOICE=  Auto-start server on Windows login? (Y/n): "
    if /i not "!STARTUP_CHOICE!"=="n" (
        reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "text2midi-server" /t REG_SZ /d "\"!BACKEND_DEST!\text2midi-backend.exe\"" /f >nul 2>&1
        if !errorlevel! equ 0 (
            echo  [OK] Server will auto-start on login.
        ) else (
            echo  [NOTE] Could not set auto-start. You can add it manually via Task Manager ^> Startup.
        )
    )
) else (
    echo  [WARNING] Could not install backend server.
    echo            You can run it directly: python vst-plugin\python-backend\server.py
)

:backend_done
echo.

:: ================================================================
::  Done!
:: ================================================================
echo.
echo  ================================================================
echo.
echo     VST3 Plugin Installation Complete!
echo.
echo     Next steps:
echo       1. Open your DAW (Ableton Live, FL Studio, Bitwig, etc.)
echo       2. Rescan / refresh your VST3 plugins
echo       3. Add "text2midi" as an instrument on a MIDI track
echo       4. Type a prompt and click Generate!
echo.
echo     The plugin appears under:
echo       Instruments ^> text2midi
echo.
echo     VST3 location: %CommonProgramFiles%\VST3\text2midi.vst3
echo.
echo     Troubleshooting:
echo       - Plugin not visible?  Rescan plugins in your DAW
echo       - "Server offline"?    Start the backend server manually
echo       - See: vst-plugin\README.md for full docs
echo.
echo  ================================================================
echo.
pause
