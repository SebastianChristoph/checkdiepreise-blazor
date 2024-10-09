# checkdiepreise-blazor

Wie sehr gehen die Preise in deutschen Märkten nach oben oder unten?
Wird Butter wirklich immer teurer? Werden Malms bei IKEA immer günstiger?

Dieses Projekt vereint WebScraping mit Python und das Visualisieren der Daten mit Blazor. 

- Alle Python-Skripte im Ordner *Crawler* werden täglich lokal auf einem Raspberry-Pi Zero ausgeführt.
- Im Ordner *CheckDiePreise* befindet sich die komplette Blazor-Anwendung
- Die eigentliche SQLite Datenbank befindet sich in der Blazor-Anwendung im Ordner *Data*, wird aber aus Sicherheits-und Platzgünden nicht mit dieser Repo synchronisiert.
