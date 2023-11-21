from flask import Flask, render_template
import requests, math
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route("/")
def lolPsdata():
    url="https://fow.kr/stats"
    response = requests.get(url)

    champData = []

    soup = BeautifulSoup(response.text, 'html.parser')
    for i, tr_tag in enumerate(soup.find_all('tr')):
        position = tr_tag.get('position')
        rname = tr_tag.get('rname')

        champData.append({i: [rname, position]})

    for i, rate in enumerate(soup.find_all('td', class_='td_rate')):
        champData[math.trunc(i/6)+1][i].append(rate)

    return render_template('index.html', champData=champData )


@app.route('/',methods=['GET','POST']) 
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)