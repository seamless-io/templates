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

After obtaining a json keyfile, create a Google Spreadsheet and share it with `client_email` from the json keyfile. Set permissions `Editor`.  
Before running the script, rename the current sheet to `crypto`. You can choose any name you want, but remember to update a corresponding environment variable as well.

## Setting up SeamlessCloud
Create a free account at [http://seamlesscloud.io](http://seamlesscloud.io/).
You can find this script in our [Templates Library](https://app.seamlesscloud.io/templates). You can try it out right in the browser, no need to do anything in your local environment. The Template is called "Collect Bitcoin price into a Google Spreadsheet".
You can find more info here: [https://app.seamlesscloud.io/faq/cli](https://app.seamlesscloud.io/faq/cli) and email us at `hello@seamlesscloud.io`
