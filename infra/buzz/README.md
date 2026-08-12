# Buzz 자체 호스팅 세팅 (사람 + AI 에이전트 협업 워크스페이스)

Block(잭 도시의 회사)이 공개한 오픈소스 **[block/buzz](https://github.com/block/buzz)** 를
YJT 자체 서버에 올리기 위한 설치·운영 자산입니다. Apache-2.0 라이선스.

> **먼저 알아둘 것 — SNS 글의 설명과 실제는 다릅니다**
>
> | SNS 글 | 실제 |
> |---|---|
> | "AI 에이전트가 비즈니스를 전부 관리하는 프레임워크" | 사람과 AI 에이전트가 **같은 채널에서 대화·협업**하는 자체 호스팅 워크스페이스 (Slack + Nostr 프로토콜) |
> | "네 개의 서버: 채널·검색·Git·자동화" | 컨테이너 4개 = **buzz-relay(Rust) + PostgreSQL + Redis + MinIO** (검색·Git·워크플로는 릴레이 내부 기능) |
> | "GitHub 스타 14,400" | 2026년 8월 기준 26.7k |
>
> 즉 이걸 깐다고 업무가 자동화되지는 않습니다. **에이전트가 참여할 수 있는 대화 공간**이
> 생기는 것이고, 실제 업무 자동화는 그 위에 채널·워크플로를 설계해야 나옵니다.

---

## 1. 구조

```
  사람 (데스크톱 앱 / 브라우저)          AI 에이전트 (Claude Code)
            │                                    │
            │  WebSocket (Nostr NIP-01)          │  buzz-acp 하네스
            └────────────► buzz-relay ◄──────────┘
                               │
        ┌──────────────┬───────┴────────┬──────────────┐
   PostgreSQL       Redis            MinIO         git 볼륨
   (이벤트+검색)    (pub/sub)      (미디어/S3)     (저장소)
```

- 모든 메시지·리액션·승인·git 이벤트가 **서명된 단일 이벤트 로그**에 쌓입니다(감사 추적).
- 에이전트는 사람과 **동일한 방식**으로 채널 멤버가 됩니다. 자기 키쌍과 자기 감사 로그를 가집니다.
- 에이전트는 `buzz` CLI(JSON in/out)로 메시지 전송·채널 생성·이슈/PR 작업을 합니다.

## 2. 사전 준비

| 항목 | 최소 | 권장 |
|---|---|---|
| 서버 | 2 vCPU / 4GB RAM / 40GB SSD | 4 vCPU / 8GB RAM / 100GB SSD |
| OS | Docker 가 도는 Linux (Ubuntu 22.04+ 등) | 동일 |
| 소프트웨어 | Docker + Compose **v2.24.4 이상**, git, openssl | 동일 |
| 네트워크 | 80/443 인바운드 허용 | 동일 |
| DNS | `buzz.yourdomain.com` A 레코드 → 서버 IP | 동일 |

에이전트 컨테이너까지 같은 서버에서 돌린다면 RAM 8GB 이상을 권장합니다
(에이전트 이미지 빌드 시 Rust 컴파일에 메모리를 많이 씁니다).

버전 확인:

```bash
docker compose version   # v2.24.4 이상이어야 함
```

## 3. 릴레이 설치 (10분)

```bash
cd infra/buzz

# 공개 도메인 + 자동 HTTPS(Let's Encrypt)
./bootstrap.sh --domain buzz.yourdomain.com

# 또는 노트북에서 먼저 확인만 해보고 싶다면
./bootstrap.sh --local
```

`bootstrap.sh` 가 하는 일:

1. `block/buzz` 를 `~/buzz` 에 클론 (`--src` 로 경로 변경 가능)
2. `buzz-admin generate-key` 로 **릴레이 서명 키쌍**과 **오너(관리자) 키쌍** 생성
3. DB/Redis/S3 비밀번호를 `openssl rand` 로 생성
4. `~/buzz/deploy/compose/.env` 를 완성된 상태로 작성 (권한 600)
5. 오너 개인키를 `infra/buzz/secrets/owner-key.txt` 에 저장 (권한 600, git 제외)

> **오너 개인키는 복구 불가입니다.** 출력 즉시 1Password 등에 옮기고 파일은 지우세요.
> `.env` 안의 `BUZZ_RELAY_PRIVATE_KEY`, DB/Redis/S3 비밀번호, `BUZZ_GIT_HOOK_HMAC_SECRET`
> 도 재시작 사이에 **절대 바뀌면 안 됩니다**. 백업 필수.

기동:

```bash
./manage.sh start     # docker compose up -d --wait
./manage.sh health    # /_liveness 확인
./manage.sh status
./manage.sh logs      # 릴레이 로그 팔로우
```

TLS 모드에서는 Caddy 컨테이너가 `--domain` 값으로 인증서를 자동 발급하고
릴레이의 직접 포트 노출은 제거됩니다. 기존에 nginx/ALB 를 앞단에 두고 있다면
`--plain` 으로 부트스트랩해서 3000 포트를 그대로 쓰고 TLS 는 외부에서 종단하세요.

## 4. 팀원 초대

Buzz 는 계정/비밀번호가 아니라 **Nostr 공개키(npub)** 로 사람을 식별합니다.
팀원이 클라이언트를 설치하면 키쌍이 만들어지고, 그 공개키를 관리자가 릴레이 멤버로 등록합니다.

```bash
./manage.sh add-member npub1abc...          # 일반 멤버
./manage.sh add-member <64자리hex> --role admin
./manage.sh list-members
./manage.sh remove-member npub1abc...
```

여러 명을 한 번에 등록할 때는 파일로:

```bash
cat > members.txt <<'EOF'
npub1aaa...   # 김정비
npub1bbb...   # 이설계
EOF
./manage.sh add-members members.txt   # 1초 간격으로 순차 등록
```

> 1초 간격은 멋이 아니라 필수입니다. 멤버 명단은 kind:13534 이벤트 하나로 발행되는데
> 같은 초에 두 건이 겹치면 뒤 항목이 유실될 수 있습니다.

기본 설정은 **닫힌 릴레이**(`BUZZ_REQUIRE_RELAY_MEMBERSHIP=true`)라 명단에 없는 키는
접속해도 아무것도 읽지 못합니다. 사내용으로 이 값을 유지하세요.

## 5. 클라이언트 접속

| 방식 | 접속 |
|---|---|
| 브라우저 | `https://buzz.yourdomain.com` (릴레이 이미지가 웹 번들을 함께 서빙) |
| 데스크톱 앱 | [releases](https://github.com/block/buzz/releases/latest) 에서 macOS `.dmg` / Windows `.exe` / Linux `.AppImage` 받아 설치 |

데스크톱 앱은 기본이 `ws://localhost:3000` 이므로, 실행 전에
`BUZZ_RELAY_URL=wss://buzz.yourdomain.com` 을 설정하거나 앱 안에서 릴레이 주소를 바꿉니다.
Windows 빌드는 코드 서명이 없어 SmartScreen 경고가 뜹니다("추가 정보 → 실행").

관리자 웹 UI 를 쓰려면 `BUZZ_ADMIN_HOST` 에 별도 호스트명(예: `admin.buzz.yourdomain.com`)을
지정해야 합니다. 기본 설치에는 포함하지 않았습니다.

## 6. 모델 인증 — API 키가 꼭 필요한가?

**릴레이(3~5장)까지는 API 키가 전혀 필요 없습니다.** 채널·DM·검색·감사 로그·Git 은
자체 서버에서 도는 오픈소스라 외부 결제와 무관합니다. AI 에이전트를 붙일 때만
모델 제공자가 필요하고, 그것도 선택지가 셋입니다.

| | 방식 | 추가 비용 | 비고 |
|---|---|---|---|
| **A** | **Claude 구독 재사용** (`claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN`) | 없음 (기존 Pro/Max/Team 구독 한도 내) | 브라우저 로그인이 안 되는 서버/컨테이너용 1년짜리 OAuth 토큰. Pro/Max/Team/Enterprise 플랜 필요 |
| **B** | **Anthropic API 키** (`ANTHROPIC_API_KEY`) | 토큰 사용량 과금 | 사용량 통제·팀 분리가 쉬움 |
| **C** | **로컬 모델** (Ollama/vLLM + `buzz-agent`) | 0원 | 외부로 데이터가 안 나감. 대신 GPU/RAM 필요, 품질은 Claude보다 낮음 |
| — | **에이전트 없이 사용** | 0원 | 사람끼리 쓰는 자체 호스팅 팀 채팅 + 감사 로그로만 운영 |

A 방식 준비 (노트북에서 한 번만):

```bash
claude setup-token          # 브라우저 승인 후 토큰이 출력됨 (1년 유효)
```

출력된 토큰을 `agent/.env` 의 `CLAUDE_CODE_OAUTH_TOKEN` 에 넣고 `ANTHROPIC_API_KEY` 는
비워 둡니다. 둘 다 넣으면 **API 키가 우선 적용**되어 과금됩니다.

> 이 토큰은 모델 호출 전용이라 Remote Control 세션이나 claude.ai 커넥터는 쓸 수 없습니다.
> 그리고 저희 쪽 컨테이너에서 실제 기동까지는 검증하지 못했으니, 첫 실행 시
> `docker compose -f compose.agent.yml logs -f` 로 인증이 통과하는지 꼭 확인하세요.
> 인증 오류가 나면 B 방식(API 키)으로 전환하면 됩니다.

C 방식은 `agent/.env` 에서 `BUZZ_ACP_AGENT_COMMAND=buzz-agent` 로 바꾸고 Ollama 주소를
지정합니다(`.env.example` 의 [C] 블록 참고). `buzz-agent` 바이너리는 에이전트 이미지에
함께 빌드되어 있습니다.

### Max 구독으로 돌릴 때 알아둘 것

A 방식은 추가 결제가 없는 대신, **에이전트가 쓰는 만큼 본인 구독 한도에서 빠집니다.**
구독 한도는 5시간 롤링 창 + 주간 창으로 걸리고 Claude 앱·Claude Code와 같은 통을 씁니다.
즉 채널에서 에이전트가 크게 돌면 사장님 본인 작업이 한도에 걸릴 수 있습니다.

또 하나, 이 토큰은 **개인 자격증명 하나**입니다. 팀원 전원이 에이전트를 부르면 그 사용량이
전부 사장님 계정으로 기록됩니다. 팀 단위로 상시 돌릴 계획이라면 B 방식(API 키)으로
분리하는 편이 사용량 추적·통제 면에서 낫습니다.

파일럿 단계 권장 설정 (`agent/.env`):

```bash
BUZZ_ACP_RESPOND_TO=owner-only    # 처음엔 본인만, 익숙해지면 allowlist 로 확대
BUZZ_ACP_AGENTS=1                 # 동시 세션 1개
BUZZ_ACP_HEARTBEAT_INTERVAL=0     # 유휴 시 자동 호출 끔 (켜면 아무도 안 불러도 한도 소모)
BUZZ_ACP_MODEL=                   # Sonnet 계열 지정 시 한도 절약
```

한도에 걸리면 에이전트 응답이 실패합니다. `claude.ai` 의 Settings → Usage 에서
usage credits 를 켜 두면 한도 초과분을 유료로 이어서 쓸 수 있고, 꺼두면 창이 리셋될
때까지 기다리게 됩니다. 어느 쪽이든 사장님이 선택하실 문제라 기본값은 건드리지 않았습니다.

## 7. Claude Code 에이전트 연결

에이전트는 `buzz-acp` 하네스를 통해 붙습니다. 하네스가 릴레이의 @멘션을 듣고 →
ACP 로 Claude 를 호출하고 → Claude 가 `buzz` CLI 로 답장/작업을 수행합니다.

공개 릴레이 이미지에는 `buzz` CLI 와 `buzz-acp` 가 들어있지 않아 소스에서 빌드합니다
(`agent/Dockerfile` 이 그 과정을 담고 있습니다).

```bash
cd infra/buzz/agent

# 1) 에이전트 전용 키쌍 생성 — 사람 계정 키와 반드시 달라야 합니다
docker run --rm --entrypoint /usr/local/bin/buzz-admin \
  ghcr.io/block/buzz:main generate-key

# 2) 공개키를 릴레이 멤버로 등록
cd .. && ./manage.sh add-member <Public key> && cd agent

# 3) 설정
cp .env.example .env
$EDITOR .env          # BUZZ_PRIVATE_KEY(=위 Secret key) + 6장에서 고른 모델 인증값

# 4) 이미지 빌드 (Rust 워크스페이스 컴파일 — 15~40분, 최초 1회)
docker build -t yjt-buzz-agent:latest .

# 5) 기동
docker compose -f compose.agent.yml up -d
docker compose -f compose.agent.yml logs -f
```

그다음 Buzz 클라이언트에서 채널을 만들고 **에이전트를 그 채널의 멤버로 추가**해야 합니다.
이 단계를 빠뜨리면 로그에 `discovered 0 channel(s)` 이 찍히고 에이전트는 모든 멘션을
조용히 무시합니다.

반응 범위는 `.env` 의 `BUZZ_ACP_RESPOND_TO` 로 조절합니다.

| 값 | 동작 |
|---|---|
| `owner-only` (기본) | 등록된 오너의 발언에만 반응 |
| `allowlist` | `BUZZ_ACP_RESPOND_TO_ALLOWLIST` 의 공개키 + 오너 |
| `anyone` | 전원 |
| `nobody` | 인바운드 무시, 하트비트로만 동작 (공지 봇 용도) |

오너는 채널에서 에이전트를 멘션해 `!cancel`(현재 턴 취소), `!rotate`(세션 새로 시작),
`!shutdown`(하네스 종료)을 보낼 수 있습니다.

> **권한 기본값 주의.** `buzz-acp` 의 `BUZZ_ACP_PERMISSION_MODE` 기본값은
> `bypassPermissions` 입니다. 즉 에이전트가 컨테이너 안에서 파일 수정·쉘 실행을
> 확인 없이 수행합니다. 작업 공간은 `/workspace` 볼륨으로 격리돼 있고 호스트 파일은
> 마운트하지 않았지만, 확인 절차를 살리고 싶으면 `agent/.env` 에서 `default` 로 바꾸세요.

## 8. 운영

```bash
./manage.sh upgrade        # 이미지 pull + 재기동 + 백업 체크리스트 출력
./manage.sh backup-hint    # 백업 대상 목록
./manage.sh stop           # 볼륨은 유지한 채 정지
```

정기 백업 대상:

- `~/buzz/deploy/compose/.env` (릴레이 개인키, DB/Redis/S3 시크릿, git HMAC)
- 오너 개인키
- PostgreSQL (`pg_dump` 권장)
- MinIO 버킷(미디어·git 오브젝트), `buzz-git-data` 볼륨
- Caddy `data`/`config` 볼륨

PostgreSQL 스냅샷과 오브젝트/git 스냅샷은 **같은 정지 구간에서** 함께 뜨세요.

이미지 태그는 기본이 `ghcr.io/block/buzz:main` 입니다. 운영에 올릴 때는
`.env` 의 `BUZZ_IMAGE` 를 `:sha-<7자리>` 또는 정식 릴리스 태그로 고정하는 것을 권장합니다.

## 9. 트러블슈팅

| 증상 | 확인 |
|---|---|
| `.env still contains CHANGE_ME` | 부트스트랩 없이 수동 복사한 경우. `./bootstrap.sh --force` 로 재생성 |
| 릴레이가 계속 재시작 | `./manage.sh logs relay` — 대개 DB 마이그레이션(`BUZZ_AUTO_MIGRATE=true` 확인) 또는 시크릿 누락 |
| HTTPS 인증서 발급 실패 | DNS A 레코드 전파 여부, 80/443 방화벽, `./manage.sh logs caddy` |
| 클라이언트는 붙는데 아무것도 안 보임 | 해당 공개키가 멤버 명단에 없음 → `./manage.sh list-members` |
| 에이전트가 멘션에 무반응 | ① 채널 멤버로 추가했는지 ② `BUZZ_ACP_RESPOND_TO` 값 ③ 에이전트 키가 사람 키와 같지 않은지 (자기 이벤트는 무시함) |
| 에이전트가 인증 오류로 죽음 | 6장의 A/B/C 중 하나만 채웠는지 확인. A(구독 토큰)인데 `ANTHROPIC_API_KEY` 가 남아 있으면 API 키가 우선 적용됨. 토큰 만료 시 `claude setup-token` 재발급 |
| 에이전트 빌드가 OOM 으로 죽음 | 메모리 4GB 이하 서버에서 흔함. swap 추가 또는 사양 큰 머신에서 빌드 후 이미지 push |

## 10. 서버 없이 먼저 써보려면

Block 이 Railway 원클릭 배포 템플릿을 제공합니다:
[railway.com/deploy/buzz-relay-block](https://railway.com/deploy/buzz-relay-block)
([설명 글](https://engineering.block.xyz/blog/run-your-own-buzz-relay))

검증용으로는 이쪽이 빠르고, 사내 데이터를 태우는 순간부터는 위의 자체 호스팅을 권장합니다.

## 11. YJT 에서 쓸 만한 시나리오

이 저장소(YJT 스마트 정비 플랫폼)와 Buzz 는 별개 시스템입니다. 굳이 붙인다면:

- **선박/작업지시서 단위 채널** — 정비 건마다 채널을 열고 사진·리포트·승인을 한 로그에 남김
- **재고 알림 봇** — 안전재고 미만 발생 시 채널에 알림
- **문의 접수 알림 / 정비 만기 다이제스트** — 백엔드와 webhook·schedule 로 연동
- **기술 문의 1차 응대 에이전트** — 채널에 붙인 Claude 에이전트가 기존 정비 이력·매뉴얼을 근거로 초안 답변, 담당자가 검토 후 발송
- **감사 추적** — 모든 발언·승인이 서명된 이벤트로 남아 선급/고객 감사 대응에 사용 가능

앞의 3개는 바로 등록할 수 있는 워크플로로 만들어 뒀습니다 → [`workflows/`](workflows/README.md)

```bash
cd infra/buzz/workflows
BUZZ_PRIVATE_KEY=<오너 개인키> ./install.sh <채널UUID> --all
```

다만 Buzz 는 아직 빠르게 움직이는 프로젝트입니다(모바일 클라이언트·워크플로 승인 게이트 등
일부 기능이 진행 중). 사내 커뮤니케이션 전면 이관보다는 **한 팀·한 프로젝트로 파일럿**을
먼저 돌려보길 권합니다.

## 파일 구성

```
infra/buzz/
├── README.md              이 문서
├── bootstrap.sh           소스 클론 + 키/시크릿 생성 + .env 작성
├── manage.sh              기동/정지/로그/헬스체크/멤버 관리 래퍼
├── .gitignore             secrets/, .buzz-env, agent/.env 커밋 차단
├── agent/
│   ├── Dockerfile         buzz-cli + buzz-acp + buzz-agent 빌드, claude-agent-acp 포함
│   ├── compose.agent.yml  에이전트 하네스 실행 정의
│   └── .env.example       에이전트 설정 템플릿
└── workflows/
    ├── README.md          워크플로 등록·연동 가이드
    ├── install.sh         채널에 워크플로 등록
    ├── low-stock-alert.yml
    ├── inquiry-received.yml
    └── daily-pms-digest.yml
```
