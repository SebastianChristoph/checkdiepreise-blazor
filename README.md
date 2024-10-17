# checkdiepreise-blazor

Wie sehr gehen die Preise in deutschen Märkten nach oben oder unten?
Wird Butter wirklich immer teurer? Werden Malms bei IKEA immer günstiger?

Dieses Projekt vereint WebScraping mit Python und das Visualisieren der Daten mit Blazor. 

- Alle Python-Skripte im Ordner *Crawler* werden täglich lokal auf einem Raspberry-Pi Zero ausgeführt.
- Im Ordner *CheckDiePreise* befindet sich die komplette Blazor-Anwendung
- **Die eigentliche SQLite Datenbank befindet sich in der Blazor-Anwendung im Ordner *Data*, wird aber aus Sicherheits-und Platzgünden nicht mit dieser Repo synchronisiert.**


  ### Problemlösung: SQLite DB und Azure

  Es ist möglich eine SQLite Datenbank auf Azure zu hosten. Es ist "von außen", also für den Raspberry Pi, dann jedoch nur umständlich möglich Einträge auf diese SQLite Datenbank zu erstellen.
  Hier behelfe ich mir einem Trick: Die SQLite-Datenbank, die tagesaktuell auf dem Raspberry Pi liegt, wird töglich via FTP auf die AzureWeb-App gesendet und damit täglich überschrieben.

  **Doch halt!**
  Wie kann eine File bzw Datenbank im *Always On* - Modus von Azure ersetzt werden? Genau, gar nicht. Daher wird die AzureWebApp über Azure Automation von 01:00 - 02:00 Uhr morgens gestoppt. In dieser Zeit sorgt ein Cronjob auf dem Raspberry Pi für den FTP Upload.
  Etwas hacky, aber funktioniert und spart enorm viel Geld (im Vergleich zu einer Azure SQL DB).
  
