#!/usr/bin/env bash
# 워크플로 YAML 을 Buzz 채널에 등록한다.
#
# 릴레이 호스트에는 `buzz` CLI 가 없으므로(공개 릴레이 이미지에 미포함),
# 에이전트 이미지(yjt-buzz-agent) 안의 CLI 를 일회성 컨테이너로 빌려 쓴다.
#
# 사전 조건:
#   1) 릴레이 기동   : ../manage.sh start
#   2) 에이전트 이미지 빌드: docker build -t yjt-buzz-agent:latest ../agent
#   3) 채널 생성 후 그 UUID 확보 (데스크톱/웹 클라이언트에서 확인)
#   4) 오너 개인키 준비 — call_webhook 이 있는 워크플로는 owner/admin 권한 필요
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE="${AGENT_IMAGE:-yjt-buzz-agent:latest}"
NETWORK="${BUZZ_NETWORK:-buzz-prod_buzz-net}"
RELAY_URL="${BUZZ_RELAY_URL:-http://relay:3000}"

usage() {
  cat <<'MSG'
사용법:
  BUZZ_PRIVATE_KEY=<오너 개인키> ./install.sh <채널UUID> <워크플로.yml> [...]
  BUZZ_PRIVATE_KEY=<오너 개인키> ./install.sh <채널UUID> --all
  BUZZ_PRIVATE_KEY=<오너 개인키> ./install.sh --list <채널UUID>

환경변수:
  BUZZ_PRIVATE_KEY  (필수) 워크플로 소유자가 될 신원의 개인키
  BUZZ_RELAY_URL    기본 http://relay:3000  (CLI 는 http/https, 하네스만 ws)
  BUZZ_NETWORK      기본 buzz-prod_buzz-net
  AGENT_IMAGE       기본 yjt-buzz-agent:latest

webhook 트리거 워크플로는 등록 응답에 webhook_secret 이 한 번만 나옵니다.
그 값을 백엔드에 저장하고, 호출 시 X-Webhook-Secret 헤더로 보내세요.
MSG
}

buzz_cli() {
  docker run --rm -i \
    --network "${NETWORK}" \
    -e BUZZ_PRIVATE_KEY \
    -e BUZZ_RELAY_URL="${RELAY_URL}" \
    --entrypoint buzz \
    "${IMAGE}" "$@"
}

[[ $# -ge 1 ]] || { usage; exit 1; }

if [[ "$1" == "-h" || "$1" == "--help" ]]; then usage; exit 0; fi

: "${BUZZ_PRIVATE_KEY:?BUZZ_PRIVATE_KEY 를 설정하세요 (워크플로 소유자 신원)}"
export BUZZ_PRIVATE_KEY

if [[ "$1" == "--list" ]]; then
  channel="${2:?사용법: ./install.sh --list <채널UUID>}"
  buzz_cli workflows list --channel "${channel}"
  exit 0
fi

CHANNEL="$1"; shift
[[ $# -ge 1 ]] || { usage; exit 1; }

if [[ "$1" == "--all" ]]; then
  set -- "${SCRIPT_DIR}"/*.yml
fi

for file in "$@"; do
  [[ -f "${file}" ]] || { echo "건너뜀 (파일 없음): ${file}" >&2; continue; }
  echo "==> 등록: $(basename "${file}")"
  # --yaml - 은 stdin 에서 정의를 읽는다.
  buzz_cli workflows create --channel "${CHANNEL}" --yaml - < "${file}"
  echo
done

cat <<'MSG'
등록이 끝났습니다.

  · 등록 목록 확인 : ./install.sh --list <채널UUID>
  · webhook 호출   : POST https://<도메인>/hooks/<workflow_id>
                     헤더 X-Webhook-Secret: <등록 응답의 webhook_secret>
                     본문 application/json (키는 {{trigger.<키>}} 로 참조)
MSG
