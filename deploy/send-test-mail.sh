#!/usr/bin/env bash
# Schickt eine Testmail über den eingestellten SMTP-Server. Aufruf auf dem Server: bash deploy/send-test-mail.sh adresse@beispiel.de
set -euo pipefail
cd "$(dirname "$0")/.."
[ $# -eq 1 ] || { echo "Aufruf: $0 adresse@beispiel.de"; exit 1; }
docker compose exec -T -e TEST_TO="$1" app python - <<'PY'
import os
from app import create_app
app = create_app()
with app.app_context():
    from app.services.mailer import send_mail
    ok = send_mail(os.environ["TEST_TO"], "Club UA: Testmail", "Testmail vom Club-Server.")
    print("Gesendet" if ok else "FEHLER: Versand fehlgeschlagen (Log: docker compose logs app)")
PY
