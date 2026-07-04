# 빌드 및 배포

## 요구사항
- Windows 10/11 x64
- .NET 8 SDK

## 개발 빌드
```powershell
dotnet restore
dotnet build GmpCompanyCollector.sln -c Release
dotnet test GmpCompanyCollector.sln -c Release
```

## self-contained 배포
```powershell
dotnet publish src/GmpCompanyCollector.App/GmpCompanyCollector.App.csproj `
  -c Release `
  -r win-x64 `
  --self-contained true `
  -p:PublishSingleFile=true `
  -p:IncludeNativeLibrariesForSelfExtract=true `
  -p:PublishReadyToRun=true
```

실행 파일: `src\\GmpCompanyCollector.App\\bin\\Release\\net8.0-windows\\win-x64\\publish\\GmpCompanyCollector.exe`

## Inno Setup
`installer/GmpCompanyCollector.iss`를 Inno Setup Compiler로 열고 Compile을 실행하면 `GmpCompanyCollector_Setup_1.0.0.exe` 설치 파일을 만들 수 있습니다.
