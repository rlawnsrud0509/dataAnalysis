from flask import Flask, render_template
import requests, json
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route("/")
def lolPsdata():
    url="https://fow.kr/stats"
    response = requests.get(url)

    champData = []
    array= []
    rateArray = []

    soup = BeautifulSoup(response.text, 'html.parser')

    for i, rate in enumerate(soup.find_all('td', class_='td_rate'), start=0):
        rateArray.append(rate.text)
        if (i+1) % 6 == 0:
            array.append(rateArray)
            rateArray = []

    for i, tr_tag in enumerate(soup.find_all('tr'), start=0):
        position = tr_tag.get('position')
        rname = tr_tag.get('rname')

        champData.append([rname, position, *array[i-1]])

    champData_json = json.dumps(champData)

    return render_template('index.html', champData=champData_json )

@app.route('/',methods=['GET','POST']) 
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)