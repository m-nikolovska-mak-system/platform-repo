#ifndef AppName
  #define AppName "DefaultApp"
#endif
#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif
#ifndef JarFileName
  #define JarFileName "app.jar"
#endif
#ifndef OutputBaseName
  #define OutputBaseName "Setup"
#endif

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=output
OutputBaseFilename={#OutputBaseName}
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "build\libs\{#JarFileName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "javaw.exe"; Parameters: "-jar ""{app}\{#JarFileName}"""; WorkingDir: "{app}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
