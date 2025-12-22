import os
import zipfile
import schedule
import time
from datetime import datetime


SOURCE_FOLDER = r"D:\icons"
BACKUP_FOLDER = r"D:\Backups"    # Where backups are stored
MAX_BACKUPS = 5                  # Keep only last 5 backups
BACKUP_TIME = "02:00"            # Daily backup time (HH:MM)


def delete_old_backups():
    backups = []

    # Read all zip files in backup folder
    for file in os.listdir(BACKUP_FOLDER):
        if file.endswith(".zip"):
            file_path = os.path.join(BACKUP_FOLDER, file)
            creation_time = os.path.getctime(file_path)
            backups.append((file_path, creation_time))

    # Sort backups by creation time (oldest first)
    backups.sort(key=lambda x: x[1])

    # Delete extra old backups
    while len(backups) > MAX_BACKUPS:
        old_backup = backups.pop(0)
        os.remove(old_backup[0])
        print(f"Deleted old backup: {os.path.basename(old_backup[0])}")


def create_backup():
    # Create timestamp
    date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backup_{date_now}.zip"

    # Ensure backup folder exists
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    backup_path = os.path.join(BACKUP_FOLDER, backup_name)

    # Create ZIP file
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
        for foldername, subfolders, filenames in os.walk(SOURCE_FOLDER):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                backup_zip.write(file_path)

    print(f"Backup created successfully: {backup_name}")

    # Clean old backups
    delete_old_backups()


schedule.every().day.at(BACKUP_TIME).do(create_backup)

print("Auto Backup System is running...")

while True:
    schedule.run_pending()
    time.sleep(60)
