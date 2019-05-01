"""
Mashup service that gets a random fact and returns it in Pig Latin.
"""

import os
import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"

payload = {}


def get_fact():
    """Get random fact from unkno.com"""
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


def translate(fact):
    """Send random fact and get url for Pig Latin translation"""
    payload = {"input_text": fact}

    r = requests.post(url, data=payload, allow_redirects=False)

    new_page = r.headers["Location"]

    return new_page


@app.route('/')
def home():
    fact = get_fact().strip()

    pig_fact = translate(fact)

    pig_link = f"<a href={pig_fact}>{pig_fact}</a>"

    return pig_link


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
