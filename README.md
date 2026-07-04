# GMP 업체·제조소 데이터 수집기

식품의약품안전처 `의약품 등 업체허가현황` 공공데이터 OpenAPI로 의약품 업체 목록과 제조소 상세정보를 수집하고 Excel/CSV로 저장하는 .NET 8 WPF 프로그램입니다.

## 주요 기능
- Decoding/Encoding/자동 감지 서비스키 입력 및 DPAPI 저장
- 업체 목록 API(`/getDrugBsshListInq`)와 상세 API(`/getDrugBsshItemInq`) 자동 페이지 수집
- JSON/XML 정상 응답 및 XML 오류 응답 자동 판별
- 수집 진행률, 취소, 로그 파일 저장
- 업체명 정규화, 날짜 변환, 주소 시·도/시·군·구 추출, 중복 표시
- DataGrid 조회, Excel(xlsx), CSV(UTF-8 BOM) 내보내기

## 공공데이터포털 활용신청 방법
공공데이터포털 로그인 → `의약품 등 업체허가현황` 검색 → 활용신청 → 개발계정 승인 → 마이페이지에서 인증키 확인 순서로 진행합니다.

## 서비스키 확인 및 형식
마이페이지에서 Encoding 인증키와 Decoding 인증키를 확인할 수 있습니다. Decoding 키는 프로그램이 URL 인코딩하고, Encoding 키는 이미 인코딩된 `%2B`, `%2F`, `%3D` 값을 다시 인코딩하지 않습니다. 처음 사용 시 `자동 감지`를 권장합니다.

## 실행 방법
배포 폴더의 `GmpCompanyCollector.exe`를 실행합니다. 별도 .NET 런타임 설치가 필요 없도록 self-contained 배포를 제공합니다.

## 데이터 수집 방법
1. `API 설정` 탭에서 서비스키를 입력합니다.
2. `API 연결 테스트`를 눌러 전체 검색 결과와 응답 시간을 확인합니다.
3. `데이터 수집` 탭에서 수집 종류와 검색조건을 선택합니다.
4. `수집 시작`을 누르고 진행률을 확인합니다.

## Excel 저장 방법
`수집 결과` 탭의 `Excel 저장` 버튼을 누르면 바탕화면에 `의약품_업체허가현황_yyyyMMdd_HHmmss.xlsx` 파일이 생성됩니다. 서비스키는 Excel에 기록하지 않습니다.

## 일반적인 오류 해결
- 등록되지 않은 인증키: 인증키 값과 Encoding/Decoding 선택을 확인합니다.
- 활용기간 만료: 공공데이터포털에서 활용기간을 갱신합니다.
- 요청 한도 초과: 다음 날 또는 제한 해제 후 다시 시도합니다.
- Excel 저장 실패: 같은 파일이 Excel에서 열려 있는지 확인합니다.

## 보안 안내
서비스키 원문은 로그, README, appsettings에 저장하지 않습니다. `인증키 기억하기`를 선택한 경우 `%LocalAppData%\\GmpCompanyCollector\\settings.dat`에 Windows DPAPI로 암호화되어 저장됩니다.

## 개발자 빌드
```powershell
dotnet restore
dotnet build GmpCompanyCollector.sln -c Release
dotnet test GmpCompanyCollector.sln -c Release
```

## 배포 파일 생성
```powershell
dotnet publish src/GmpCompanyCollector.App/GmpCompanyCollector.App.csproj `
  -c Release `
  -r win-x64 `
  --self-contained true `
  -p:PublishSingleFile=true `
  -p:IncludeNativeLibrariesForSelfExtract=true `
  -p:PublishReadyToRun=true
```

출력 위치: `src\\GmpCompanyCollector.App\\bin\\Release\\net8.0-windows\\win-x64\\publish\\`

## 알려진 제약사항
- 현재 리눅스 컨테이너에는 .NET SDK가 없어 이 환경에서 실제 빌드/게시 검증은 수행하지 못했습니다.
- 차트는 1차 버전에서 표/Excel 시트 중심으로 구현되어 있으며 향후 시각화 라이브러리를 추가할 수 있습니다.
