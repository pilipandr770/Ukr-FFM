"""Стандартный каталог услуг партнёра. Текст — контент для участников клуба (немецкий), правится в админке."""

from ..extensions import db
from ..models import Service

PROVIDER = "Andrii-IT · Partner des Clubs"
EMAIL = "info@andrii-it.de"
BENEFIT = "Kostenloses Erstgespräch für Club-Mitglieder"

# Встроенные ИИ-поиски по законам: услуга в каталоге открывает инструмент с предвыбранной страной (slug → код страны)
LAW_SERVICES = {"gesetze-schnellsuche-de": "DE"}

DEFAULT_SERVICES = (
    dict(slug="gesetze-schnellsuche-de", sort=-2, title="KI-Schnellsuche im deutschen Recht",
         summary="Stell deine Frage in eigenen Worten und bekomme die passenden Vorschriften aus dem deutschen "
                 "Bundesrecht im Wortlaut, mit einer verständlichen Erläuterung. Spart Zeit bei der Vorbereitung "
                 "auf einen Termin mit einer Anwältin oder einem Anwalt.",
         description="Das Tool durchsucht rund 6.000 Bundesgesetze nach Bedeutung (nicht nur nach Stichworten) und "
                     "zitiert den Gesetzestext unverändert mit Quelle. Eine KI erklärt in einfachen Worten, was im "
                     "Text steht. Sie bewertet nie deinen Einzelfall und gibt keine Handlungsempfehlung — das ist "
                     "keine Rechtsberatung. Nutze es, um mit klaren Fragen und den richtigen Paragraphen in das "
                     "Gespräch mit einer Fachperson zu gehen. Für eine verbindliche Einschätzung schreib uns über "
                     "das Formular unten: Wir stellen den Kontakt zu einer Fachperson her.",
         benefits="Passende Paragraphen in Minuten statt Stunden\nGesetzestext im Wortlaut mit Quelle\n"
                  "Gut vorbereitet in den Termin mit einer Anwältin oder einem Anwalt\n"
                  "Keine Einzelfallbewertung, keine Rechtsberatung",
         price_hint="im Mitgliedsbeitrag enthalten (Kontingent je Tarif)"),
    dict(slug="ki-chatbots", sort=1, title="KI-Chatbots & digitale Assistenten",
         summary="Ein Assistent für deine Website, WhatsApp oder Telegram, der Anfragen beantwortet, Termine "
                 "vorbereitet und Leads qualifiziert — DSGVO-konform mit Hosting in der EU.",
         description="Wir entwickeln KI-Assistenten, die dein Angebot kennen und im Ton deiner Marke antworten: "
                     "auf der Website, in WhatsApp oder Telegram. Inklusive Datenschutzkonzept, Kennzeichnung nach "
                     "KI-Verordnung und Übergabe an dein Team, wenn ein Mensch gefragt ist.",
         benefits="Antworten rund um die Uhr, auch außerhalb der Bürozeiten\nWeniger Routinefragen im Postfach\n"
                  "Leads mit vollständigen Angaben statt halber E-Mails\nHosting in Deutschland, Auftragsverarbeitung inklusive",
         price_hint="Festpreis nach Erstgespräch"),
    dict(slug="cybersecurity-check", sort=2, title="Cybersecurity-Check für Selbstständige & KMU",
         summary="Wie angreifbar ist dein Unternehmen von außen? Ein Check deiner Website, E-Mail-Sicherheit und "
                 "öffentlich sichtbaren Systeme — mit verständlichem Bericht und klaren nächsten Schritten.",
         description="Wir prüfen, was Angreifer:innen über dein Unternehmen sehen: Website, Domain- und "
                     "E-Mail-Konfiguration (SPF, DKIM, DMARC), veraltete Software, offene Dienste. Du bekommst "
                     "einen Bericht ohne Fachchinesisch und eine priorisierte Maßnahmenliste.",
         benefits="Schwachstellen finden, bevor andere es tun\nNachweis für Versicherer und Kund:innen\n"
                  "Priorisierte Maßnahmen statt Panik",
         price_hint="ab Pauschalpreis, je nach Umfang"),
    dict(slug="nis2-dsgvo-compliance", sort=3, title="NIS2- und DSGVO-Check",
         summary="Bist du von NIS2 betroffen und was musst du konkret tun? Betroffenheitsprüfung, Lückenanalyse "
                 "und Maßnahmenplan für Geschäftsführung und Team.",
         description="Das NIS2-Umsetzungsgesetz erweitert den Kreis der regulierten Unternehmen deutlich und "
                     "nimmt die Geschäftsführung persönlich in die Pflicht. Wir klären Betroffenheit, bewerten den "
                     "Ist-Stand und erstellen einen umsetzbaren Plan.",
         benefits="Klarheit über Betroffenheit und Fristen\nDokumentation für Prüfungen\nSchulung der Geschäftsführung",
         price_hint="nach Aufwand"),
    dict(slug="ki-verordnung", sort=4, title="KI im Unternehmen — rechtssicher einführen",
         summary="Du nutzt ChatGPT, Chatbots oder KI-Tools? Wir prüfen, welche Pflichten aus KI-Verordnung und "
                 "DSGVO für dich gelten, und helfen bei Richtlinien und Schulung.",
         description="Seit 2025 gilt die Pflicht zur KI-Kompetenz für Unternehmen, die KI einsetzen, seit August "
                     "2026 die Transparenzpflichten für Chatbots. Wir machen eine Bestandsaufnahme, ordnen Risiken ein "
                     "und liefern Nutzungsrichtlinie und Schulung.",
         benefits="Überblick über eingesetzte KI-Tools\nNutzungsrichtlinie für dein Team\nNachweis der KI-Kompetenz",
         price_hint="Paketpreis"),
    dict(slug="claude-code-einrichtung", sort=5, title="Claude Code: Einrichtung & effektive Nutzung",
         summary="Du willst mit Claude Code schneller arbeiten, weißt aber nicht, wie du es einrichtest und sinnvoll "
                 "einsetzt? Der Entwickler und Admin dieses Clubs zeigt dir Einstellungen, Arbeitsweise und typische "
                 "Stolpersteine.",
         description="Dieser Club wurde gemeinsam von seinem Entwickler und Claude Code gebaut. Aus dieser Praxis "
                     "gibt Andrii Pylypchuk sein Wissen weiter: Wie richtest du Claude Code für dein Projekt ein, "
                     "welche Einstellungen, Berechtigungen und Projektregeln (CLAUDE.md) lohnen sich, wie formulierst "
                     "du Aufgaben, damit das Ergebnis passt, und wie prüfst du, was die KI geliefert hat. Das Angebot "
                     "richtet sich an Gründer:innen, Selbstständige und kleine Teams ohne tiefes Technikwissen. Es "
                     "ist eine Einführung und Begleitung, keine Garantie für ein bestimmtes Ergebnis.",
         benefits="Sinnvolle Einrichtung statt Ausprobieren auf eigene Faust\nKlare Regeln für sicheres Arbeiten "
                  "(Berechtigungen, Geheimnisse, Prüfung der Ergebnisse)\nPraxisbeispiele aus einem echten Projekt\n"
                  "Mehr Wirkung pro Stunde und pro Token",
         price_hint="Erstgespräch kostenlos, danach nach Aufwand"),
    dict(slug="online-shop", sort=6, active=False, title="Eigener Online-Shop mit KI-Verkäufer",
         summary="Starte deinen eigenen Online-Shop mit Produktkatalog, Warenkorb, Kartenzahlung und einem "
                 "KI-Verkäufer, der Fragen deiner Kundschaft beantwortet. Eigene Adresse, DSGVO-Seiten inklusive.",
         description="Die Shop-Plattform SmartShop gehört zum selben Anbieter wie dieser Club und läuft getrennt "
                     "vom Club. Jeder Shop bekommt eine eigene Adresse (Subdomain oder eigene Domain), Katalog, "
                     "Warenkorb und Kasse. Zahlungen laufen über Stripe direkt auf dein Konto, der Club nimmt kein "
                     "Geld an. Der eingebaute KI-Verkäufer kennt dein Sortiment und Bestellstatus. Auf Wunsch "
                     "mit Versand über DHL oder UPS, Shop auf Ukrainisch, Deutsch und Englisch. Impressum, AGB und "
                     "Datenschutz legst du für deinen Shop selbst an und bist als Händler:in dafür verantwortlich. "
                     "Der Zugang ist ein eigenes Abo bei SmartShop, nicht Teil deines Club-Tarifs.",
         benefits="Shop mit Kasse und Kartenzahlung in kurzer Zeit startklar\nKI-Verkäufer beantwortet Kundenfragen\n"
                  "Mehrsprachig: Ukrainisch, Deutsch, Englisch\nZahlungen direkt auf dein Stripe-Konto",
         price_hint="eigenes Monatsabo mit Testphase, Preise im Erstgespräch"),
)


def seed_default_services() -> int:
    """Добавляет недостающие услуги по slug. Существующие (в том числе изменённые в админке) не трогает."""
    created = 0
    for item in DEFAULT_SERVICES:
        if Service.query.filter_by(slug=item["slug"]).first():
            continue
        fields = {"member_benefit": BENEFIT, "provider_name": PROVIDER, "provider_email": EMAIL, "active": True, **item}
        db.session.add(Service(**fields))
        created += 1
    db.session.commit()
    return created
