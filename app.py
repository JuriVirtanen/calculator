import requests
import csv
from flask import Flask
from flask import render_template, redirect, request

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
data = data[0]['rates']

with open('kursy.csv', 'w', newline='') as plik:
    zapis = csv.writer(plik, delimiter=";")
    for waluta in data:
        zapis.writerow([waluta['currency'], waluta['code'], waluta['bid'], waluta['ask']])

kursy = []
for waluta in data:
    kursy.append({"nazwa": waluta['code'], "kurs": waluta['ask']})

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", kursy = kursy)


@app.route("/calc", methods=["POST"])
def calc():
    oblicz = request.form
    kodw = oblicz.get('kody')
    ilew = oblicz.get('ile')
    for sss in kursy:
        if sss['nazwa'] == kodw:
            koszt = float(sss['kurs'])*int(ilew)
            return f"<p>Koszt zakupu wynosi {round(koszt, 2)} PLN</p>"