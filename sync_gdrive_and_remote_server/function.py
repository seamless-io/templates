import io
import os
from pathlib import Path

import paramiko
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Google Drive
FOLDER_ID = 'XXX'  # The ID of your Google Drive folder. You can get it from the URL.
JSON_KEYFILE = 'google-credentials.json'  # The file with Google credentials.
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']

# Remote server
HOST = 'example.com'  # Domain name or an IP address.
PORT = 22  # SSH port. By default it is 22.
USERNAME = 'user'  # Username to connect via SSH.
PKEY = 'remote-server-pkey.txt'  # The file with a private key to the remote server.
FOLDER = '/home/ubuntu/files'  # The path to a folder on the remote server, where you are going to store files.

def gdrive_client(json_keyfile, scopes):
    credentials = service_account.Credentials.from_service_account_file(json_keyfile, scopes=scopes)
    service = build('drive', 'v3', credentials=credentials)
    return service


def get_ssh_client(hostname, port, username, private_key):
    pkey_bytes = io.StringIO(private_key)
    pkey = paramiko.RSAKey.from_private_key(pkey_bytes)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=int(port), username=username, pkey=pkey)
    return client


def get_files(service, folder_id):
    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, files(id, name, mimeType)",
                                   q=f"'{folder_id}' in parents").execute()
    nextPageToken = results.get('nextPageToken')
    while nextPageToken:
        nextPage = service.files().list(pageSize=10,
                                        fields="nextPageToken, files(id, name, mimeType, parents)",
                                        q=f"'{folder_id}' in parents",
                                        pageToken=nextPageToken).execute()
        nextPageToken = nextPage.get('nextPageToken')
        results['files'] = results['files'] + nextPage['files']
    return results['files']


def download_file(service, file, folder):
    request = service.files().get_media(fileId=file['id'])
    filename = f"{folder}/{file['name']}"
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(file['name'] + " Download %d%%." % int(status.progress() * 100))


def sync_files(json_keyfile, scopes, folder_id):
    print('Start syncing...')

    # Open a private key and instantiate the SSH client.
    with open(PKEY) as pkey:
        PRIVATE_KEY = pkey.read()
    ssh_client = get_ssh_client(HOST, PORT, USERNAME, PRIVATE_KEY)

    # Check if FOLDER ('/home/ubuntu/files') exists on the remote machine, if not - create it.
    stdin, stdout, stderr = ssh_client.exec_command(f'[ -d {FOLDER} ] && echo "Directory exists!"')
    if stdout.read().decode('utf-8') != 'Directory exists!':
        ssh_client.exec_command(f'mkdir {FOLDER}')

    # Collect existing file names on the remote machine.
    stdin, stdout, stderr = ssh_client.exec_command(f'ls {FOLDER}')
    existing_files = stdout.read().decode('utf-8').split('\n')

    # Instantiate Google Drive client and collect files metadata from Google Drive.
    service = gdrive_client(json_keyfile, scopes)
    files = get_files(service, folder_id)

    # Check if "./files" temp folder exists on the local machine, if not - create it.
    # We are going to store files there, then delete it.
    files_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '/files'))
    if not os.path.isdir(files_folder):
        Path(files_folder).mkdir(parents=True, exist_ok=True)

    # Loop through files from Google Drive, if it is not existed on the remote machine upload it.
    for file in files[:2]:
        if file['name'] not in existing_files:
            # We download a file on the local machine, before upload it to the remote server.
            download_file(service, file, files_folder)

            # Upload a file to the remote server
            ftp_client = ssh_client.open_sftp()
            ftp_client.put(f'{files_folder}/{file["name"]}', f'{FOLDER}/{file["name"]}')
            ftp_client.close()

            # Delete a file from the local machine.
            # It prevents polluting local file system in case we are going to sync a large amount of files.
            if os.path.exists(f'{files_folder}/{file["name"]}'):
                os.remove(f'{files_folder}/{file["name"]}')

    # Delete "/files" folder from the local machine.
    if os.path.exists(files_folder):
        os.rmdir(files_folder)

    print('Finish syncing.')


if __name__ == '__main__':
    sync_files(JSON_KEYFILE, SCOPE, FOLDER_ID)
