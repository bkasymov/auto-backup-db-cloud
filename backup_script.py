import os
import tarfile
import boto3
from cryptography.fernet import Fernet
import psycopg2
from configparser import ConfigParser

def parse_config(config_file):
    config = ConfigParser()
    config.read(config_file)
    db_config = {
        'host': config.get('database', 'host'),
        'port': config.get('database', 'port'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'dbname': config.get('database', 'dbname')
    }
    cloud_config = {
        'provider': config.get('cloud', 'provider'),
        'token': config.get('cloud', 'token'),
        'bucket': config.get('cloud', 'bucket')
    }
    backup_password = config.get('backup', 'password')
    return db_config, cloud_config, backup_password

def backup_database(db_config):
    backup_file = '/tmp/database_backup.sql'
    conn = psycopg2.connect(**db_config)
    with open(backup_file, 'w') as f:
        cursor = conn.cursor()
        cursor.copy_expert(f"COPY (SELECT * FROM {db_config['dbname']}) TO STDOUT", f)
        cursor.close()
    conn.close()
    return backup_file

def create_tar(backup_file):
    tar_file = backup_file + '.tar.gz'
    with tarfile.open(tar_file, 'w:gz') as tar:
        tar.add(backup_file, arcname=os.path.basename(backup_file))
    os.remove(backup_file)
    return tar_file

def encrypt_file(tar_file, password):
    encrypted_file = tar_file + '.enc'
    key = Fernet(password)
    with open(tar_file, 'rb') as f:
        data = f.read()
    encrypted_data = key.encrypt(data)
    with open(encrypted_file, 'wb') as f:
        f.write(encrypted_data)
    os.remove(tar_file)
    return encrypted_file

def upload_to_s3(encrypted_file, cloud_config):
    s3 = boto3.client(
        's3',
        aws_access_key_id=cloud_config['token'],
        aws_secret_access_key=cloud_config['token']
    )
    bucket = cloud_config['bucket']
    s3.upload_file(encrypted_file, bucket, os.path.basename(encrypted_file))
    os.remove(encrypted_file)

def main():
    config_file = 'config.ini'
    db_config, cloud_config, backup_password = parse_config(config_file)

    backup_file = backup_database(db_config)
    tar_file = create_tar(backup_file)
    encrypted_file = encrypt_file(tar_file, backup_password.encode())

    if cloud_config['provider'] == 'aws':
        upload_to_s3(encrypted_file, cloud_config)
    else:
        print("Cloud provider not supported yet")

if __name__ == "__main__":
    main()
