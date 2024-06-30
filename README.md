# Database Backup Script

This project is a Python script designed to automate the backup process for a database, including archiving, encryption, and uploading the backup to a cloud storage service.

## Features

- Parses configuration for database and cloud storage credentials
- Connects to the PostgreSQL database and creates a backup
- Archives the backup file to optimize storage size
- Encrypts the archived backup for security
- Uploads the encrypted backup to AWS S3 (or other cloud storage solutions with minor modifications)

## Prerequisites

- Python 3.6 or higher
- PostgreSQL database
- AWS S3 account (for cloud storage)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/database-backup-script.git
    cd database-backup-script
    ```

2. Install the required Python packages:
    ```sh
    pipenv install
    ```

3. Create a `config.ini` file with your configuration:
    ```ini
    [database]
    host=localhost
    port=5432
    user=your_db_user
    password=your_db_password
    dbname=your_db_name

    [cloud]
    provider=aws
    token=your_aws_access_key
    bucket=your_s3_bucket

    [backup]
    password=your_backup_password
    ```

## Usage

Run the script with:
```sh
python backup_script.py
