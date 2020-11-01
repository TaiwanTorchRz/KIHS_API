import time
from API import news,race,honor,learning,personal,parent
import threading
from datetime import datetime
from flask import Flask,jsonify
from flask_cors import CORS
        
updatetime= ""

def fun_news():
    news.updateNews()
def  fun_race():
    race.updateNews()
def fun_honor():
    honor.updateNews()
def fun_learning():
    learning.updateNews()
def fun_personal():
    personal.updateNews()
def fun_parent():
    parent.updateNews()

def getData():
    while True: 
        threading_news = threading.Thread(target=fun_news,name='news')
        threading_race = threading.Thread(target=fun_race,name='race')
        threading_honor = threading.Thread(target=fun_honor,name='honor')
        threading_learning = threading.Thread(target=fun_learning,name='learning')
        threading_personal = threading.Thread(target=fun_personal,name='personal')
        threading_parent = threading.Thread(target=fun_parent,name='parent')
        threading_news.start()
        threading_race.start()   
        threading_honor.start()
        threading_learning.start()
        threading_personal.start()
        threading_parent.start()
        threading_news.join()
        threading_race.join()
        threading_honor.join()
        threading_learning.join()
        threading_personal.join()
        threading_parent.join()
        global updatetime
        updatetime = (str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
        print("最後更新時間 "+ str(updatetime))
        time.sleep(10*60) #10 minutes

threading_getData = threading.Thread(target=getData)
print("啟動網頁伺服器")

app = Flask(__name__)

CORS(app, resources={r"/.*": {"origins": ["https://www.ksvs.kh.edu.tw","http://www.ksvs.kh.edu.tw"]}}) 
app.config['JSON_AS_ASCII'] = False 

@app.route('/honor')
def route_honor():
    
    return jsonify(honor.getJson())
@app.route('/news')
def route_news():
    return jsonify(news.getJson())

    
@app.route('/learning')
def route_learing():
    return jsonify(learning.getJson()) 

@app.route('/parent')
def route_parent():
    return jsonify(parent.getJson()) 

@app.route('/personal')
def route_personal():
    return jsonify(personal.getJson()) 
    
@app.route('/race')
def route_race():
    return jsonify(race.getJson())   

@app.route('/')
def index():
    return updatetime

   

if __name__ == '__main__':
    
    threading_getData.start()
    app.run(port=80,host="0.0.0.0")