; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppID={{4714199A-0D66-4E69-97FF-7B54BFF80B88}
AppCopyright=%(AppCopyright)s
AppName=%(AppName)s
AppVerName=%(AppName)s %(AppVerName)s
AppPublisher=%(AppPublisher)s
AppPublisherURL=%(AppPublisherURL)s
AppReadmeFile={app}\README.html
AppSupportURL=%(AppSupportURL)s
AppUpdatesURL=%(AppUpdatesURL)s
DefaultDirName={pf}\%(AppName)s
DefaultGroupName=%(AppName)s
LicenseFile=..\LICENSE.txt
OutputDir=.
OutputBaseFilename=%(AppName)s-%(AppVersion)s-Setup
SetupIconFile=..\%(AppName)s\theme\icons\%(AppName)s.ico
Compression=lzma/Max
SolidCompression=true
VersionInfoVersion=%(VersionInfoVersion)s
VersionInfoDescription=%(AppName)s Setup
VersionInfoTextVersion=%(VersionInfoTextVersion)s
WizardImageFile=..\misc\media\install.bmp
WizardSmallImageFile=..\misc\media\icon-install.bmp
AppVersion=%(AppVersion)s
UninstallDisplayName=%(AppName)s
UninstallDisplayIcon={app}\%(AppName)s.exe
AlwaysShowComponentsList=false
ShowLanguageDialog=auto
MinVersion=0,5.1.2600
SignTool=sign.cmd
SignedUninstaller=yes

[Languages]
Name: english; MessagesFile: ..\misc\InnoSetup\v5\Default.isl; 
Name: french; MessagesFile: ..\misc\InnoSetup\v5\Languages\French.isl; 
Name: german; MessagesFile: ..\misc\InnoSetup\v5\Languages\German.isl; 
Name: italian; MessagesFile: ..\misc\InnoSetup\v5\Languages\Italian.isl; 
Name: spanish; MessagesFile: ..\misc\InnoSetup\v5\Languages\Spanish.isl; 

[Tasks]
Name: desktopicon; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked
Name: quicklaunchicon; Description: {cm:CreateQuickLaunchIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked
Name: calibrationloadinghandledbydisplaycal; Description: {cm:CalibrationLoadingHandledByDisplayCAL}; Flags: exclusive; GroupDescription: {cm:CalibrationLoading}; 
Name: calibrationloadinghandledbyos; Description: {cm:CalibrationLoadingHandledByOS}; Flags: exclusive unchecked; GroupDescription: {cm:CalibrationLoading}; MinVersion: 0,6.1.7600; 

[Files]
Source: py2exe.%(Platform)s-py%(PythonVersion)s\%(AppName)s-%(AppVersion)s\*; DestDir: {app}; Flags: recursesubdirs replacesameversion; Excludes: \%(AppName)s.exe,\README.html,\README-fr.html; 
Source: py2exe.%(Platform)s-py%(PythonVersion)s\%(AppName)s-%(AppVersion)s\%(AppName)s.exe; DestDir: {app}; Flags: replacesameversion; 
Source: py2exe.%(Platform)s-py%(PythonVersion)s\%(AppName)s-%(AppVersion)s\README.html; DestDir: {app}; Flags: isreadme; 
Source: py2exe.%(Platform)s-py%(PythonVersion)s\%(AppName)s-%(AppVersion)s\README-fr.html; DestDir: {app}; Flags: isreadme; Languages: french
Source: ..\..\ccss\*.ccss; DestDir: {commonappdata}\ArgyllCMS; Flags: replacesameversion; 

[Icons]
Name: {group}\%(AppName)s; Filename: {app}\%(AppName)s.exe; IconFilename: {app}\%(AppName)s.exe
Name: "{group}\%(AppName)s Profile Loader"; Filename: {app}\%(AppName)s-apply-profiles.exe; IconFilename: {app}\%(AppName)s-apply-profiles.exe; 
Name: "{group}\3DLUT Maker"; Filename: {app}\%(AppName)s-3DLUT-maker.exe; IconFilename: {app}\%(AppName)s-3DLUT-maker.exe; 
Name: "{group}\Curve Viewer"; Filename: {app}\%(AppName)s-curve-viewer.exe; IconFilename: {app}\%(AppName)s-curve-viewer.exe; 
Name: "{group}\Profile Info"; Filename: {app}\%(AppName)s-profile-info.exe; IconFilename: {app}\%(AppName)s-profile-info.exe; 
Name: "{group}\Synthetic Profile Creator"; Filename: {app}\%(AppName)s-synthprofile.exe; IconFilename: {app}\%(AppName)s-synthprofile.exe; 
Name: "{group}\Scripting Client"; Filename: {app}\%(AppName)s-scripting-client.exe; IconFilename: {app}\%(AppName)s-scripting-client.exe; 
Name: "{group}\Testchart Editor"; Filename: {app}\%(AppName)s-testchart-editor.exe; IconFilename: {app}\%(AppName)s-testchart-editor.exe; 
Name: "{group}\VRML to X3D converter"; Filename: {app}\%(AppName)s-VRML-to-X3D-converter.exe; IconFilename: {app}\%(AppName)s-VRML-to-X3D-converter.exe; 
Name: {group}\{cm:UninstallProgram,%(AppName)s}; Filename: {uninstallexe}; IconFilename: {app}\theme\icons\%(AppName)s-uninstall.ico; Tasks: ; Languages: 
Name: {commondesktop}\%(AppName)s; Filename: {app}\%(AppName)s.exe; Tasks: desktopicon; IconFilename: {app}\%(AppName)s.exe
Name: {userappdata}\Microsoft\Internet Explorer\Quick Launch\%(AppName)s; Filename: {app}\%(AppName)s.exe; Tasks: quicklaunchicon; IconFilename: {app}\%(AppName)s.exe
Name: {group}\LICENSE; Filename: {app}\LICENSE.txt
Name: {group}\README (EN); Filename: {app}\README.html; Tasks: ; Languages: 
Name: {group}\README (FR); Filename: {app}\README-fr.html; Tasks: ; Languages: french
Name: "{commonstartup}\%(AppName)s Profile Loader"; Filename: {app}\%(AppName)s-apply-profiles.exe; OnlyBelowVersion: 0,6.0; Tasks: calibrationloadinghandledbydisplaycal; 

[Run]
Filename: {app}\%(AppName)s.exe; Description: {cm:LaunchProgram,%(AppName)s}; Flags: nowait postinstall skipifsilent;
MinVersion: 0,6.1.7600; Filename: {app}\lib\python.exe; Parameters: "-S -c ""import sys; sys.path.insert(0, '\\'.join(sys.executable.replace('/', '\\').split('\\')[:-1]) + '\\library.zip'); from %(AppName)s import util_win; None if not util_win.calibration_management_isenabled() else util_win.disable_calibration_management();"""; Flags: RunHidden RunAsCurrentUser; Description: {cm:CalibrationLoadingHandledByDisplayCAL}; Tasks: calibrationloadinghandledbydisplaycal; 
MinVersion: 0,6.0; Filename: schtasks.exe; parameters: "/Delete /TN ""%(AppName)s Profile Loader Launcher"" /F"; Flags: RunHidden RunAsCurrentUser;
MinVersion: 0,6.0; Filename: {app}\lib\python.exe; Parameters: "-S -c ""import sys; sys.path.insert(0, '\\'.join(sys.executable.replace('/', '\\').split('\\')[:-1]) + '\\library.zip'); from %(AppName)s.profile_loader import setup_profile_loader_task; setup_profile_loader_task('{app}\%(AppName)s-apply-profiles.exe', '{app}', '{app}')"""; Flags: RunHidden RunAsCurrentUser; Tasks: calibrationloadinghandledbydisplaycal; 
Filename: {app}\%(AppName)s-apply-profiles.exe; Flags: nowait runasoriginaluser; Tasks: calibrationloadinghandledbydisplaycal; 
MinVersion: 0,6.1.7600; Filename: {app}\lib\python.exe; Parameters: "-S -c ""import sys; sys.path.insert(0, '\\'.join(sys.executable.replace('/', '\\').split('\\')[:-1]) + '\\library.zip'); from %(AppName)s import util_win; None if util_win.calibration_management_isenabled() else util_win.enable_calibration_management();"""; Flags: RunHidden RunAsCurrentUser; Description: {cm:CalibrationLoadingHandledByOS}; Tasks: calibrationloadinghandledbyos; 

[InstallDelete]
Type: files; Name: "{commonstartup}\dispcalGUI Profile Loader.lnk"
Type: files; Name: "{group}\*dispcalGUI*"
Type: files; Name: "{app}\dispcalGUI*.exe"
Type: files; Name: "{app}\lib\dispcalGUI*"
Type: files; Name: "{app}\screenshots\dispcalGUI*.png"
Type: files; Name: "{app}\theme\dispcalGUI*.png"
Type: files; Name: "{app}\theme\icons\dispcalGUI*.ico"
Type: files; Name: "{app}\theme\icons\16x16\dispcalGUI*.png"
Type: files; Name: "{app}\theme\icons\32x32\dispcalGUI*.png"
Type: files; Name: "{userstartup}\%(AppName)s Profile Loader.lnk"
Type: files; Name: "{commonstartup}\%(AppName)s Profile Loader.lnk"
Type: filesandordirs; Name: "{userprograms}\{groupname}"
Type: filesandordirs; Name: "{commonprograms}\{groupname}"

[UninstallRun]
Filename: taskkill.exe; parameters: /im %(AppName)s-apply-profiles.exe; Flags: RunHidden RunAsCurrentUser;
Filename: schtasks.exe; parameters: "/Delete /TN ""%(AppName)s Profile Loader Launcher"" /F"; Flags: RunHidden RunAsCurrentUser;

[Code]
function Get_RunEntryShellExec_Message(Value: string): string;
begin
	Result := FmtMessage(SetupMessage(msgRunEntryShellExec), [Value]);
end;

function Get_UninstallString(AppId: string): string;
var
	UninstallString: string;
begin
	if not RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\' + AppId + '_is1', 'UninstallString', UninstallString) and
		not RegQueryStringValue(HKLM, 'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\' + AppId + '_is1', 'UninstallString', UninstallString) and
			not RegQueryStringValue(HKCU, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\' + AppId + '_is1', 'UninstallString', UninstallString) then
				RegQueryStringValue(HKCU, 'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\' + AppId + '_is1', 'UninstallString', UninstallString);
	Result := RemoveQuotes(UninstallString);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
	ErrorCode: integer;
	UninstallString: string;
begin
	if CurStep=ssInstall then begin
		UninstallString := Get_UninstallString(ExpandConstant('{#emit SetupSetting("AppId")}'));
		if UninstallString <> '' then begin
			if not Exec(UninstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES', '', SW_SHOW, ewWaitUntilTerminated, ErrorCode) then begin
				SuppressibleMsgBox(SysErrorMessage(ErrorCode), mbError, MB_OK, MB_OK);
			end;
		end;
	end;
end;
