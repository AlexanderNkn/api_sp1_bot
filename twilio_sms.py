import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv() 

# Account SID from twilio.com/console
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# Auth Token from twilio.com/console
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# Phone number TO
NUMBER_TO = os.getenv("NUMBER_TO")
# Phone number FROM
NUMBER_FROM = os.getenv("NUMBER_FROM")

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def sms_sender(sms_text):
    message = client.messages.create(
        to=NUMBER_TO,
        from_=NUMBER_FROM,
        body=sms_text
    )
    return message.sid
