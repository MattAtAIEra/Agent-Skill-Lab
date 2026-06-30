<p align="center">
  <img src="banner.svg" alt="Agent Skill Lab" width="100%"/>
</p>

<h3 align="center">Schluss mit Chaos — Claude-Code-Plugins, die deinem KI-Agenten Ingenieurdisziplin beibringen.</h3>

<p align="center">
  <a href="README.md">English</a> &bull;
  <a href="README_zh_TW.md">繁體中文</a> &bull;
  <a href="README_ja.md">日本語</a> &bull;
  <strong>Deutsch</strong> &bull;
  <a href="README_ko.md">한국어</a>
</p>

<p align="center">
  <a href="#installation">In 30 Sekunden installiert</a> &bull;
  <a href="#plugins">Plugins entdecken</a> &bull;
  <a href="#mitwirken">Mitwirken</a>
</p>

---

## Das Problem

KI-Coding-Agenten sind beeindruckend produktiv — solange man nicht genau hinschaut. Ohne klare Leitplanken überspringen sie Spezifikationen, vergessen Tests, hämmern fehlgeschlagene Befehle stur erneut ein und liefern APIs ohne jede Dokumentation. Das Ergebnis: Statt Features auszuliefern, spielst du Babysitter für deinen Agenten.

## Die Lösung

**Agent Skill Lab** ist ein Plugin-Marktplatz für [Claude Code](https://docs.anthropic.com/en/docs/claude-code), der Engineering-Best-Practices als installierbare Skills bereitstellt. Jedes Plugin kodifiziert eine bestimmte Disziplin — Spec-first-API-Entwicklung, saubere Befehlsausführung, strukturiertes Entwicklungsprotokoll, SQL-DDL-Konventionen — damit dein Agent dieselben Standards einhält wie ein erfahrener Entwickler.

## Installation

```bash
# 1. Marktplatz hinzufügen (einmalig)
claude plugin marketplace add https://github.com/MattAtAIEra/Agent-Skill-Lab.git

# 2. Benötigte Plugins installieren (Namen siehe Tabelle unten)
claude plugin install dev-discipline@agent-skill-lab
claude plugin install narrated-deck@agent-skill-lab
# …gleiches Schema für jedes weitere Plugin:  <plugin-name>@agent-skill-lab
```

> In einer Claude-Code-Sitzung gehen auch die Slash-Befehle — `/plugin marketplace add …`, `/plugin install …`, danach `/reload-plugins`. `/plugin` öffnet einen interaktiven Browser.

## Aktualisieren

Plugins werden **nicht** per `git pull` aktualisiert — Claude Code hält unter `~/.claude/plugins/` eine eigene verwaltete Kopie, ein manuelles Pullen dieses Repos bewirkt daher nichts. Nach der Veröffentlichung einer neuen Version aktualisierst du innerhalb von Claude Code:

```bash
# 1. Katalog dieses Marktplatzes neu laden
claude plugin marketplace update agent-skill-lab

# 2. Ein Plugin auf die neueste Version aktualisieren
claude plugin update narrated-deck@agent-skill-lab

# 3. Neu laden, damit die neue Version wirksam wird (kein Neustart nötig)
/reload-plugins
```

- **Nicht automatisch:** Bei Drittanbieter-Marktplätzen wie diesem ist die automatische Aktualisierung **standardmäßig deaktiviert** — Aktualisieren ist ein manueller Schritt (oder pro Marktplatz über die `/plugin`-Oberfläche aktivieren).
- **Versionsgesteuert:** Die `version` eines Plugins (in seiner `plugin.json`) steuert Updates — du erhältst Änderungen nur, wenn der Maintainer sie hochzählt; Commits ohne Versionssprung erreichen installierte Kopien nicht.

## Plugins

| Plugin | Skills | Funktion |
|--------|--------|----------|
| **dev-discipline** | `api-dev-workflow` `command-execution` `dev-log` | Spec-first-API-Entwicklung, sichere Befehlsausführung, strukturiertes Entwicklungsprotokoll |
| **sql-ddl-convention** | `sql-ddl-convention` | DDL-Designstandards — Audit-Felder, Indizes, Namenskonventionen, Mermaid-ERD-Generierung |
| **skill-and-agent-authoring** | `skill-and-agent-authoring` | Korrekte YAML-Frontmatter und Verzeichnisstruktur für die Plugin-Erstellung |
| **narrated-deck** | `narrated-deck` | Verwandelt PPT/PDF/Gliederung in eine eigenständige narrierte HTML-Seite — TTS-Audio pro Untertitel, Szenenübergänge, eingebauter Player |
| **research-discipline** | `government-research-stance` | Hält staatlich beauftragte Forschung in der Rolle des technischen Stabs und verhindert Übergriffe in legislative/regulatorische Rollen |
| **deploy-preflight** | `deploy-preflight` | Preflight-Check für Produktiv-Deployments — Ressourcen des Zielhosts prüfen und Schutzmaßnahmen in Deploy-Skripte einbauen |
| **notebooklm-cleaner** | `notebooklm-watermark-remover` | Entfernt das NotebookLM-Wasserzeichen aus exportierten PDFs |

### dev-discipline

Drei Skills, die den Entwicklungsworkflow deines Agenten wasserdicht machen:

- **api-dev-workflow** — Erzwingt Spec-first-Entwicklung: API-Spezifikation schreiben, Bestätigung einholen, implementieren, testen, Postman-Collection & OpenAPI-Doku generieren. Kein Schritt darf übersprungen werden.
- **command-execution** — Verhindert blindes Wiederholen. Einmal ausführen → Ergebnis prüfen → Ursache analysieren → nächsten Schritt entscheiden. Deckt Arbeitsverzeichnis-Validierung, Voraussetzungsprüfung und Hintergrundprozess-Verwaltung ab.
- **dev-log** — Dokumentiert jede Entwicklungsphase automatisch in `doc/dev-log.md` mit strukturierten Einträgen: Was wurde getan, was wurde entdeckt, aktueller Teststatus.

### sql-ddl-convention

Ein umfassendes SQL-DDL-Regelwerk:

- `BIGINT`-Primärschlüssel, verpflichtende Audit-Felder (`creator`, `createDate`, `modifier`, `modifyDate`, `removed`)
- Fremdschlüssel-Benennung `<tableName>_id`, keine FK-Constraints (Verantwortung der Anwendungsschicht)
- Indexregeln, standardmäßig `NOT NULL`, `camelCase`-Benennung, keine ENUMs, kein `FLOAT` für Geldbeträge
- Automatische Mermaid-ER-Diagramm-Generierung bei jeder DDL-Ausgabe

### skill-and-agent-authoring

Das Meta-Plugin: eine Anleitung zum Erstellen neuer Skills und Agents mit korrektem YAML-Frontmatter, Trigger-Phrasen-Konventionen, Verzeichnisstruktur und Tool-Konfiguration.

## Projektstruktur

```
agent-skill-lab/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── dev-discipline/         # API-Workflow, Befehlssicherheit, Entwicklungsprotokoll
│   ├── sql-ddl-convention/     # SQL-DDL-Standards + Mermaid-ERD
│   ├── skill-and-agent-authoring/  # Plugin-Erstellungsanleitung
│   ├── narrated-deck/          # PPT/PDF/Gliederung → narrierte HTML-Seite (TTS)
│   ├── research-discipline/    # Haltung & Ton für Regierungsforschung
│   ├── deploy-preflight/       # Preflight-Checks für Produktiv-Deployments
│   └── notebooklm-cleaner/     # NotebookLM-Wasserzeichen aus PDFs entfernen
├── banner.svg
└── README.md
```

## Mitwirken

Du hast bewährte Entwicklungspraktiken, die auch KI-Agenten einhalten sollten? Mach ein Plugin daraus. Pull Requests sind herzlich willkommen.

1. Forke dieses Repository
2. Erstelle dein Plugin unter `plugins/your-plugin-name/`
3. Nutze das **skill-and-agent-authoring**-Plugin als Formatierungsleitfaden
4. Reiche einen PR ein

## Lizenz

MIT

---

<p align="center">
  <sub>Gebaut für Entwickler, die von ihrer KI denselben Anspruch erwarten wie von sich selbst.</sub>
</p>
