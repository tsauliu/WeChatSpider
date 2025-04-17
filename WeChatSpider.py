# link to browser (how to use pywinauto to control the browser)
# save the links
# deploy to the windows server
   #把hk 服务器改成windows server，host公众号抓取
    # 用JP 或者tw 服务器做总结
#%%
from functions_wechat import *
from functions_edge import *

main_window = open_wechat()
time.sleep(1)

# driver = edge_driver()
EdgeDriver.get("https://www.baidu.com")

# loop through the the page of channels
channels=main_window.descendants(control_type="ListItem")
with open("channels.csv", "w", encoding="utf-8") as f:
    for channel in channels:
        f.write(channel.window_text() + "\n")

# loop through the the articles of one channel
articles = main_window.descendants(control_type="Pane")
with open("articles.csv", "w", encoding="utf-8") as f:
    for article in articles:
        text=article.window_text()
        if len(text)>=5:
            article.click_input()
            scrape_url_to_md(EdgeDriver, "./articles")
            time.sleep(2)
            f.write(text + "\n")
