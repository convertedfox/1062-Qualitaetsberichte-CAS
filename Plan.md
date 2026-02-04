# Ziel
## Einleitung
Ziel dieser Anwendung ist es, ein übersichtliches Dashboard für die Qualitätsberichterstattung von Studiengängen zu erstellen. 
Mit Hilfe von Python und Streamlit sollen statistische Daten aus einer großen Excel-Datei gezogen und in einer benutzerfreundlichen Form dargestellt werden. Jede Unterseite des Dashboards wird dabei die gleichen Kennzahlen für einen bestimmten Studiengang abbilden.
## Dargestellte Daten
### Einzelmetriken pro Studiengang
Das Dashboard soll folgende Metriken für jeden Studiengang visualisieren:

a) Studienanfängerzahlen der letzten vier Jahre: Diese Daten befinden sich am Anfang der Excel-Datei in den ersten Spalten.
b) Immatrikulierte Studierende der letzten vier Jahre: Ebenfalls ein wichtiger statistischer Wert.
c) Hochschultyp des Vorstudiums der Studienanfänger: Eine Übersicht darüber, von welcher Art Hochschule die Studienanfänger kommen.
d) Erfolgsquote der Studierenden: Wie viele Studierende schließen das Studium erfolgreich ab.
e) Anzahl der für das Studium benötigten Fachsemester: Durchschnittliche Fachsemesterzahl bis zum Abschluss.
f) Berufserfahrung der Studienanfänger: Wie viele Jahre Berufserfahrung die Studienanfänger mitbringen.
g) Durchschnittliches Alter zu Beginn des Studiums: Das Durchschnittsalter der Studierenden beim Studienstart.
h) Herkunft der Dozenten: Eine Übersicht, woher die Lehrenden stammen.
i) Modulbelegung nach Studiengängen: In welchen Studiengängen die Studierenden welche Module belegen.
j) Herkunft der Modulteilnehmer: Aus welchen Studiengängen kommen die Teilnehmer eines Moduls.
k) Durchschnittliche Modulauslastung: Eine Fließkommazahl, die zeigt, wie stark Module im Schnitt ausgelastet sind.
### Kumulierte Metriken pro Fachbereich
Pro Fachbereich soll es eine eigene Übersichtsseite geben, die kumulierte Metriken aller Studiengänge des jeweiligen Fachbereichs darstellt:
a) Studienanfängerzahlen in den letzten 4 Jahren als Balkendiagramm
b) Immatrikulierte Studierende in den letzten 4 Jahren (Gesamtzahl) als Balkendiagramm
c) Wie viele Module belegt jeder Studiengang (?) als Donut - und das aggregieren auf den Fachbereich
d) Aus welchem Studiengang kommen die Modulteilnehmer (?) als Donut - und das aggregieren auf den Fachbereich
# Architektur
## Quelldateien
Die Quelldaten werden stets in einer Excel-Datei angeliefert, die einer festen Struktur folgt. Diese Excel-Daten werden im ersten Schritt in einen oder mehrere DataFrames überführt, damit die statistischen Werte sauber weiterverarbeitet werden können.
Diese liegt immer im Ordner "data" und heisst immer "Import YYYY". Nimm stets die aktuellste Datei als Quelle, also z.b. "Import 2025.xlsx" vor "Import 2024.xlsx

## Framework
Als Framework dient Streamlit, um die Web-Oberfläche des Dashboards zu gestalten. Die Grafiken und Visualisierungen werden direkt aus den DataFrames heraus generiert und auf den Unterseiten für die jeweiligen Studiengänge angezeigt.
# Benutzeroberfläche
Für die Navigation der Nutzer wird es auf der linken Seite eine Seitenleiste geben, in der alle verfügbaren Studiengänge aufgelistet sind. 
Jeder Studiengang erhält eine eigene Unterseite, die automatisch aus der vorliegenden Excel-Datei generiert wird. 
Das Programm wertet also aus, wie viele Studiengänge vorhanden sind, und erstellt für jeden davon eine eigene Sektion im Dashboard. 
Auf diese Weise können die Benutzer einfach durch die Studiengänge navigieren und erhalten auf jeder Unterseite die relevanten statistischen Kennzahlen.
## Designguide
Verwende exakt diese Farben aus dem DHBW CAS Designguide als Design-Tokens. 
Erfinde keine weiteren Farben. Wenn ein UI-Element eine zusätzliche Farbe bräuchte, nutze eine Abstufung von DHBW Grau (#5C6971) oder markiere TODO.

PRIMÄR:
- primary = #3D4548  (CAS Dunkelgrau)
- secondary = #5C6971 (DHBW Grau)
- accent = #E2001A   (DHBW Rot)

FACHBEREICHE (für Charts/Badges):
- tech = #4192AB
- business = #003966
- social = #9B0B33
- health = #3DCC00

Regeln:
- accent (#E2001A) nur für Interaktion/Hervorhebung (Links, aktive Navigation, CTA), sparsam.
- DHBW Grau darf in 100/75/50/25% eingesetzt werden; CAS Dunkelgrau und DHBW Rot nur 100%.
- https://github.com/convertedfox/1062-Qualitaetsberichte-CAS.git

## UI Umsetzung (Stand heute)
- Grundlayout: Standard-Streamlit, Sidebar mit Expandern je Fachbereich.
- Studiengang-Auswahl: pro Fachbereich Radio-Liste innerhalb des Expanders.
- Diagramme: Balkendiagramme in CAS Rot (#E2001A).
- KPI-Boxen: Karten mit leichter Umrandung und grauem Hintergrund (DHBW Grau mit 25/50% Alpha).
- Abschnitts-Header: rote Unterstreichung (#E2001A).
- Charts/Tabellen: in Card-Optik (Border + Padding mit DHBW Grau 50/25%).
- Typografie: Textfarbe ist global weiss für bessere Lesbarkeit.
- pures weiß oder schwarz als Schriftfarbe - je nach Hintergrund.
