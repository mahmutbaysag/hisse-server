import requests
import json
from bs4 import BeautifulSoup
from flask import Flask

URL = "https://finans.mynet.com/borsa/hisseler"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


tablo = soup.table
satirlar = tablo.find_all("tr")

veriler = []

for i in satirlar[1:]:
    print(i)
    hucreler = i.find_all("td")
    degisim = hucreler[3].string 
    if float(degisim.replace(",","."))<=1:
        satir = {
            "ad":str(hucreler[0].text).replace("\n",""),
            "sonfiyat":hucreler[2].string,
            "degisim":hucreler[3].string,
            "hacim":hucreler[4].string}
        veriler.append(satir)

def myFunc(e):
    return e['degisim']    

veriler.sort(reverse=True,key=myFunc)

app = Flask(__name__)

@app.route("/hisseler")
def hisseler():
    
    return json.dumps({"hisseler" : veriler})
    #return {"members":["member1","member2","member3"]}

if __name__ == "__main__":
    app.run(debug=True)


