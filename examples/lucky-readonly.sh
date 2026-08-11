#!/usr/bin/env sh
set -eu

: "${LUCKY_BASE_URL:?set LUCKY_BASE_URL to the panel URL including its safe entry}"
: "${LUCKY_OPEN_TOKEN:?set LUCKY_OPEN_TOKEN without putting it in this file}"

case "${1:-}" in
  status) endpoint='/api/status' ;;
  info) endpoint='/api/info' ;;
  modules) endpoint='/api/modules/list' ;;
  *)
    echo "usage: $0 {status|info|modules}" >&2
    exit 2
    ;;
esac

curl --fail-with-body --silent --show-error \
  --header "openToken: ${LUCKY_OPEN_TOKEN}" \
  "${LUCKY_BASE_URL%/}${endpoint}"
printf '\n'
