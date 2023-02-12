import requests
import csv
from flask import Flask
from flask import render_template

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
data = data[0]['rates']

with open('kursy.csv', 'w', newline='') as plik:
    zapis = csv.writer(plik, delimiter=";")
    for waluta in data:
        zapis.writerow([waluta['currency'], waluta['code'], waluta['bid'], waluta['ask']])

kursy = []
for waluta in data:
    kursy.append({"nazwa": waluta['currency'], "kurs": waluta['ask']})

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", kursy = kursy)