from WeChatSpider import daily_scrape
import datetime
import time

import requests,json
def status_message(msg):
    payload_message = {
        "msg_type": "text",
        "content": {
            "text": msg+' \n'+str(datetime.datetime.now())[:19]
            }
        }
    headers = {
        'Content-Type': 'application/json'
    }
    # webhook地址
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/36473a8e-3bf1-40bd-9115-3385e314bf74"
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload_message))
    return response


print("Starting the scraper...")
while True:
    if datetime.datetime.now().hour in [10,17,22] and datetime.datetime.now().minute < 10:
        try:
            status_message(f"Starting the scraper at {datetime.datetime.now().hour}:{datetime.datetime.now().minute}")
            daily_scrape()
            status_message(f"Scraper finished at {datetime.datetime.now().hour}:{datetime.datetime.now().minute}")
        except Exception as e:
            print(e)
            status_message(f"Error: {e}")
    print(f"Waiting for the next run at {datetime.datetime.now().hour}:{datetime.datetime.now().minute}")
    time.sleep(60)
    
