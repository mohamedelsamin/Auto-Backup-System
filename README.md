# Auto-Backup-System
## 📌 Project Overview

Auto Backup System is a Python automation project designed to simplify and secure the backup process.
The system collects files from a user-defined folder, compresses them into ZIP archives, stores them in a backup directory, runs automatically on a schedule, and deletes old backups to save disk space.

## 🎯 Features
- Backup any user-defined folder
- Compress files into ZIP archives
- Automated daily backups using scheduling
- Automatic deletion of old backups
- Timestamped backup filenames
- Windows compatible

## Technologies Used
- Python 3
- os – File system operations
- zipfile – File compression
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

