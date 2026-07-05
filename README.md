# GMP 업체·제조소 데이터 수집기

Python/tkinter 기반 Windows 데스크톱 프로그램입니다. 식품의약품안전처 `의약품 등 업체허가현황` OpenAPI의 업체 목록(`/getDrugBsshListInq`)과 업체·제조소 상세(`/getDrugBsshItemInq`) 데이터를 수집해 화면 조회, Excel, CSV 저장을 제공합니다.

## 주요 기능
- 서비스키 자동 감지/Decoding/Encoding 모드 및 Windows DPAPI 저장
- JSON/XML 자동 판별과 공공데이터 XML 오류 한글 안내
- 자동 페이지 수집, 재시도, 취소, 요청 간격 적용
- 업체명 정규화, 날짜 변환, 주소 분석, 중복 표시
- openpyxl Excel 저장, utf-8-sig CSV 저장
- PyInstaller Windows EXE 빌드 스크립트와 GitHub Actions 워크플로 제공

## 일반 사용자 실행
Windows 빌드 산출물 ZIP을 압축 해제한 뒤 `GmpCompanyCollector.exe`를 실행합니다. Python 설치가 필요 없습니다.

## 개발 실행
```bash
python main.py
```

## 테스트
```bash
python -m pytest
```

## Windows EXE 빌드
```bash
pyinstaller --noconfirm --clean --windowed --name GmpCompanyCollector GmpCompanyCollector.spec
```

## 빌드 스크립트 안내
보안 정책 충돌을 줄이기 위해 `.bat` 파일은 포함하지 않습니다. 개발 실행과 빌드는 `BUILD.md`의 Python/PyInstaller 명령 또는 GitHub Actions artifact를 사용하십시오.
