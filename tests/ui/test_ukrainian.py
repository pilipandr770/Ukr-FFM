"""Ukrainian UI and locale boundaries; no database or network required."""
from pathlib import Path
import re
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from babel.messages.pofile import read_po
from flask_babel import force_locale, gettext, ngettext

from app import create_app
from app.i18n import select_locale
from app.i18n_labels import display_label
from app.services.matching import _template_text, fit_label
from config.plans import PLANS


@pytest.fixture()
def app():
    return create_app("test")


@pytest.mark.parametrize("locale", ["de", "uk"])
def test_catalogs_are_complete_and_formats_are_valid(locale):
    root = Path(__file__).resolve().parents[2]
    with (root / "translations/messages.pot").open("rb") as f:
        template = read_po(f)
    with (root / f"translations/{locale}/LC_MESSAGES/messages.po").open("rb") as f:
        catalog = read_po(f, locale=locale)
    assert not catalog.fuzzy
    for message in template:
        if not message.id:
            continue
        translation = catalog.get(message.id)
        assert translation and translation.string and not translation.fuzzy, message.id
        assert not list(translation.check(catalog)), message.id
        if isinstance(message.id, tuple):
            assert len(translation.string) == (3 if locale == "uk" else 2)
            assert all(translation.string)


@pytest.mark.parametrize("path,expected,status", [
    ("/", "Знайдіть людей", 200),
    ("/login", "Увійти", 200),
    ("/register", "Створити обліковий запис", 200),
    ("/missing-page", "404", 404),
])
def test_public_pages_in_ukrainian(app, path, expected, status):
    response = app.test_client().get(path, headers={"Accept-Language": "uk-UA,uk;q=0.9,de;q=0.5"})
    body = response.get_data(as_text=True)
    assert response.status_code == status
    assert '<html lang="uk">' in body
    assert expected in body
    assert '<option value="uk" lang="uk" selected>' in body
    assert "'unsafe-inline'" not in response.headers["Content-Security-Policy"]


@pytest.mark.parametrize("next_url,expected", [
    ("/login?next=%2Fapp%2F", "/login?next=%2Fapp%2F"),
    ("https://example.com", "/"), ("//example.com", "/"),
    ("/\\example.com", "/"), ("/\nexample.com", "/"),
])
def test_language_cookie_and_safe_redirect(app, next_url, expected):
    client = app.test_client()
    response = client.post("/language", data={"locale": "uk", "next": next_url})
    assert response.status_code == 303
    assert response.headers["Location"] == expected
    cookie = response.headers["Set-Cookie"]
    assert "HttpOnly" in cookie and "SameSite=Lax" in cookie
    assert '<html lang="uk">' in client.get("/", headers={"Accept-Language": "de"}).text
    client.post("/language", data={"locale": "de"})
    assert '<html lang="de">' in client.get("/", headers={"Accept-Language": "uk"}).text


def test_invalid_language_changes_nothing(app):
    client = app.test_client()
    client.post("/language", data={"locale": "uk"})
    assert client.post("/language", data={"locale": "xx"}).status_code == 400
    assert '<html lang="uk">' in client.get("/").text
    assert client.get("/language").status_code == 405


def test_language_post_requires_csrf(app):
    app.config["WTF_CSRF_ENABLED"] = True
    client = app.test_client()
    assert client.post("/language", data={"locale": "uk"}).status_code == 400
    page = client.get("/").text
    token = re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)
    assert client.post("/language", data={"locale": "uk", "csrf_token": token}).status_code == 303


def test_language_is_saved_to_authenticated_profile(app, monkeypatch):
    import app.blueprints.public as public
    from app.extensions import db
    user = SimpleNamespace(is_authenticated=True, locale="de")
    monkeypatch.setattr(public, "current_user", user)
    commit = Mock()
    monkeypatch.setattr(db.session, "commit", commit)
    assert app.test_client().post("/language", data={"locale": "uk"}).status_code == 303
    assert user.locale == "uk"
    commit.assert_called_once()


def test_profile_locale_wins_over_cookie_and_browser(app, monkeypatch):
    import app.i18n as i18n
    monkeypatch.setattr(i18n, "current_user", SimpleNamespace(locale="uk"))
    with app.test_request_context("/", headers={"Cookie": "locale=de", "Accept-Language": "de"}):
        assert select_locale() == "uk"


def test_ukrainian_plural_forms_and_dynamic_labels(app):
    with app.test_request_context("/"), force_locale("uk"):
        for number,expected in [(1,"1 учасник"),(2,"2 учасники"),(5,"5 учасників"),
                                (11,"11 учасників"),(21,"21 учасник"),(22,"22 учасники"),(25,"25 учасників")]:
            assert ngettext("%(num)d member", "%(num)d members", number) == expected
        assert str(PLANS["guest"]["name"]) == "Гість"
        assert display_label("travel_operator") == "Туроператор"
        assert display_label("Zivilrecht") == "Цивільне право"
        assert display_label("mittel") == "Середній"
        assert fit_label(.5) == "Добре підходить"
        assert fit_label(.3) == "Частково підходить"
        assert fit_label(.01) == "Мало спільного"
        need = SimpleNamespace(q_looking_for="Дизайнер", q_challenge="")
        offer = SimpleNamespace(q_can_help="Дизайн сайтів", q_focus="")
        assert _template_text(need, offer) == "Потреба: Дизайнер — пропозиція: Дизайн сайтів."


def test_confirmation_email_uses_recipients_language(app, monkeypatch):
    import app.blueprints.auth as auth
    sent = Mock()
    monkeypatch.setattr(auth, "send_mail", sent)
    monkeypatch.setattr(auth, "make_email_token", lambda user: "test-token")
    with app.test_request_context("/"), force_locale("de"):
        auth.send_confirmation(SimpleNamespace(email="member@example.test", locale="uk"))
    assert sent.call_args.args[1] == "Підтвердьте адресу електронної пошти"
    assert "Відкрийте це посилання" in sent.call_args.args[2]


def test_tool_findings_and_fallback_report_are_ukrainian(app, monkeypatch):
    from app.services.tools import seo, common
    response = SimpleNamespace(status_code=200, headers={"Content-Type": "text/html"}, encoding="utf-8")
    monkeypatch.setattr(seo, "_get", lambda url, **kwargs: (response, b'<html lang="de"><title>Test</title><h1>Test</h1></html>', .1, url))
    with app.test_request_context("/"), force_locale("uk"):
        result = seo.analyze("https://example.test", [])
        assert result["findings"][0]["title"] == "Захищене з'єднання (HTTPS)"
        assert result["findings"][0]["cat"] == "Технічна частина"
        report = common._fallback_report(result)
        assert report["zusammenfassung"].startswith("Результат перевірки:")
        assert "Виконайте дії" in report["naechste_schritte"]


def test_generated_report_prompt_uses_selected_language(app, monkeypatch):
    from app.services.tools import common
    complete = Mock(return_value='{"message": "готово"}')
    monkeypatch.setattr(common.llm, "complete", complete)
    with app.test_request_context("/"), force_locale("uk"):
        assert common.json_from_llm("Write German", {}) == {"message": "готово"}
    assert "Ukrainian" in complete.call_args.args[0]
    assert "JSON keys" in complete.call_args.args[0]

def test_parallel_security_checks_keep_ukrainian_locale(app, monkeypatch):
    from app.services.tools import security_extra as extra
    from flask_babel import get_locale
    observed = []
    def finding(*args):
        observed.append(str(get_locale()))
        return []
    for name in ("header_findings", "content_findings", "tls_findings", "mail_findings",
                 "domain_findings", "subdomain_findings", "security_txt_findings"):
        monkeypatch.setattr(extra, name, finding)
    with app.test_request_context("/"), force_locale("uk"):
        extra.run_extras("example.test", "example.test", "html", {}, True, False, "", "text")
    assert observed == ["uk"] * 7
