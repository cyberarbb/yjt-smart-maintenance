# YJT 파일럿 워크플로

Buzz 채널에 등록해서 쓰는 워크플로 정의입니다. 배포 직후 채널이 비어 있지 않도록
YJT 업무에 바로 붙는 3개를 준비했습니다.

| 파일 | 트리거 | 하는 일 |
|---|---|---|
| `low-stock-alert.yml` | webhook | 백엔드가 감지한 안전재고 미만 부품을 채널에 게시 |
| `inquiry-received.yml` | webhook | 신규 기술문의 접수 카드를 채널에 게시 |
| `daily-pms-digest.yml` | schedule (매일 08:00 KST) | 백엔드에서 만기 도래 정비 목록을 가져와 게시 |

세 파일 모두 Buzz의 실제 워크플로 파서(`buzz_workflow::parse_yaml`)로 파싱·검증을
통과시켰고, `daily-pms-digest.yml` 의 조건식은 evalexpr 로 200/500 두 경우를
평가해 확인했습니다.

여기에 더해 **소스 빌드한 릴레이에 실제로 등록해 돌려봤습니다**:

- 세 정의 모두 등록 성공, webhook 트리거 2종은 `webhook_secret` 발급 확인
  (`schedule` 트리거인 다이제스트에는 시크릿이 나오지 않습니다 — 정상)
- `low-stock-alert` 에 실제 POST → 채널에 아래 메시지가 게시됨(템플릿 치환 정상):

  ```
  ⚠️ **안전재고 미만** — MAN MAN-TCR18-COMP

  · 품명: 컴프레서 휠
  · 현재고: 2 / 안전재고: 5
  · 창고: 부산창고
  ```

- 잘못된 시크릿으로 호출 시 **HTTP 401** 로 거부
- 정상 호출 응답: `{"run_id":"...","status":"pending","workflow_id":"..."}`

> **주의.** webhook 호출과 CLI 접속은 모두 `.env` 의 `RELAY_URL` 과 **같은 호스트명**을
> 써야 합니다. 릴레이가 Host 헤더로 커뮤니티를 식별하기 때문에 IP 로 붙으면
> `no community is configured for this host` (404) 가 납니다.

## 등록

```bash
# 사전: 릴레이 기동 + 에이전트 이미지 빌드 + 채널 생성(UUID 확보)
cd infra/buzz/workflows

BUZZ_PRIVATE_KEY=<오너 개인키> ./install.sh <채널UUID> --all
BUZZ_PRIVATE_KEY=<오너 개인키> ./install.sh --list <채널UUID>
```

릴레이 이미지에는 `buzz` CLI 가 없어서, `install.sh` 는 에이전트 이미지 안의 CLI 를
일회성 컨테이너로 빌려 씁니다(별도 설치 불필요).

> `call_webhook` 이 들어간 워크플로(`daily-pms-digest.yml`)는 **채널 owner/admin
> 권한**으로만 저장·실행됩니다. 채널 내용을 외부로 내보낼 수 있는 액션이라
> 일반 멤버 권한으로는 막혀 있습니다.

## webhook 트리거 연동

등록 응답에 `webhook_secret` 이 **한 번만** 나옵니다. 그 값을 백엔드 환경변수로
저장하세요. 이후 호출:

```
POST https://buzz.yourdomain.com/hooks/<workflow_id>
X-Webhook-Secret: <webhook_secret>
Content-Type: application/json

{"part_number": "MAN-TCR18-COMP", "quantity": "2", ...}
```

본문 JSON 의 각 키는 워크플로 안에서 `{{trigger.<키>}}` 로 참조됩니다. 값은 모두
문자열로 변환되므로, 조건 비교가 필요하면 `trigger_quantity == "0"` 처럼 문자열로
비교하거나 판단 자체를 백엔드에서 하고 결과만 보내는 편이 안전합니다.

FastAPI 쪽 호출 예 (기존 `notification_service` 에 얹으면 됩니다):

```python
import httpx

BUZZ_HOOK_URL = os.environ["BUZZ_LOW_STOCK_HOOK_URL"]      # .../hooks/<workflow_id>
BUZZ_HOOK_SECRET = os.environ["BUZZ_LOW_STOCK_HOOK_SECRET"]

async def notify_low_stock(item) -> None:
    payload = {
        "part_number": item.part.part_number,
        "name": item.part.name,
        "brand": item.part.brand.value,
        "quantity": str(item.quantity),
        "min_quantity": str(item.min_quantity),
        "warehouse": item.warehouse,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            BUZZ_HOOK_URL,
            json=payload,
            headers={"X-Webhook-Secret": BUZZ_HOOK_SECRET},
        )
        resp.raise_for_status()
```

## schedule 트리거 주의사항

- **cron 은 UTC 기준**입니다. `0 23 * * *` = 한국시간 08:00. 5필드 표준 cron 을 쓰면
  릴레이가 초/연도 필드를 채워서 해석합니다.
- `call_webhook` 대상은 **공인 주소**여야 합니다. 릴레이가 SSRF 방지를 위해 사설·예약
  IP 로 해석되는 호스트를 차단하므로 사내 IP나 localhost 는 쓸 수 없습니다.
  YJT 백엔드가 Render 같은 공개 도메인에 있으면 그대로 됩니다.
- 리다이렉트는 따라가지 않고, 응답 본문에는 크기 상한이 있습니다. 백엔드가 사람이
  읽을 텍스트를 짧게 만들어 돌려주는 형태가 가장 잘 맞습니다.

`daily-pms-digest.yml` 은 `YOUR-BACKEND-DOMAIN` 과 `REPLACE_WITH_BACKEND_TOKEN`
자리표시자를 쓰고 있으니 등록 전에 실제 값으로 바꾸세요. 백엔드에
`/api/maintenance/due-digest` 엔드포인트는 아직 없습니다 — 이 워크플로가 기대하는
계약(GET → 사람이 읽는 텍스트 응답)에 맞춰 추가하시면 됩니다.

## 사용 가능한 트리거·액션 (참고)

| 트리거 | 설명 |
|---|---|
| `message_posted` | 채널에 메시지 게시 (evalexpr `filter` 지원) |
| `reaction_added` | 이모지 반응 (특정 `emoji` 지정 가능) |
| `diff_posted` | diff 메시지 게시 |
| `schedule` | `cron` 또는 `interval`(최소 60s) — 둘 중 하나만 |
| `webhook` | `POST /hooks/<workflow_id>` |

| 액션 | 설명 |
|---|---|
| `send_message` | 채널에 메시지 게시 (`channel` 로 다른 채널 지정 가능) |
| `send_dm` | DM 발송 |
| `set_channel_topic` | 채널 토픽 변경 |
| `add_reaction` | 트리거 메시지에 반응 추가 |
| `call_webhook` | 외부 HTTP 호출 (owner/admin 권한 필요, 출력: `status`/`body`) |
| `request_approval` | 승인 대기 (기본 24h) |
| `delay` | 지연 |

템플릿 변수: `{{trigger.text}}`, `{{trigger.author}}`, `{{trigger.channel_id}}`,
`{{trigger.timestamp}}`, `{{trigger.emoji}}`, `{{trigger.message_id}}`,
webhook 본문의 임의 키 `{{trigger.<키>}}`, 앞 단계 출력 `{{steps.<id>.output.<필드>}}`.
조건식(`if`)에서는 밑줄 형태(`trigger_text`, `steps_<id>_output_<필드>`)를 씁니다.
