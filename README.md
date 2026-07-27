# 부트캠프 TIL

실습 코드(`.py`)에 주석만 달면 학습 노트 사이트가 자동으로 만들어지는 저장소입니다.
`git push` 한 번이면 노트 변환 → 공부 주제 이슈 생성 → 사이트 배포가 자동으로 돕니다.

## 폴더 구조

```
.
├─ docs/                      # 여기 안에서 실습하고 정리합니다
│  ├─ index.md               # 첫 화면 · 진도표
│  └─ week03-pandas/         # 주차별 폴더
│     ├─ groupby.py          # 실습 코드 (여기만 신경 쓰면 됨)
│     ├─ groupby.md          # ← py2md.py 가 자동 생성 (직접 고치지 말 것)
│     └─ data.csv            # 실습 데이터
├─ tools/
│  ├─ py2md.py               # .py → 학습 노트 .md 변환
│  └─ issue_extract.py       # #@@@ → GitHub 이슈 (중복 방지 포함)
├─ .github/workflows/
│  └─ deploy.yml             # push 시 변환·이슈·배포 자동 실행
├─ .vscode/
│  └─ python.code-snippets   # 기호 입력 단축어 (til, sec, fold 등)
├─ mkdocs.yml                # 사이트 설정
├─ preview.sh                # 로컬 미리보기
└─ README.md
```

## 주석 기호

실습 `.py` 파일에 아래 기호를 주석으로 달면 노트가 자동으로 만들어집니다.

| 기호 | 뜻 | 노트에서 |
|---|---|---|
| `#==` | 섹션 제목 | `##` 헤딩 |
| `#>` | 설명 (여러 줄은 한 문단으로 합쳐짐) | 본문 문단 |
| `#!` | 배운 점 · 막혔던 부분 | 노란 박스 (코드 바로 밑, 연속된 줄은 한 박스로) |
| `#?` | 나중에 볼 것 | 하단 체크박스 |
| `#@@@` | 따로 팔 큰 주제 | GitHub 이슈 |
| `#(1)` | 코드 줄 강조 + 클릭 주석 (마커) | 그 줄이 파란 배경, 옆 번호 클릭 시 설명 표시 |
| `#(1)>` | 위 마커의 여러 줄 설명 | 클릭 시 펼쳐지는 내용 (줄바꿈 유지) |
| `# --8<-- [start]`<br>`# --8<-- [end]` | 노트에 넣을 코드 구간의 시작·끝 | 이 구간 안의 코드만 노트에 나옴 |

`title:` 과 `tags:` 는 파일 어디에 있어도 됩니다 (맨 위가 아니어도 인식).
`title:` 이 아예 없으면 아직 안 쓴 파일로 보고 노트를 만들지 않습니다.

## 중요: 코드는 감싼 구간만 나옵니다

노트에 코드를 넣으려면 그 부분을 `# --8<-- [start]` 와 `# --8<-- [end]` 로
감싸야 합니다. 감싸지 않은 코드는 노트에 나오지 않습니다 (섹션 제목·설명만 남음).

```python
#== 게시글 생성

# --8<-- [start]
@app.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    created_post = Post(**post.model_dump())  #(1)
    #(1)> model_dump()가 pydantic 객체를 dict로 변환
    #(1)> **가 그 dict를 키워드 인자로 풀어줌 → Post(title=..., ...)
    db.add(created_post)
    return created_post
# --8<-- [end]

#! 응답으로 나갈 때(return)는 FastAPI가 pydantic→JSON을 자동으로 해준다.
#! DB 객체 생성 같은 중간 작업은 자동이 아니라 직접 model_dump()가 필요하다.
```

- 이름은 없어도 됩니다. 한 파일에서 여러 구간을 뽑을 때만 `[start:이름]` 처럼 구분하세요.
- `#(1)` 을 붙인 줄은 파란 배경으로 강조되고, 옆 번호를 누르면 `#(1)>` 설명이 펼쳐집니다.
- 코드 줄에 `#(1)` 마커를 안 붙이고 바로 아래에 `#(1)>` 만 써도 됩니다.
  그러면 직전 코드 줄에 자동으로 마커가 붙습니다.

## 처음 세팅 (한 번만)

1. GitHub에 **public** 저장소를 만들고 이 파일들을 올립니다.
2. `mkdocs.yml` 의 `site_url`, `repo_url` 을 본인 주소로 바꿉니다.
3. 저장소 **Settings → Actions → General → Workflow permissions** 를
   **Read and write permissions** 로 바꿉니다 (배포·이슈 생성에 필요).
4. 첫 push 후 워크플로우가 성공하면 `gh-pages` 브랜치가 생깁니다.
   그다음 **Settings → Pages → Source** 를 `gh-pages` 브랜치 / `/ (root)` 로 지정합니다.
5. 저장소 **Issues → Labels** 에서 `til-todo` 라벨을 하나 만듭니다.
6. 로컬에 도구 설치: `pip install mkdocs-material`

> 워크플로우 파일(`.github/workflows/deploy.yml`)을 로컬에서 push 하려면
> Personal Access Token 에 `workflow` 권한이 필요합니다. 없으면 push 가 거부되니,
> 토큰에 권한을 추가하거나 이 파일만 GitHub 웹에서 직접 만드세요.

## 기호 입력 단축어 (VS Code / Cursor)

`.vscode/python.code-snippets` 덕분에 `.py` 파일에서 단축어 + Tab 으로 기호를 넣을 수 있습니다.

| 단축어 | 나오는 것 |
|---|---|
| `til` | 파일 전체 기본 틀 (title, tags, 섹션) |
| `sec` | `#== ` |
| `desc` | `#> ` |
| `stuck` | `#! ` |
| `todo` | `#? ` |
| `issue` | `#@@@ ` |
| `fold` | `#(1)` 마커 + `#(1)>` 설명 줄 |
| `fold+` | `#(1)>` (설명 다음 줄) |

## 매일 하는 일

1. `docs/주차폴더/` 안에서 `.py` 로 실습하며 주석으로 정리
   (노트에 넣을 코드는 `# --8<-- [start]` / `[end]` 로 감싸기)
2. 미리보기: `./preview.sh` → 브라우저에서 http://127.0.0.1:8000
3. `git add . && git commit -m "3주차 groupby" && git push`

push하면 나머지(노트 변환·이슈 생성·사이트 배포)는 자동입니다.

## 주의

- 자동 생성된 `.md` 를 손으로 고치면 다음 push 때 덮어써집니다.
  특정 노트를 직접 다듬고 싶으면, 짝이 되는 `.py` 를 지우고 `.md` 만 남겨
  직접 관리하는 파일로 승격시키세요.
- `#@@@` 는 정말 따로 시간 잡고 팔 큰 주제에만 쓰세요.
  자잘한 건 `#?` 로 노트에 남기는 편이 이슈 목록을 깔끔하게 유지합니다.
- 코드 줄 강조 클릭 주석(`#(1)`)은 브라우저에서 JavaScript로 펼쳐집니다.
  정적 미리보기가 아니라 실제 배포된 사이트나 `mkdocs serve` 에서 확인하세요.