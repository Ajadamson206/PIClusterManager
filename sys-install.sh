#!/usr/bin/env bash
set -euo pipefail

# Install garden-cluster-manager to the system
# Run from project root

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root"
  exit 1
fi

# Variables

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

APP_NAME="garden-cluster"
APP_USER="picos"
APP_GROUP="picos"

APP_DIR="/usr/local/lib/${APP_NAME}"
APP_BIN_DIR="${APP_DIR}/bin"
VENV_DIR="${APP_DIR}/.venv"

ETC_DIR="/etc/garden"
VAR_DIR="/var/lib/garden"
LOG_DIR="/var/log/garden"

SERVICE_FILE="${PROJECT_ROOT}/configurations/cluster-manager.service"

echo "[*] Installing system dependencies..."
# Debian/Raspberry Pi OS:
if command -v apt-get >/dev/null 2>&1; then
  apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y dnsmasq hostapd dhcpcd nftables
else
  echo "Unsupported distro: no apt-get found"
  exit 1
fi

echo "[*] Creating user/group..."
getent group "${APP_GROUP}" >/dev/null || groupadd -r "${APP_GROUP}"
id -u "${APP_USER}" >/dev/null 2>&1 || useradd -r -g "${APP_GROUP}" -s /usr/sbin/nologin -d "${VAR_DIR}" -M "${APP_USER}"

echo "[*] Creating directories..."
install -d -m 0755 /usr/local/bin
install -d -m 0750 -o root -g "${APP_GROUP}" "${ETC_DIR}"
install -d -m 0750 -o "${APP_USER}" -g "${APP_GROUP}" "${APP_DIR}"
install -d -m 0750 -o "${APP_USER}" -g "${APP_GROUP}" "${APP_BIN_DIR}"
install -d -m 0750 -o "${APP_USER}" -g "${APP_GROUP}" "${VAR_DIR}"
install -d -m 0750 -o "${APP_USER}" -g "${APP_GROUP}" "${LOG_DIR}"

echo "[*] Installing application code..."
# safer than mv; preserves perms; doesn't delete source
rsync -a --delete "${PROJECT_ROOT}/src/" "${APP_DIR}/src/"
chown -R "${APP_USER}:${APP_GROUP}" "${APP_DIR}"

echo "[*] Installing config..."
install -m 0640 -o root -g "${APP_GROUP}" \
  "${PROJECT_ROOT}/configurations/garden-cluster-config.json" \
  "${ETC_DIR}/garden-cluster-config.json"

echo "[*] Installing service launcher..."
install -m 0750 -o root -g root \
  "${PROJECT_ROOT}/configurations/garden-cluster-manager" \
  "${APP_BIN_DIR}/garden-cluster-manager"

ln -sf "${APP_BIN_DIR}/garden-cluster-manager" /usr/local/bin/garden-cluster-manager

echo "[*] Creating/Updating venv..."
python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/pip" install --upgrade pip wheel
"${VENV_DIR}/bin/pip" install -r "${PROJECT_ROOT}/requirements.txt"

echo "[*] Installing systemd unit..."
install -m 0644 "${SERVICE_FILE}" /etc/systemd/system/${APP_NAME}.service
systemctl daemon-reload
systemctl enable --now "${APP_NAME}.service"

echo "[+] Done. Check logs with:"
echo "    journalctl -u ${APP_NAME}.service -f"
