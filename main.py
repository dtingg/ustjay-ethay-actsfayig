"""
Mashup service that gets a random fact and returns it in Pig Latin.
"""

import os
import requests
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """
    Get a random fact from unkno.com
    :return: string of a random fact
    """
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    fact = facts[0].getText()

    # Fix weird formatting
    fact = fact.replace("â€™", "'").replace("â€œ", '"').replace('â€”', "—").replace("â€", '"')

    return fact


def get_page(fact):
    """
    Translate fact into Pig Latin and get new url
    :param fact: string
    :return: url for translation page
    """
    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    payload = {"input_text": fact}

    r = requests.post(url, data=payload, allow_redirects=False)
    new_page = r.headers["Location"]

    return new_page


def get_translation(new_page):
    """
    Get the Pig Latin translation
    :param new_page: url of translation
    :return: string of translation
    """
    response = requests.get(new_page)
    soup = BeautifulSoup(response.content, "html.parser")

    fact = soup.find("body").getText()
    strip_fact = fact.replace("Pig Latin\nEsultray", "")

    return strip_fact


def template():
    """
    HTML formatting for home page
    :return: HTML template
    """
    page_template = """
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <title>Dianna's Pig Latin Fact Mashup</title>
  </head>
  <body>
  <div class="p-4 container-fluid">
    <h1>Dianna's Pig Latin Fact Mashup</h1><br>    
    <div class="card-deck">
    <div class="card">
        <img src="https://res.cloudinary.com/hfamjelvo/image/upload/v1556828209/fact_mnwyra.jpg" class="card-img-top" alt="hashtag fact">
        <div class="card-body">
        <h5 class="card-title">Random Fact</h5>
        <p class="card-text">{}</p>
        <a class="btn btn-secondary" href="/" role="button">Get another fact</a>
        </div>
    </div>
    <div class="card">
        <img src="https://res.cloudinary.com/hfamjelvo/image/upload/v1556828209/code_ssq7xp.jpg" class="card-img-top" alt="computer code">
        <div class="card-body">
        <h5 class="card-title">Translation Page</h5>
        <p class="card-text">{}</p>
        <a class="btn btn-secondary" href="{}" role="button">Go to translation</a>
        </div>
    </div>
    <div class="card">
        <img src="https://res.cloudinary.com/hfamjelvo/image/upload/v1556828209/pig_embakq.jpg" class="card-img-top" alt="pig">
        <div class="card-body">
        <h5 class="card-title">Fact in Pig Latin</h5>
        <p class="card-text">{}</p>
        <a class="btn btn-secondary" href="https://en.wikipedia.org/wiki/Pig_Latin" role="button">Learn about Pig Latin</a>
        </div>
    </div>
    </div>
    <br>
    <br>
  </body>
</html>  
    """

    return page_template


@app.route('/')
def home():
    """
    Web app home page
    :return: random fact, translation url, Pig Latin translation
    """
    fact = get_fact().strip()

    new_page = get_page(fact)

    translation = get_translation(new_page)

    return template().format(fact, new_page, new_page, translation)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
