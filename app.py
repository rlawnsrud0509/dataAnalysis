from flask import Flask, render_template
import requests, json
from bs4 import BeautifulSoup
import plotly.graph_objs as go

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
    champDataArray = str(champData_json).split("[")

    for i in range(len(champDataArray)):
        champDataArray[i] = champDataArray[i].split(",")
        if len(champDataArray[i]) == 10:
            data = champDataArray[i][5] + champDataArray[i][6]
            champDataArray[i][5] = data

    for i in range(len(champDataArray)):
        for j in range(len(champDataArray[i])):
            champDataArray[i][j] = champDataArray[i][j].replace('"', "")
            champDataArray[i][j] = champDataArray[i][j].replace('"', "")
            champDataArray[i][j] = champDataArray[i][j].replace(" ", "")
        champDataArray[i] = champDataArray[i][:6]

    champDataArray = champDataArray[3:]
        
    print(champDataArray)

    names = [item[0] for item in champDataArray]
    
    win_rates = [float(item[2].strip('%')) for item in champDataArray]
    pick_rates = [float(item[3].strip('%')) for item in champDataArray]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=win_rates,
        y=pick_rates,
        mode='markers+text', 
        text=names,  
        textposition='top center',  
        marker=dict(size=6, color='white'),  
    ))

    fig.update_layout(
        title='챔피언의 승률과 픽률에 따른 산점도',
        xaxis=dict(title='승률'),
        yaxis=dict(title='픽률'),
        font=dict(color='white'), 
        plot_bgcolor='black', 
    )

    fig.show()


    return render_template('index.html', champData=champData_json )

@app.route('/',methods=['GET','POST']) 
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)