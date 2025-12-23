# Auto-Backup-System
## 📌 Project Overview

The Auto Backup System is a Python automation tool designed to create secure and organized backups of important files automatically.
It compresses selected folders, stores backups locally, removes old backups, uploads the latest backup to **Google Drive**, and sends an email notification after successful completion.  
### This project was built to solve a real problem:  
👉 Manually backing up files is error-prone, time-consuming, and easy to forget.

## 🎯 Features
- Automatic backup of important folders
- Compression into ZIP files
- Automatic deletion of old backups
- Upload latest backup to Google Drive
- Email notification after successful backup
- Can be scheduled to run automatically

## Technologies Used
- Python 3
- os – File system operations
- zipfile – File compression
- Google Drive API – cloud upload
- smtplib & email – email notifications
- schedule – Task scheduling
- datetime – Timestamp generation
- time – Continuous execution loop

## 🧪 Run Backup Immediately (Optional)

To test the backup process instantly, temporarily add this line inside backup.py:
```
schedule.every().day.at(BACKUP_TIME).do(create_backup)

create_backup()  👈👈👈👈👈

print("Auto Backup System is running...")
```
On first run, a browser window will open to authenticate your Google account.

## 🔐 Google Drive Setup
- Create a project on Google Cloud Console
- Enable Google Drive API
- Download ``` client_secrets.json ```
- Place it in the project folder

## Email Notification
After a successful backup and upload, an email is automatically sent to confirm that the process completed successfully.
