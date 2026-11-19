#!/usr/bin/env bash
# Stellt den Mailversand des Clubs auf Zoho (eigene Domain) um. Das Passwort wird verdeckt abgefragt und nur in .env geschrieben.
# Aufruf auf dem Server: bash deploy/set-smtp.sh [absender@domain] [smtp-host]
set -euo pipefail
cd "$(dirname "$0")/.."

SENDER="${1:-info@andrii-it.de}"
HOST="${2:-smtp.zoho.eu}"
read -r -s -p "App-Passwort für ${SENDER} (Eingabe bleibt unsichtbar): " PASSWORD
echo
[ -n "$PASSWORD" ] || { echo "Kein Passwort eingegeben, Abbruch."; exit 1; }

cp .env ".env.bak-pre-smtp-$(date +%Y%m%d%H%M%S)"
set_var() {  # set_var NAME WERT: ersetzt die Zeile oder hängt sie an; Wert wird nicht als sed-Muster gedeutet
  local name="$1" value="$2" tmp
  tmp="$(mktemp)"
  grep -v "^${name}=" .env > "$tmp" || true
  printf '%s=%s\n' "$name" "$value" >> "$tmp"
  cat "$tmp" > .env && rm -f "$tmp"
}
set_var SMTP_HOST "$HOST"
set_var SMTP_PORT 587
set_var SMTP_TLS 1
set_var SMTP_USER "$SENDER"
set_var SMTP_PASSWORD "$PASSWORD"
set_var SMTP_FROM "$SENDER"
unset PASSWORD

docker compose up -d app scheduler
echo "Fertig: Versand über ${HOST} als ${SENDER}."
