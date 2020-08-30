import os

import requests
import yaml

url = f"https://github_actions:{os.getenv('SEAMLESS_WEB_API_PASSWORD')}@{os.getenv('SEAMLESS_HOST')}/api/v1/marketplace"
res = requests.post(url, json=yaml.load(open('table_of_contents.yml')))
res.raise_for_status()
