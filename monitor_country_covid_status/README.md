# Monitor country's COVID situation and decide when it's safe to travel

This job sends daily Whatsapp messages with COVID confirmed cases data and gives traveling recommendation. The data source is [https://covid19api.com/](https://covid19api.com/)  

- [Requirements](#requirements)
- [Setting up Twilio](#setting-up-twilio)
- [Setting up SeamlessCloud](#setting-up-seamlesscloud)
- [Running the script]()

## Requirements
1. Python 3.6 or higher
2. WhatsApp free account
3. Twilio free account
4. [SeamlessCloud](http://seamlesscloud.io/) free account

## Setting up Twilio
We are going to use Twilio account to send messages to Whatsapp. 

1. Navigate to [https://www.twilio.com/](https://www.twilio.com/), Sign up, verify your email and phone number.
    ![Sign Up](../images/monitor_country_covid_status/1.png)

2. Choose yes on the "Do you write code?" screen.   
    ![Do you write code?](../images/monitor_country_covid_status/2.png)
    
3. Choose Python on the "What is your preferred language?" screen.   
    ![What is your preferred language?](../images/monitor_country_covid_status/3.png)
    
4. Choose "Use Twilio in a project" on the "What is your goal today?" screen.   
    ![What is your goal today?](../images/monitor_country_covid_status/4.png)
    
5. Choose "Send WhatsApp messages" on the "What do you want to do first?" screen.   
    ![What do you want to do first?](../images/monitor_country_covid_status/5.png)
    
6. Twillio asks you if you want to activate the Sandbox. Agree and click "Confirm".   
    ![activate the Sandbox](../images/monitor_country_covid_status/6.png)
    
7. Now Twilio wants you to connect your WhatsApp account. Please follow the instructions.
    ![connect your WhatsApp account](../images/monitor_country_covid_status/7.png)
    
8. Next, pick the option "Send a One-Way WhatsApp Message". On this screen, you will find your account ID and AuthToken. That is all we need in our Python script to send a message to WhatsApp. Please update the variables `account_sid` and `auth_token` in the script to actual values from your account.
    ![Send a One-Way WhatsApp Message](../images/monitor_country_covid_status/8.png)


## Setting up SeamlessCloud  
Create a free account at [http://seamlesscloud.io](http://seamlesscloud.io/).  
![Seamless Sign Up](../images/smls-signup.png)

## Running the script  
Follow instructions to run and publish your first test job. 
![Seamless Sign Up](../images/seamless_no_jobs_screen.png)

You can also check out the [Quick Start Guide](https://app.seamlesscloud.io/guide). When you will be done with testing, copy/paste files from this folder to yours.    

We are almost there! Run our script on the SeamlessCloud: `smls run`. If you set up everything correctly, you will receive a message in WhatsApp. And finally, let's deploy our script to execute it on schedule, say 9 AM every day (UTC time): `smls publish --name "Japan COVID Status" --schedule "0 9 * * *"` (of course, if you want to pick another country, feel free to name your Job accordingly). If you are new to cron schedule, check this service [https://crontab.guru](https://crontab.guru/). 
    
![Email](../images/monitor_country_covid_status/9.jpeg)
