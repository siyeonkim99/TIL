# 부트캠프 TIL

실습 코드(`.py`)에 주석만 달면 학습 노트 사이트가 자동으로 만들어지는 저장소입니다.

## 폴더 구조

```
.
├─ docs/                      # 여기 안에서 실습하고 정리합니다
│  ├─ index.md               # 첫 화면 · 진도표
│  └─ week03-pandas/
│     ├─ groupby.py          # 실습 코드 (여기만 신경 쓰면 됨)
│     ├─ groupby.md          # ← py2md.py 가 자동 생성 (직접 고치지 말 것)
│     └─ data.csv            # 실습 데이터
├─ tools/
│  ├─ py2md.py               # .py → 학습 노트 .md 변환
│  └─ issue_extract.py       # #@@@ → GitHub 이슈 (중복 방지 포함)
├─ .github/workflows/
│  └─ deploy.yml             # push 시 변환·이슈·배포 자동 실행
├─ mkdocs.yml                # 사이트 설정
├─ preview.sh                # 로컬 미리보기
└─ README.md
```

## 주석 기호 5개

| 기호 | 뜻 | 노트에서 |
|---|---|---|
| `#==` | 섹션 제목 | `##` 헤딩 |
| `#>` | 설명 | 본문 문단 |
| `#!` | 막혔던 부분 | 경고 박스 + 다음 코드 줄 강조 |
| `#?` | 나중에 볼 것 | 하단 체크박스 |
| `#@@@` | 따로 팔 큰 주제 | GitHub 이슈 |

파일 맨 위 docstring에 `title:` 과 `tags:` 를 쓰면 노트 제목·태그가 됩니다.

## 처음 세팅 (한 번만)

1. GitHub에 **public** 저장소를 만들고 이 파일들을 올립니다.
2. `mkdocs.yml` 의 `site_url`, `repo_url` 을 본인 주소로 바꿉니다.
3. 저장소 **Settings → Pages → Source** 를 `gh-pages` 브랜치로 지정합니다.
4. 저장소 **Issues → Labels** 에서 `til-todo` 라벨을 하나 만듭니다.
5. 로컬에 도구 설치: `pip install mkdocs-material`

## 매일 하는 일

1. `docs/주차폴더/` 안에서 `.py` 로 실습 + 주석 정리
2. 미리보기: `./preview.sh` → 브라우저에서 http://127.0.0.1:8000
3. `git add . && git commit -m "3주차 groupby" && git push`

push하면 나머지(노트 변환·이슈 생성·사이트 배포)는 자동입니다.

## 주의

- 자동 생성된 `.md` 를 손으로 고치면 다음 push 때 덮어써집니다.
  특정 노트를 직접 다듬고 싶으면, 짝이 되는 `.py` 를 지우고 `.md` 만 남겨
  직접 관리하는 파일로 승격시키세요.
- `#@@@` 는 정말 따로 시간 잡고 팔 큰 주제에만 쓰세요.
  자잘한 건 `#?` 로 노트에 남기는 편이 이슈 목록을 깔끔하게 유지합니다.
