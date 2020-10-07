# Update a Google Spreadsheet

This job inserts a price of cryptocurrency of your choice to a Google Spreadsheet.

- [Requirements](#requirements)
- [Setting up an account in Google Cloud Platform](#setting-up-an-account-in-google-cloud-platform)
- [Setting up SeamlessCloud](#setting-up-seamlesscloud)
- [Running the script](#running-the-script)

## Requirements
1. Python 3.6 or higher
2. [Google Cloud Platform](https://console.cloud.google.com/) account
3. [SeamlessCloud](http://seamlesscloud.io/) account

## Setting up an account in Google Cloud Platform
BLUF: The easiest way is to find a video tutorial on YouTube.
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

After obtaining a json keyfile, create a Google Spreadsheet and share it with `client_email` form the json keyfile. Set permissions `Editor`.  
Before running the script, rename the current sheet to `crypto`. You can choose any name you want, but remember to update a corresponding environment variable as well.

## Setting up SeamlessCloud
Create a free account at [http://seamlesscloud.io](http://seamlesscloud.io/) and install `smls` library on your local machine.
```shell script
pip install smls
```  
Be sure you `pip` for Python 3. You can check it: `pip --version`.

## Running the script
1. Download the source code from Github or [https://app.seamlesscloud.io/templates](https://app.seamlesscloud.io/templates).
2. Copy/paste your json keyfile to the job folder.
3. Install dependencies `pip install -r requirements.txt`.
4. Optional. If you want to run the script locally, set up environment variables `CRYPTO`, `JSON_KEYFILE`, `SHEET_ID`, `SHEET_NAME`. Here is a good [blog about env variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).
5. Authenticate smls client: `smls auth <API_KEY>`. You can find `API_KEY` on the [Account page](https://app.seamlesscloud.io/account).
6. Publish your job: `smls publish --name "Update a Google Spreadsheet (BTC)"`. If you want to set up the schedule: `smls publish --name "Update a Google Spreadsheet (BTC)" --schedule "0 0 * * *"`. New to cron schedules? Check this out: [https://crontab.guru/](https://crontab.guru/).
7. Open a job's page and create job parameters. You can change cryptocurrency if you want.
![parameters](../images/crud_gsheet/parameters.png)
7. Click "Run" button. If you set up everything right, you will see a new record in your Google Spreadsheet.

You can find more info here: [https://app.seamlesscloud.io/faq/cli](https://app.seamlesscloud.io/faq/cli) and email us at `hello@seamlesscloud.io`
