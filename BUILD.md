# 개발자 빌드 문서

## 준비
Windows 10/11 x64와 Python 3.12 이상을 설치합니다. 프로젝트 폴더에서 명령 프롬프트를 엽니다.

## 가상환경과 의존성
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

## 개발 실행
```powershell
.venv\Scripts\python.exe main.py
```

## 테스트 실행
```powershell
.venv\Scripts\python.exe -m pytest
```

## PyInstaller 빌드
one-folder 방식은 시작 속도와 보안 오탐 면에서 더 안정적이며 기본 배포 방식입니다.
```powershell
.venv\Scripts\pyinstaller.exe --noconfirm --clean --windowed --name GmpCompanyCollector GmpCompanyCollector.spec
```
결과물: `dist\GmpCompanyCollector\GmpCompanyCollector.exe`

one-file 방식이 필요하면 다음 명령을 사용합니다.
```powershell
pyinstaller --noconfirm --clean --onefile --windowed --name GmpCompanyCollector main.py
```

## 오류 해결
- pywin32 설치 실패: Windows Python 환경인지 확인합니다.
- Defender 오탐: 코드 서명을 적용하거나 one-folder ZIP 배포를 우선 사용합니다.

## 배포 ZIP
빌드 후 `dist\GmpCompanyCollector` 폴더를 ZIP으로 압축해 배포합니다.

## bat 파일 제거 안내
조직 보안 정책과 PR 검토 부담을 줄이기 위해 `.bat` 확장자 파일은 저장소에서 제거했습니다. 위의 가상환경, 테스트, PyInstaller 명령을 직접 실행하거나 GitHub Actions에서 생성되는 Windows artifact를 사용하면 됩니다.
