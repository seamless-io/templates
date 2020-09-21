# Send daily email with Major World Indices prices

This job sends daily emails with prices of Major World Indices. The data source is [https://finance.yahoo.com/world-indices](https://finance.yahoo.com/world-indices)  

- [Requirements](#requirements)
- [Setting up Gmail](#setting-up-gmail)
- [Setting up SeamlessCloud](#setting-up-seamlesscloud)
- [Running the script]()

## Requirements
1. Python 3.6 or higher
2. Gmail account
3. [SeamlessCloud](http://seamlesscloud.io/) account

## Setting up Gmail
We are going to use Gmail account to send emails. For security reasons, user's Gmail password cannot be used in Python script. Also, we are not going to turn on the [Less Secure App Access](https://support.google.com/accounts/answer/6010255?hl=en) instead, we will enable 2-Step Verification and create an app password.

1. Navigate to [https://myaccount.google.com/](https://myaccount.google.com/) and open the `Security` tab. Then, enable `2-Step Verification` and click `App passwords`.  
    ![My Account](../images/send_daily_email_yfinance/myaccount.png)

2. In the dropdown menu, select `Other (Custom name)` option and name your application, for example `World Indices`.   
    ![Select Other](../images/send_daily_email_yfinance/apps.png)
    
3. Paste somewhere the generated password (to be 100% clear, you will have a different password from the one you see on the screenshot). We are going to use this password in our Python script.  
    ![Password](../images/send_daily_email_yfinance/password.png)


## Setting up SeamlessCloud  
Create a free account at [http://seamlesscloud.io](http://seamlesscloud.io/). Since you already have a Gmail account you will be able to sign up and then log in with your Gmail account.  
![Seamless Sign Up](../images/smls-signup.png)

## Running the script  
You can find this template in our Template library. Just find it in the list and click "Use Template". Then all you need to do is to fill out 3 Parameters: SENDER, RECIPIENT, PASSWORD. That's it! Now click "Run now" and check if it works. If you want to make changes to the code, please download the code and follow this guide https://staging-app.seamlesscloud.io/guide. 
    
![Email](../images/send_daily_email_yfinance/email.png)
