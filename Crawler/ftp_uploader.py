from ftplib import FTP
import os
import secrets

ftp_server = secrets.ftp_server
ftp_username = secrets.ftp_username
ftp_password =  secrets.ftp_password
file_to_upload = secrets.file_to_upload 
upload_directory = secrets.upload_directory

print("CURRENT OS:", os.getcwd())
file_name = os.path.basename(file_to_upload)

def upload_sqlitedb_to_azure():
    print("START FTP UPLOAD")
    ftp = FTP(ftp_server)
    ftp.login(user=ftp_username, passwd=ftp_password)
    ftp.set_pasv(True)

    try:
        ftp.cwd(upload_directory)
        print(f'Wechsel in das Verzeichnis "{upload_directory}" erfolgreich.')
    except Exception as e:
        print(f'Fehler beim Wechseln in das Verzeichnis: {e}')
        ftp.quit()
        return
    
    try:
        with open(file_to_upload, 'rb') as file:
            ftp.storbinary(f'STOR {file_name}', file)
            print(f'Datei "{file_name}" wurde erfolgreich hochgeladen.')
    except Exception as e:
        print(f"Fehler beim Hochladen: {e}")

    ftp.quit()
