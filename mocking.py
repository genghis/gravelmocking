import random
import os
import slack
from flask import Flask, request

SLACK_TOKEN = os.environ['SLACK_TOKEN']
client = slack.WebClient(token=SLACK_TOKEN)

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


@app.route('/', methods=['POST'])
def sarcastic():
    command = request.form.get("command")
    text = request.form.get('text')
    channel_id = request.form.get('channel_id')
    user_id = request.form.get('user_id')
    user_name = client.users_info(user=user_id)["user"]["profile"]["display_name"]
    icon_url = client.users_info(user=user_id)["user"]["profile"]["image_512"]

    if command == "mocking":
        print(client.chat_postMessage(icon_url=icon_url, username=user_name,
                                      channel=channel_id, text=randomize_caps(text)))
    else:
        print(client.chat_postMessage(icon_url=icon_url, username=user_name,
                                      channel=channel_id, text=matts_inferior_caps(text)))

    return '', 200
