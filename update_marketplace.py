import os
import tarfile

import requests

PACKAGE_NAME = 'templates.tar.gz'
EXCLUDE_FOLDERS_AND_FILES = ['.git', '__pycache__', '.pytest_cache']


def filtr(file):
    for name in EXCLUDE_FOLDERS_AND_FILES:
        if file.name.startswith(f"./{name}"):
            return None
    return file


tar = tarfile.open(PACKAGE_NAME, "w:gz")
tar.add('.', filter=filtr)
tar.close()

url = f"http://github_actions:{os.getenv('SEAMLESS_WEB_API_PASSWORD')}@{os.getenv('SEAMLESS_HOST')}/api/v1/marketplace"
resp = requests.post(url, files={'templates': open(PACKAGE_NAME, 'rb')})
resp.raise_for_status()
