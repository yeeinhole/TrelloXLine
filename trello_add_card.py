import requests
import json
import datetime as dt
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
list_name = conf.get('Trello' , 'list_name').split(',')

url_get_border = conf.get('Url' , 'get_border')+board
url_add_list = conf.get('Url' , 'add_list')
url_add_card = conf.get('Url' , 'add_card')

body = {
    "actions":"all",
    "key":key,
    "token":token
}

req = requests.request("GET", url_get_border, params=body)

if not req.ok:
    print("Get botder error, http code="+str(req.status_code)+", error msg="+req.text)
    sys.exit()

board_info = json.loads(req.text)
board_id = board_info['id']


sevenday = dt.timedelta(days = 7)
startday = dt.datetime(2020, 2, 9, 0, 0)
finalday = dt.datetime(2021, 1, 4, 0, 0)

for i in list_name:
    
    body = {
        "name":i,
        "idBoard":board_id,
        "key":key,
        "token":token
    }
    req = requests.request("POST", url_add_list, params=body)

    if not req.ok:
        print("Add list error, http code="+str(req.status_code)+", error msg="+req.text)
        sys.exit()

    new_list_info = json.loads(req.text)
    new_list_id = new_list_info['id'] 
    
    #初始化日期與數量
    day = startday
    count = 1
    while day < finalday:

        querystring = {
            "idList":new_list_id,
            "name":"##"+str(count),
            "keepFromSource":"all",
            "due":day,
            "key":key,
            "token":token
        }

        req = requests.request("POST", url_add_card, params=querystring)

        if not req.ok:
            print("Add cards error, http code="+str(req.status_code)+", error msg="+req.text)
            sys.exit()

        day = day+sevenday
        count+=1
    
print("Job Success!! "+str(time.time() - start_time))