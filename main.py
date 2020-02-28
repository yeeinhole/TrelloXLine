import requests
import json
import datetime as dt
import send_notify as line
import configparser
import sys
import time

#啟動時間
start_time = time.time()

#使用ConfigParser套件讀入組態檔
conf = configparser.ConfigParser()
#載入組態檔
conf.read("config.ini", encoding="utf-8")

#Trello Key & Token
key = conf.get('Trello' , 'key')
token = conf.get('Trello' , 'token')
board = conf.get('Trello' , 'board')

#line token
line_token = conf.get('Line' , 'line_token')
#line nptify url
url_notify = conf.get('Url' , 'notify')

url = "https://api.trello.com/1/boards/"+board+"/lists"

querystring = {"cards":"open",
                "card_fields":["due","dueComplete"],
                "filter":"open",
                "fields":"name",
                "key":key,
                "token":token}

#取得board裡的卡片清單
req = requests.request("GET", url, params=querystring)
if not req.ok:
    print("Get list error, http code="+str(req.status_code)+", error msg="+req.text)
    sys.exit()

card_lists = json.loads(req.text)
# print(card_lists)

today = dt.datetime.now()
checkday = dt.datetime.now()
oneday = dt.timedelta(days = 1)
#計算出週日的日期
while checkday.isoweekday() != 7:
    checkday += oneday

#今天距離週日還有幾天
lessday = checkday - today

#轉成文字才能與Trello比對
checkday = checkday.strftime("%Y-%m-%d")

finish_users = []
not_finish_users = []
#偵測卡片的due date有沒有截止日的
for lists in card_lists:
    finish = False
    for card in lists['cards']:
        #卡片沒設定due的話跳過這一張卡片
        if card['due'] == None:
            continue 
        
        #抓卡片的due date 跟 是否打勾
        if (checkday == card['due'].split('T')[0]) and (card['dueComplete']):
            finish = True
            break
    
    #紀錄該週完成與未完成的人
    if not finish:
        # print("send notify to "+lists['name'])
        not_finish_users.append(lists['name'])
    else:
        finish_users.append(lists['name'])

#製作訊息
message = {'message': "\n"
    "Hi 各位安安 \n"+
    "--- \n"+
    "本週已完成的人： \n"+
    ("，".join(finish_users))+"\n"+
    "請下週再接再厲～～\n"+
    "--- \n"+
    "本週未完成的人： \n"+
    ("，".join(not_finish_users))+"\n"+
    "距離本周截止你只剩下"+str(lessday.days)+"天了～～ \n"+
    "趕快去寫文章！！ \n"+
    "--- \n"+
    "投稿連結： \n"+
    "https://forms.gle/MvufZiucPir4yhHb6"
}

#發送訊息
line.send_notify(line_token, message)
if(req.status_code == 200):
    print("Job Success!! "+str(time.time() - start_time))
else:
    print("Line Notify Error, http code="+str(req.status_code)+", error msg="+req.text)