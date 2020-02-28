import requests
import json
import datetime

lineToken = 'YOU_TOKEN'
lineUrl = 'https://notify-api.line.me/api/notify'
lineHeader = {
    'Authorization': 'Bearer ' + lineToken
}
lineMsg = {
    'message': '今天沒有匯率資訊喔',
    'stickerPackageId': '1',
    'stickerId': '107'
}

today = str(datetime.date.today())
# today = '2020-02-24' #for testing
startAt = str(datetime.date.today() - datetime.timedelta(days=20))

allUrl = "https://unionpayintl-3231d.firebaseio.com/MOP-TWD.json?print=pretty&orderBy=\"$key\"&startAt=\"" + startAt + "\""
todayUrl = "https://unionpayintl-3231d.firebaseio.com/MOP-TWD/" + today + ".json"


rates = json.loads(requests.get(allUrl).text)
today = json.loads(requests.get(todayUrl).text)

highest = {
    'Date': '',
    'Rate': 0
}

for rate in rates:
    if(rates[rate]['Rate'] > highest['Rate']):
        highest = rates[rate]

if today:
    if today['Rate'] >= highest['Rate']:
        lineMsg['message'] = '該換錢囉, 今天匯率為: ' + \
            str(today['Rate'])
        lineMsg['stickerId'] = '14'
    else:
        lineMsg['message'] = '今天匯率為: ' + str(today['Rate'])
        lineMsg['stickerId'] = '104'

requests.request("POST", lineUrl, headers=lineHeader, data=lineMsg)
