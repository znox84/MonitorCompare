# MonitorCompare

모니터 화면 크기를 실제 비율로 비교하는 웹 도구 (PWA).

- 모니터 최대 4개 비교 · 인치/종횡비/피벗 설정
- 드래그 이동 + 가이드 선 스냅 · 높이 정렬 · 확대/축소
- 데스크톱(마우스) / 모바일(터치·핀치 줌) 모두 지원
- **PWA**: 아이폰/안드로이드 홈 화면에 설치, 오프라인 실행

## GitHub Pages 배포

이 폴더(`MonitorCompare`) 자체를 저장소 루트로 올리는 방식이 가장 깔끔합니다.

```bash
# 1) 이 폴더에서 git 초기화
cd MonitorCompare
git init
git add .
git commit -m "MonitorCompare PWA"
git branch -M main

# 2) GitHub에 빈 저장소를 먼저 만든 뒤 (예: monitor-compare) 연결
git remote add origin https://github.com/<사용자명>/<저장소명>.git
git push -u origin main
```

GitHub CLI(`gh`)가 있다면 2단계를 한 줄로:

```bash
gh repo create <저장소명> --public --source=. --remote=origin --push
```

### Pages 활성화
저장소 → **Settings → Pages → Build and deployment**
- **Source**: `Deploy from a branch`
- **Branch**: `main` / `/(root)` → **Save**

1~2분 뒤 아래 주소로 공개됩니다 (HTTPS 자동):

```
https://<사용자명>.github.io/<저장소명>/
```

루트에 접속하면 `index.html`이 `MonitorCompare.html`로 자동 이동합니다.

## 아이폰에 설치

1. **사파리**로 위 주소 접속
2. 공유 버튼(⬆️) → **홈 화면에 추가**
3. 홈 화면 아이콘 실행 → 주소창 없는 전체화면 앱으로 동작

> 설치·오프라인 기능은 **HTTPS**에서만 동작합니다. GitHub Pages는 기본 HTTPS이므로 그대로 됩니다.

## 파일 구성

```
MonitorCompare/
├─ index.html               # 루트 접속 시 앱으로 리다이렉트
├─ MonitorCompare.html      # 앱 본체
├─ manifest.webmanifest     # PWA 매니페스트
├─ sw.js                    # 서비스 워커 (오프라인 캐시)
├─ .nojekyll                # GitHub Pages Jekyll 처리 비활성화
└─ icons/                   # 앱 아이콘 (192 / 512 / 180 / 32)
```

## 아이콘 다시 생성 (선택)

색상/디자인을 바꾸려면 `scripts/gen_icons.py`(색상 상수 수정 후) 재실행. 외부 라이브러리 없이 Python 표준 라이브러리만 사용합니다.
