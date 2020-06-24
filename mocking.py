import random
import os
import slack
from flask import Flask, request

SLACK_TOKEN = os.environ['SLACK_TOKEN']
client = slack.WebClient(token=SLACK_TOKEN)
genghis_id = os.environ['genghis_id']

app = Flask(__name__)


def randomize_caps(text):
    newstring = ':mocking: '
    options = ['upper', 'lower']
    for character in text:
        if newstring[-1].isupper() and newstring[-2].isupper():
            option = 'lower'
        elif newstring[-1].islower() and newstring[-2].islower():
            option = "upper"
        else:
            option = random.choice(options)
        if option == 'upper':
            newstring += character.upper()
        elif option == 'lower':
            newstring += character.lower()
    newstring += ' :mocking:'
    return newstring


def matts_inferior_caps(text):
    newstring = ':mocking: '
    for character in text:
        if newstring[-1].isupper():
            newstring += character.lower()
        else:
            newstring += character.upper()
    newstring += ' :mocking:'
    return newstring


def channel_post(text, icon_url, user_name, channel_id, command):
    if command == "/mocking":
        print(client.chat_postMessage(icon_url=icon_url, username=user_name,
                                      channel=channel_id, text=randomize_caps(text)))
    else:
        print(client.chat_postMessage(icon_url=icon_url, username=user_name,
                                      channel=channel_id, text=matts_inferior_caps(text)))


@app.route('/', methods=['POST'])
def sarcastic():
    print(f"REQUEST INFO IS \n\n {request.form}")
    command = request.form.get("command")
    text = request.form.get('text')
    channel_id = request.form.get('channel_id')
    channel_name = request.form.get('channel_name')
    user_id = request.form.get('user_id')

    print(f"CLIENT INFO IS:\n\n {client.users_info(user=user_id)}")
    user_name = client.users_info(user=user_id)[
        "user"]["profile"]["display_name"]
    if not user_name or user_name.lower() == "sarcasm":
        user_name = client.users_info(user=user_id)["user"]["name"]

    if user_name.lower() == "genghis" and user_id != genghis_id:
        user_name = client.users_info(user=user_id)["user"]["name"]
        try:
            print(client.chat_postEphemeral(channel=channel_id, user=user_id,
                                            text="You try to impersonate ME? With MY BOT? For shame."))
        except:
            pass

    icon_url = client.users_info(user=user_id)["user"]["profile"]["image_512"]

    if channel_name == "directmessage":
        return "Nah bro, the bot can't slide into DMs"
    else:
        channel_post(text, icon_url, user_name, channel_id, command)

    return '', 200
