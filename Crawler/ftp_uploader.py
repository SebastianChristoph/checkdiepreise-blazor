from ftplib import FTP
import os
import secrets

# FTP-Verbindungsinformationen
ftp_server = secrets.ftp_server #
ftp_username = secrets.ftp_username
ftp_password =  secrets.ftp_password
file_to_upload = 'C:\\Users\\sebas\\Desktop\portfolopOnline\\checkdiepreise-blazor\\LocalSqliteDb.db'  # Ersetze durch den Pfad zu deiner Datei
upload_directory = 'site\\wwwroot\\App_Data' 

print("CURRENT OS:", os.getcwd())

# Extrahiere den Dateinamen aus dem Pfad
file_name = os.path.basename(file_to_upload)

def upload_sqlitedb_to_azure():
    print("START FTP UPLOAD")
    ftp = FTP(ftp_server)
    ftp.login(user=ftp_username, passwd=ftp_password)
    
    # Passiven Modus aktivieren
    ftp.set_pasv(True)

    # Dateien im Root-Verzeichnis auflisten
    try:
        files = ftp.nlst()  # Liste der Dateien und Ordner im Root-Verzeichnis
        for f in files:
            print(f)
    except Exception as e:
        print(f'Fehler beim Abrufen der Dateiliste: {e}')
        ftp.quit()
        return

    # In das gewünschte Verzeichnis wechseln
    try:
        ftp.cwd(upload_directory)  # Wechselt in den Ordner 'App_Data'
        print(f'Wechsel in das Verzeichnis "{upload_directory}" erfolgreich.')
    except Exception as e:
        print(f'Fehler beim Wechseln in das Verzeichnis: {e}')
        ftp.quit()
        return

    # Datei öffnen und hochladen
    try:
        with open(file_to_upload, 'rb') as file:
            # Datei hochladen
            ftp.storbinary(f'STOR {file_name}', file)  # Nur den Dateinamen übergeben, nicht den kompletten Pfad
            print(f'Datei "{file_name}" wurde erfolgreich hochgeladen.')
    except Exception as e:
        print(f"Fehler beim Hochladen: {e}")

    # Verbindung trennen
    ftp.quit()
