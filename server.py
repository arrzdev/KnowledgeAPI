import re
from unidecode import unidecode
import wikipedia
import requests
import json

from flask import Flask

import json
import waitress
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "alive"

@app.route("/<topic>")
def get(topic):
    return knowledgeProcess(sentence=topic)

def knowledgeProcess(sentence=None):

    try:
        wikipedia_data = wikipediaGet(topic=sentence)

        if wikipedia_data:
            #if we have wikipedia data
            return {"status": "ok", "data": wikipedia_data}

        else:
            #try duckduckgo before quitting

            duck_sentence_data = duckGetSentence(sentence=sentence)
            if duck_sentence_data:
                return {"status": "ok", "data": duck_sentence_data}
            else:
                return {"status": "ok", "data": "I did not find anything about that"}
    except:
        return {"status": "error"}

def wikipediaGet(topic=None):
    try:
        wikipedia_response = unidecode(wikipedia.summary(topic, sentences=2))
        removed_audio_label = wikipedia_response.replace(" (listen)", "")
        removed_junk = re.sub(r'\([^)]*\)', '', removed_audio_label)
        cleaned = removed_junk.replace("    ", " ").replace("   ", " ").replace("  ", " ")
        return cleaned.replace(";", ".")

    except:
        return False

def duckGetSentence(sentence=None):
    sentence_return = requests.get(f"https://api.duckduckgo.com/?q={sentence}&format=json&skip_disambig=1&no_html=1")

    if sentence_return.status_code == 200:
        sentence_data = json.loads(sentence_return.text)
        return sentence_data["Abstract"].replace(";", ".")
    else:
        return False

def duckGetTopic(topic=None):
    #TOPIC
    topic_return = requests.get(f"https://api.duckduckgo.com/?q={topic}&format=json&skip_disambig=1&no_html=1")

    if topic_return.status_code == 200:
        topic_data = json.loads(topic_return.text)
        return topic_data["Abstract"].replace(";", ".")
    else:
        return False


if __name__ == '__main__':
    os.system('title ServerLogs')
    #app.run(host='0.0.0.0', port="33507")

    #PRODUCTION
    port = int(os.environ.get('PORT', 5500))
    waitress.serve(app, port=port)