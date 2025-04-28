from WeChatSpider import daily_scrape
import datetime
import time

print("Starting the scraper...")
while True:
    if datetime.datetime.now().hour in [10,15,22] and datetime.datetime.now().minute < 10:
        try:
            daily_scrape()
        except Exception as e:
            print(e)
    time.sleep(60)
    print("Waiting for the next run...")
    
