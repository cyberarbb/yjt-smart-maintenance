#!/usr/bin/env bash
# Buzz 릴레이 운영 래퍼.
#
# 업스트림 deploy/compose/run.sh 를 감싸서 (1) TLS 오버레이 적용 여부를 상태
# 파일에서 자동으로 판단하고, (2) 헬스체크/멤버 일괄 등록처럼 자주 쓰는 작업을
# 한 줄로 처리한다. bootstrap.sh 를 먼저 실행해야 한다.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_FILE="${SCRIPT_DIR}/.buzz-env"

if [[ ! -f "${STATE_FILE}" ]]; then
  echo "오류: ${STATE_FILE} 이 없습니다. 먼저 ./bootstrap.sh 를 실행하세요." >&2
  exit 1
fi
# shellcheck disable=SC1090
source "${STATE_FILE}"

COMPOSE_DIR="${BUZZ_SRC}/deploy/compose"
[[ -d "${COMPOSE_DIR}" ]] || { echo "오류: ${COMPOSE_DIR} 을 찾을 수 없습니다." >&2; exit 1; }

if [[ "${BUZZ_MODE}" == "tls" ]]; then
  export BUZZ_COMPOSE_TLS=true
fi

run_sh() { (cd "${COMPOSE_DIR}" && ./run.sh "$@"); }

http_port() {
  awk -F= '/^BUZZ_HTTP_PORT=/ {print $2; exit}' "${COMPOSE_DIR}/.env" 2>/dev/null || true
}

usage() {
  cat <<'MSG'
사용법: ./manage.sh <명령> [인자]

기동/운영
  start | stop | restart      릴레이 스택 기동 / 정지 / 릴레이만 재생성
  status                      컨테이너 상태
  logs [service]              로그 팔로우 (기본: relay)
  upgrade                     이미지 pull 후 재기동 + 백업 체크리스트 출력
  config                      머지된 compose 설정 확인 (기동 전 검증용)
  health                      /_liveness 확인
  backup-hint                 백업 대상 목록

멤버 관리 (릴레이가 떠 있어야 함)
  add-member <npub|hex> [--role member|admin]
  remove-member <npub|hex> [--role member|admin]
  list-members
  add-members <file>          한 줄에 한 명씩 적힌 파일을 순차 등록
                              (# 주석/빈 줄 무시, 1초 간격 — 같은 초 충돌 방지)

기타
  owner-pubkey                현재 설정된 오너 공개키 출력
  compose <args...>           deploy/compose/run.sh 로 그대로 전달
MSG
}

cmd="${1:-help}"
shift || true

case "${cmd}" in
  start|stop|restart|status|ps|pull|upgrade|config|backup-hint|logs)
    run_sh "${cmd}" "$@"
    ;;

  health)
    if [[ "${BUZZ_MODE}" == "tls" ]]; then
      # TLS 모드에서는 Caddy 오버레이가 relay 의 직접 포트 노출을 제거하므로
      # 공개 도메인으로 확인한다.
      url="https://${BUZZ_DOMAIN}/_liveness"
    else
      port="$(http_port)"
      port="${port:-3000}"
      url="http://127.0.0.1:${port}/_liveness"
    fi
    echo "GET ${url}"
    if curl -fsS "${url}"; then
      echo
      echo "OK — 릴레이가 응답합니다. 클라이언트 접속 주소: ${BUZZ_RELAY_URL}"
    else
      echo "실패 — ./manage.sh logs relay 로 원인을 확인하세요." >&2
      exit 1
    fi
    ;;

  add-member|remove-member|list-members)
    run_sh "${cmd}" "$@"
    ;;

  add-members)
    file="${1:?사용법: ./manage.sh add-members <file>}"
    [[ -f "${file}" ]] || { echo "오류: ${file} 을 찾을 수 없습니다." >&2; exit 1; }
    count=0
    while IFS= read -r line || [[ -n "${line}" ]]; do
      key="$(echo "${line}" | sed 's/#.*//' | tr -d '[:space:]')"
      [[ -n "${key}" ]] || continue
      echo "--> add-member ${key}"
      run_sh add-member "${key}"
      count=$((count + 1))
      # kind:13534 로스터 이벤트가 같은 초에 겹치면 뒤 항목이 무시될 수 있음.
      sleep 1
    done < "${file}"
    echo "총 ${count}명 등록 요청 완료. ./manage.sh list-members 로 확인하세요."
    ;;

  owner-pubkey)
    awk -F= '/^RELAY_OWNER_PUBKEY=/ {print $2; exit}' "${COMPOSE_DIR}/.env"
    ;;

  compose)
    run_sh "$@"
    ;;

  help|-h|--help)
    usage
    ;;

  *)
    echo "알 수 없는 명령: ${cmd}" >&2
    usage >&2
    exit 1
    ;;
esac
