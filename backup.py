import os
import zipfile
import schedule
import time
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SOURCE_FOLDER = r"D:\icons"      # Folder to back up
BACKUP_FOLDER = r"D:\Backups"    # Local backup destination
MAX_BACKUPS = 5                   # Maximum number of backups to keep
BACKUP_TIME = "02:00"             # Daily backup time (HH:MM)
CLIENT_SECRETS_PATH = r"D:\my python\backup system\client_secrets.json"


# Email configuration
FROM_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"  # Gmail App Password
TO_EMAIL = "recipient_email@gmail.com"


def delete_old_backups():
    backups = []
    for file in os.listdir(BACKUP_FOLDER):
        if file.endswith(".zip"):
            file_path = os.path.join(BACKUP_FOLDER, file)
            creation_time = os.path.getctime(file_path)
            backups.append((file_path, creation_time))

    backups.sort(key=lambda x: x[1])

    while len(backups) > MAX_BACKUPS:
        old_backup = backups.pop(0)
        os.remove(old_backup[0])
        print(f"Deleted old backup: {os.path.basename(old_backup[0])}")


def upload_to_drive(file_path):
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile(CLIENT_SECRETS_PATH)  # Use full path
    gauth.LocalWebserverAuth()  # This opens browser for first-time auth
    drive = GoogleDrive(gauth)

    file_drive = drive.CreateFile({'title': os.path.basename(file_path)})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    print(f"Uploaded to Google Drive: {file_path}")


def send_email_notification(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()
    print(f"Email sent to {to_email}")


def create_backup():
    date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backup_{date_now}.zip"

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    backup_path = os.path.join(BACKUP_FOLDER, backup_name)

    # Compress files
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
        for foldername, subfolders, filenames in os.walk(SOURCE_FOLDER):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                backup_zip.write(file_path)

    print(f"Backup created successfully: {backup_name}")

    # Delete old backups
    delete_old_backups()

    try:
        # Upload to Google Drive
        upload_to_drive(backup_path)

        # Send email notification
        send_email_notification(
            subject="Backup Successful",
            body=f"Your backup '{backup_name}' was created and uploaded successfully!",
            to_email=TO_EMAIL
        )
    except Exception as e:
        print(f"Error during upload/email: {e}")


schedule.every().day.at(BACKUP_TIME).do(create_backup)

print("Auto Backup System is running...")

while True:
    schedule.run_pending()
    time.sleep(60)
