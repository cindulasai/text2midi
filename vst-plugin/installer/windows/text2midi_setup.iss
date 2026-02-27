; text2midi VST3 Plugin — Inno Setup Installer Script
; Build: iscc text2midi_setup.iss

[Setup]
AppName=text2midi
AppVersion=0.1.0
AppPublisher=text2midi
AppPublisherURL=https://github.com/spec-kit
DefaultDirName={autopf}\text2midi
DefaultGroupName=text2midi
OutputBaseFilename=text2midi_setup
Compression=lzma2
SolidCompression=yes
LicenseFile=..\..\LICENSE
SetupIconFile=icon.ico
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Types]
Name: "full"; Description: "Full installation"
Name: "compact"; Description: "VST3 plugin only"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "vst3"; Description: "VST3 Plugin"; Types: full compact custom; Flags: fixed
Name: "server"; Description: "Backend Server (required for generation)"; Types: full custom
Name: "startup"; Description: "Auto-start server on Windows login"; Types: full

[Files]
; VST3 plugin bundle — install to common VST3 directory
Source: "..\..\build\text2midi_artefacts\Release\VST3\text2midi.vst3\*"; \
    DestDir: "{commoncf}\VST3\text2midi.vst3"; \
    Flags: recursesubdirs; Components: vst3

; Backend server executable
Source: "..\..\python-backend\dist\text2midi-backend\*"; \
    DestDir: "{app}"; \
    Flags: recursesubdirs; Components: server

[Icons]
Name: "{group}\text2midi Server"; Filename: "{app}\text2midi-backend.exe"; Components: server
Name: "{group}\Uninstall text2midi"; Filename: "{uninstallexe}"

[Registry]
; Optional: auto-start server on Windows login
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueName: "text2midi-server"; ValueType: string; \
    ValueData: """{app}\text2midi-backend.exe"""; \
    Flags: uninsdeletevalue; Components: startup

[Run]
; Launch server after install
Filename: "{app}\text2midi-backend.exe"; \
    Description: "Start text2midi server now"; \
    Flags: nowait postinstall skipifsilent; Components: server

[UninstallDelete]
Type: filesandordirs; Name: "{commoncf}\VST3\text2midi.vst3"
Type: filesandordirs; Name: "{app}"

[Code]
function InitializeSetup(): Boolean;
begin
    Result := True;
    // Could add .NET / VC++ runtime checks here in the future
end;
