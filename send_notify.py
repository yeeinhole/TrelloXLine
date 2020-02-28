import requests

url = "https://notify-api.line.me/api/notify"

#發送line notify的function
def send_notify(token, message):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    
    req = requests.post(url, headers = headers, params = message)
    return req.status_code