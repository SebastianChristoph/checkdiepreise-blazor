# checkdiepreise-blazor

Wie sehr gehen die Preise in deutschen Märkten nach oben oder unten?
Wird Butter wirklich immer teurer? Werden Malms bei IKEA immer günstiger?

Dieses Projekt vereint WebScraping mit Python und das Visualisieren der Daten mit *ASP.NET Frameork mit Blazor* . 

- Alle Python-Skripte im Ordner *Crawler* werden täglich lokal auf einem Raspberry-Pi Zero ausgeführt.
- Im Ordner *CheckDiePreise* befindet sich die komplette Blazor-Anwendung
- Die SQLite Datenbank befindet sich in der Blazor-Anwendung im wwwroot


  ### Problemlösung: SQLite DB, Azure ud Git

  Es ist möglich eine SQLite Datenbank auf Azure zu hosten, auf die der Raspberry Pi mit seinen Crawler-Scrips zugreift. Diese Azure SQL DB ist jedoch teuer (rund 70 Euro pro Monat). Daher nutze ich eine SQLite DB. Diese ist immer aktuell auf dem Raspberry Pi. Ein tägiches Skript holt sich diese DB via SSH vom Raspberry Pi und synchronisiert die DB mit dem Git Repo der checkdiepreise-Repo. 
Etwas umständlich, aber gratis !  
