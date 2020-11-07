# Sync files between a Google Drive folder and a remote server

- [Requirements](#requirements)
- [Setting up an account in Google Cloud Platform](#setting-up-an-account-in-google-cloud-platform)
- [Setting up SeamlessCloud](#setting-up-seamlesscloud)
- [Running the script locally](#running-the-locally)
- [Running the script on SeamlessCloud](#running-the-locally)

## Requirements
1. Python 3.6 or higher
2. [Google Cloud Platform](https://console.cloud.google.com/) account
3. [SeamlessCloud](http://seamlesscloud.io/) account (optionally)

## Setting up an account in Google Cloud Platform
BLUF: The easiest way is to find a video tutorial on YouTube (for example, [this one](https://www.youtube.com/watch?v=W5mPX1-015o&ab_channel=storagefreak)).
As a result, you will have a json file that looks like this:
```json
{
  "type": "service_account",
  "project_id": "project-290420",
  "private_key_id": "das23782dded1ada49604e8f9casddd1c33d98asdadf498",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADAN******9gGPbxBvl2Q==\n-----END PRIVATE KEY-----\n",
  "client_email": "project@project-120420.iam.gserviceaccount.com",
  "client_id": "1092342459991526277037806",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/project%project-2231220.iam.gserviceaccount.com"
}
```

After obtaining a json keyfile, create a Google Drive folder and share it with `client_email` from the json keyfile. Set permissions `Editor`.  
Before running the script, upload at least one file.

## Setting up SeamlessCloud
Create a free account at [http://seamlesscloud.io](http://seamlesscloud.io/).

With Seamless Cloud you can also deploy any custom script from your local machine, more info here: [https://app.seamlesscloud.io/faq/cli](https://app.seamlesscloud.io/faq/cli). Email us at `hello@seamlesscloud.io` in case you have questions.

## Running the script locally
1. Clone or download the script.
2. Move `google-credentials.json` from the previous step to `sync_grdive_and_remote_server` folder.
3. Create `remote-server-pkey.txt` file to be able to connect to a remote server via SSH.
4. Update variables in `function.py` (Google Drive and a remote server access).
5. Run the script on your machine: `PYTHONPATH=. python3 function.py`.

## Running the script on SeamlessCloud
1. Authenticate `smls` client `smls auth <API_KEY>`. You can find `API_KEY` in your [account](https://app.seamlesscloud.io/account).
2. Deploy the job `smls publish --name "Sync GDrive and server"`.
3. Open the job page and click `Run` button.
