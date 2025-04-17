# link to browser (how to use pywinauto to control the browser)
# save the links
# deploy to the windows server
   #把hk 服务器改成windows server，host公众号抓取
    # 用JP 或者tw 服务器做总结
#%%
from functions_wechat import *
from functions_edge import *
from database_mgmt import read_articles_to_dataframe,setup_database

setup_database()

main_window = open_wechat()
time.sleep(1)

# loop through the the page of channels
channels=main_window.descendants(control_type="ListItem")
with open("channels.csv", "w", encoding="utf-8") as f:
    for channel in channels:
        f.write(channel.window_text() + "\n")

channel_scraped="自动驾驶之心"
child_window=main_window.child_window(title=channel_scraped, control_type="ListItem")
child_window.click_input()
time.sleep(1)
 # Scroll down 2 units using current position
# 向下滚动聊天窗口2个单位


articles_df = read_articles_to_dataframe()
c1=articles_df['channel_scraped']==channel_scraped
articles_scraped=articles_df[c1]['article_title'].to_list()
# loop through the the articles of one channel
articles = main_window.descendants(control_type="Pane")
with open("articles.csv", "w", encoding="utf-8") as f:
    for article in articles:
        article_title=article.window_text()
        if len(article_title)>=5: 
            if article_title in articles_scraped:
                print(f"Article {article_title} already scraped, skipping...")  
                continue
            else:
                article.click_input()
                time.sleep(3)
                scrape_url_to_md(EdgeDriver, "./articles",channel_scraped,article_title)
                time.sleep(2)
            f.write(article_title + "\n")
            time.sleep(1)
            mouse.scroll(coords=get_mouse_position(), wheel_dist=-1)
