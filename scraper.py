import requests, bs4, sys, re, json, flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


res = requests.get('https://en.wikipedia.org/wiki/' + ' '.join(sys.argv[1:]))
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'html.parser')

links = soup.find_all('a', attrs={'href': re.compile("^/wiki")})


dicts = []


for link in links:
    linkDict = {}
    linkDict['title'] = link.get('title')
    linkDict['link'] = "https://en.wikipedia.org" + (link.get('href'))

    dicts.append(linkDict)

    with open('data.json', 'a') as outfile:
        json.dump(linkDict, outfile, indent=4)


@app.route('/links', methods=['GET'])
def get():
    return jsonify(dicts)


app.run()
