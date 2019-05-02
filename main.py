"""
Mashup service that gets a random fact and returns it in Pig Latin.
"""

import os
import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """Get random fact from unkno.com"""
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()



def get_page(fact):
    """Translate random fact into Pig Latin and get new url"""
    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    payload = {"input_text": fact}

    r = requests.post(url, data=payload, allow_redirects=False)

    new_page = r.headers["Location"]

    return new_page


def get_translation(new_page):
    response = requests.get(new_page)
    soup = BeautifulSoup(response.content, "html.parser")

    fact = soup.find("body").getText()
    strip_fact = fact.replace("Pig Latin\nEsultray", "")

    return strip_fact


def template():
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
    <h1>Dianna's Pig Latin Fact Mashup</h1><br>
    
    <h2>Original Fact</h2>
    <h3>{}</h3><br>
    
    <h2>Fact in Pig Latin</h2>
    <h3>{}</h3><br>
    
    <h2>Translation Page</h2>
    <h3><a href={}>{}</a></h3>
    
  </body>
</html>  
    """

    return page_template


@app.route('/')
def home():
    fact = get_fact().strip()

    new_page = get_page(fact)

    translation = get_translation(new_page)

    return template().format(fact, translation, new_page, new_page)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
