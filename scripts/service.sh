#!/usr/bin/env bash
# data_agent service manager — start | stop | restart | status
#
# Default start runs backend + frontend in the background (daemon).
# Foreground dev mode: ./scripts/service.sh start --foreground  (alias: -f)
#
# Environment (optional):
#   DATA_AGENT_BACKEND_PORT   default 8000
#   DATA_AGENT_FRONTEND_PORT  default 6641
#   DATA_AGENT_HOST           default 0.0.0.0
#   DATA_AGENT_BACKEND_URL    default http://127.0.0.1:${BACKEND_PORT}
#   DATA_AGENT_PID_DIR        default /tmp/data_agent
#   DATA_AGENT_LOG_DIR        default /tmp/data_agent
#   DATA_AGENT_FRONTEND_MODE  dev (default) or prod
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

BACKEND_PORT="${DATA_AGENT_BACKEND_PORT:-8000}"
FRONTEND_PORT="${DATA_AGENT_FRONTEND_PORT:-6641}"
BACKEND_HOST="${DATA_AGENT_HOST:-0.0.0.0}"
BACKEND_URL="${DATA_AGENT_BACKEND_URL:-http://127.0.0.1:${BACKEND_PORT}}"
PID_DIR="${DATA_AGENT_PID_DIR:-/tmp/data_agent}"
LOG_DIR="${DATA_AGENT_LOG_DIR:-/tmp/data_agent}"
PUBLIC_URL="${DATA_AGENT_PUBLIC_URL:-http://bigdatauatgpu3.synnex.org:${FRONTEND_PORT}}"

BACK_PID=""
FRONT_PID=""

usage() {
  cat <<EOF
Usage: $(basename "$0") <command> [options]

Commands:
  start [--foreground|-f]   Start backend + frontend (daemon by default)
  stop                      Stop running services
  restart [--foreground|-f] Stop then start
  status                    Show process and health status

Examples:
  $(basename "$0") start              # background (daemon)
  $(basename "$0") start --foreground # dev mode, logs in terminal, Ctrl+C stops
  $(basename "$0") restart
  $(basename "$0") status
EOF
}

init_runtime() {
  if [[ ! -d .venv ]]; then
    echo "Missing .venv — run ./scripts/setup.sh first." >&2
    exit 1
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate

  export NVM_DIR="${NVM_DIR:-$ROOT/.nvm}"
  if [[ -s "$NVM_DIR/nvm.sh" ]]; then
    # shellcheck disable=SC1091
    . "$NVM_DIR/nvm.sh"
    nvm use 22 >/dev/null 2>&1 || true
  fi
  if [[ -d "$NVM_DIR/versions/node" ]]; then
    local node_bin
    node_bin="$(find "$NVM_DIR/versions/node" -maxdepth 2 -type f -name node | sort | tail -1)"
    if [[ -n "$node_bin" ]]; then
      export PATH="$(dirname "$node_bin"):$PATH"
    fi
  fi
}

load_dotenv_for_shell() {
  if [[ -f "$ROOT/.env" ]]; then
    set -a
    # shellcheck disable=SC1091
    source "$ROOT/.env"
    set +a
  fi
}

stop_pid_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    local pid
    pid="$(cat "$file")"
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
      sleep 1
      kill -9 "$pid" 2>/dev/null || true
    fi
    rm -f "$file"
  fi
}

cmd_stop() {
  init_runtime
  echo "Stopping data_agent services…"
  stop_pid_file "$PID_DIR/backend.pid"
  stop_pid_file "$PID_DIR/frontend.pid"
  pkill -f "uvicorn app.main:app --host .* --port ${BACKEND_PORT}" 2>/dev/null || true
  pkill -f "next dev -H .* -p ${FRONTEND_PORT}" 2>/dev/null || true
  pkill -f "next start -H .* -p ${FRONTEND_PORT}" 2>/dev/null || true
  sleep 1
  echo "Stopped."
}

pid_alive() {
  local pid="$1"
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

check_backend_health() {
  curl -sf --connect-timeout 5 "http://127.0.0.1:${BACKEND_PORT}/health" >/dev/null 2>&1
}

check_frontend_health() {
  curl -sf --connect-timeout 10 "http://127.0.0.1:${FRONTEND_PORT}/" >/dev/null 2>&1
}

print_component_status() {
  local name="$1"
  local pid_file="$2"
  local health_fn="$3"
  local log_file="$4"

  local pid=""
  [[ -f "$pid_file" ]] && pid="$(cat "$pid_file" 2>/dev/null || true)"

  local proc="stopped"
  local health="down"
  if pid_alive "$pid"; then
    proc="running (pid $pid)"
    if "$health_fn"; then
      health="ok"
    else
      health="unhealthy"
    fi
  elif "$health_fn"; then
    proc="running (no pid file)"
    health="ok"
  fi

  printf "  %-9s %-28s health: %s\n" "$name" "$proc" "$health"
  if [[ -f "$log_file" ]]; then
    printf "            log: %s\n" "$log_file"
  fi
}

cmd_status() {
  init_runtime
  mkdir -p "$PID_DIR" "$LOG_DIR"

  echo "data_agent status"
  echo "  backend  port ${BACKEND_PORT}"
  echo "  frontend port ${FRONTEND_PORT}"
  echo "  url      ${PUBLIC_URL}"
  echo ""
  print_component_status "backend" "$PID_DIR/backend.pid" check_backend_health "$LOG_DIR/backend.log"
  print_component_status "frontend" "$PID_DIR/frontend.pid" check_frontend_health "$LOG_DIR/frontend.log"
}

start_backend_daemon() {
  (
    cd backend
    unset DATA_AGENT_RECURSION_LIMIT
    export PYTHONPATH=.
    nohup uvicorn app.main:app --host "$BACKEND_HOST" --port "$BACKEND_PORT" \
      >"$LOG_DIR/backend.log" 2>&1 &
    echo $! >"$PID_DIR/backend.pid"
  )
}

start_frontend_daemon() {
  (
    cd frontend
    export DATA_AGENT_BACKEND_URL="$BACKEND_URL"
    if [[ "${DATA_AGENT_FRONTEND_MODE:-dev}" == "prod" ]] && [[ -d .next ]]; then
      nohup npx next start -H 0.0.0.0 -p "$FRONTEND_PORT" \
        >"$LOG_DIR/frontend.log" 2>&1 &
    else
      nohup npx next dev -H 0.0.0.0 -p "$FRONTEND_PORT" \
        >"$LOG_DIR/frontend.log" 2>&1 &
    fi
    echo $! >"$PID_DIR/frontend.pid"
  )
}

cmd_start_daemon() {
  init_runtime
  mkdir -p "$PID_DIR" "$LOG_DIR"

  cmd_stop

  echo "Starting backend on ${BACKEND_HOST}:${BACKEND_PORT}…"
  start_backend_daemon

  echo "Starting frontend on 0.0.0.0:${FRONTEND_PORT}…"
  start_frontend_daemon

  sleep 4
  if check_backend_health; then
    echo "Backend OK"
  else
    echo "Backend FAILED — see $LOG_DIR/backend.log" >&2
    tail -20 "$LOG_DIR/backend.log" || true
    exit 1
  fi

  if check_frontend_health; then
    echo "Frontend OK"
  else
    echo "Frontend FAILED — see $LOG_DIR/frontend.log" >&2
    tail -20 "$LOG_DIR/frontend.log" || true
    exit 1
  fi

  echo "Ready: ${PUBLIC_URL}"
  echo "Logs: $LOG_DIR/backend.log $LOG_DIR/frontend.log"
  echo "PIDs: $(cat "$PID_DIR/backend.pid") $(cat "$PID_DIR/frontend.pid")"
}

foreground_cleanup() {
  echo ""
  echo "Shutting down…"
  [[ -n "${BACK_PID:-}" ]] && kill "$BACK_PID" 2>/dev/null || true
  [[ -n "${FRONT_PID:-}" ]] && kill "$FRONT_PID" 2>/dev/null || true
}

cmd_start_foreground() {
  init_runtime
  load_dotenv_for_shell
  trap foreground_cleanup EXIT INT TERM

  echo "==> Backend  http://${BACKEND_HOST}:${BACKEND_PORT}  (docs: /docs)"
  (
    cd backend
    PYTHONPATH=. uvicorn app.main:app --host "$BACKEND_HOST" --port "$BACKEND_PORT" --reload
  ) &
  BACK_PID=$!

  echo "==> Frontend http://0.0.0.0:${FRONTEND_PORT}"
  (
    cd frontend
    npx next dev -H 0.0.0.0 -p "$FRONTEND_PORT"
  ) &
  FRONT_PID=$!

  echo "PIDs: backend=$BACK_PID frontend=$FRONT_PID"
  echo "Open: ${PUBLIC_URL}"
  echo "Press Ctrl+C to stop."
  wait
}

parse_foreground_flag() {
  FOREGROUND=false
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --foreground | -f)
        FOREGROUND=true
        shift
        ;;
      -h | --help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown option: $1" >&2
        usage >&2
        exit 1
        ;;
    esac
  done
}

cmd_start() {
  parse_foreground_flag "$@"
  if [[ "$FOREGROUND" == true ]]; then
    cmd_start_foreground
  else
    cmd_start_daemon
  fi
}

cmd_restart() {
  parse_foreground_flag "$@"
  cmd_stop
  if [[ "$FOREGROUND" == true ]]; then
    cmd_start_foreground
  else
    cmd_start_daemon
  fi
}

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    start)
      cmd_start "$@"
      ;;
    stop)
      cmd_stop
      ;;
    restart)
      cmd_restart "$@"
      ;;
    status)
      cmd_status
      ;;
    -h | --help | help | "")
      usage
      [[ -z "$cmd" ]] && exit 1
      ;;
    *)
      echo "Unknown command: $cmd" >&2
      usage >&2
      exit 1
      ;;
  esac
}

main "$@"
