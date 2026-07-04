#define MyAppName "GmpCompanyCollector"
#define MyAppVersion "1.0.0"
[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\GmpCompanyCollector
DefaultGroupName=GMP 업체·제조소 데이터 수집기
OutputBaseFilename=GmpCompanyCollector_Setup_1.0.0
[Tasks]
Name: "desktopicon"; Description: "바탕화면 바로가기 만들기"; GroupDescription: "추가 아이콘:"
[Files]
Source: "..\src\GmpCompanyCollector.App\bin\Release\net8.0-windows\win-x64\publish\*"; DestDir: "{app}"; Flags: recursesubdirs
[Icons]
Name: "{group}\GMP 업체·제조소 데이터 수집기"; Filename: "{app}\GmpCompanyCollector.exe"
Name: "{autodesktop}\GMP 업체·제조소 데이터 수집기"; Filename: "{app}\GmpCompanyCollector.exe"; Tasks: desktopicon
