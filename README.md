# Hacky-Auth
Authentication bot for hack^2.


# How it works?
When a user fills out a google registration form the data gets sent to a googlesheet, from there a js script is triggered and sends over this data via a http webhook to a mongodb server, 
when mongo detects the request, it triggers another js script that saves the data in mongodb making it accessible for the discord bot. 

# Installation and setup:
* ```git clone https://github.com/Hack-2/Hacky-Auth```
* ```python3 -m pip install -r requirements.txt```
* ```python3 bot.py```
* .env file format:
    ```
    {
      "token" : "DISCORD_TOKEN",
      "mongodb_user" : "MONGODB_USERNAME",
      "mongodb_pass" : "MONGODB_PASSWORD"
    }
  ```

# Commands Available

 
    +===============+=======================================================================================+
    |    Command    |                                      Description                                      |
    +===============+=======================================================================================+
    | !help         | Lists all available commands.                                                         |
    +---------------+---------------------------------------------------------------------------------------+
    | !info         | Lists user's info such as (registration date and workshops attended).                 |
    +---------------+---------------------------------------------------------------------------------------+
    | !plot         | Plots the increase of registered users daily.                                         |
    +---------------+---------------------------------------------------------------------------------------+
    | !verify #CODE | Verifies codes given at workshops to prove attendance and saves them in the database. |
    +---------------+---------------------------------------------------------------------------------------+


# To do
* Send matplotlib graphs about users registrations and attendances. ✅ 
* Add exceptions to pass any possible errors.

