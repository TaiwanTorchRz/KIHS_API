import io
# from selenium import webdriver
# from selenium.webdriver.edge.options import Options
import time
from bs4 import BeautifulSoup
import requests
import json

items_number = 50
# options = Options()
# options.set("--disable-notifications")
# options.add_argument("--disable-notifications")
headers = {
 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
# edge = webdriver.Edge('./msedgedriver.exe')

# edge.get("https://groups.google.com/a/ksvs.kh.edu.tw/g/honor")
# edge.get('https://groups.google.com/a/ksvs.kh.edu.tw/forum/feed/news/msgs/rss.xml?num=100')
r = requests.get("https://groups.google.com/a/ksvs.kh.edu.tw/forum/feed/news/msgs/rss.xml?num="+str(items_number),headers=headers)
# soup = BeautifulSoup(edge.page_source , 'html.parser')
soup = BeautifulSoup(r.text, 'html.parser')
# items_number = soup.find('div',{'class':'aEb7Ed'})
# items_number = items_number.getText().split(' ')[-1]
titles = soup.find_all('title')
sub_titles = soup.find_all('description')    
urls = soup.find_all('guid')

authors = soup.find_all('author')

len_ = range((int)(items_number))
# print("共有"+str(items_number)+"個物品")

resoult = [[0]*8 for i in range((int)(items_number))]
def getitems():
    for i in range((int)(items_number)):
        resoult[i][0] = i
    counter = 0
    for i in range(0, (int)(len(titles))):
        if i!= 0:
            print(titles[i].getText())
            resoult[counter][1] = (titles[i].getText())
            counter = counter +1
        
    counter = 0
    for i in range(0, (int)(len(sub_titles))):
        if i!= 0:
            print(sub_titles[i].getText())  
            resoult[counter][2] = (sub_titles[i].getText())
            counter = counter+1
    counter = 0   
    for i in range(0, (int)(len(authors))):
        print(authors[i].getText())  
        resoult[counter][4] = (authors[i].getText())
        counter = counter+1 
    counter = 0
    for i in range(0, (int)(len(urls))):
        if True:
            print('正在處理..'+str(urls[i].getText()).replace('/d/topic/news/','/g/news/c/'))
            print("counter: " + (str(counter)))
            resoult[counter][5] = (str(urls[i].getText()).replace('/d/topic/news/','/g/news/c/'))
            getDetails(resoult[counter][5],counter)
            counter = counter + 1
        # print(urls[i].getText())

def getDetails(url,index):
    r = requests.get(url,headers=headers)
    detials_html = BeautifulSoup(r.text , 'html.parser')
    time = detials_html.find_all('span',{'class':'zX2W9c'})
    resoult[index][3] = time[0].getText()

    contents = detials_html.find_all('div', {'class': 'L8sBDd'})
    resoult[index][6] = str(contents)[1:-1]
    files = detials_html.find_all('div', {'class': 'E3gXse'}) #c2eF9b
    resoult[index][7] = list()
    for item in files:
        url = str(item.get('data-view-attachment-url'))
        file_name= str(item.get('aria-label')[14:])
        resoult[index][7].append([str(file_name),str(url)])
        print("label:"+str(item.get('aria-label')[14:]))#移除Download FIle字樣 中文可能是"下載檔案"
        print("url:"+str(item.get('data-view-attachment-url')))
        # print(resoult[index][6])


# print(resoult[0])
# for item in resoult:
#     print(item)
def updateNews():
    getitems()
    j = json.dumps(resoult,ensure_ascii=False)
    with io.open('json/news.json', mode='w', encoding='utf8') as json_file:
        json.dump(resoult, json_file, ensure_ascii=False)

def getJson():
    
    with io.open('json/news.json', mode='r', encoding='utf8') as json_file:
        
        return json.load(json_file)

        