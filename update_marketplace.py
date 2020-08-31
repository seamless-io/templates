import os
import tarfile

import requests

PACKAGE_NAME = 'templates.tar.gz'

tar = tarfile.open(PACKAGE_NAME, "w:gz")
tar.add('.')
tar.close()

url = f"https://github_actions:{os.getenv('SEAMLESS_WEB_API_PASSWORD')}@{os.getenv('SEAMLESS_HOST')}/api/v1/marketplace"
resp = requests.post(url, files={'templates': open(PACKAGE_NAME, 'rb')})
resp.raise_for_status()
