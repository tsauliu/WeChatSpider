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
os.makedirs("./articles", exist_ok=True)

main_window = open_wechat()
time.sleep(1)

channel_section=main_window.child_window(title="会话列表", control_type="Pane")
channels=channel_section.descendants(control_type="ListItem")

update_articles_for_each_channel=2
for channel in channels:
    channel_scraped=channel.window_text()

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

    first_article_scraped=False
    article_count=0
    for article in articles:
        article_title=article.window_text()
        if len(article_title)>=5: 
            if article_title in articles_scraped and first_article_scraped:
                print(f"Article {article_title} already scraped, skipping...")
            else:
                print(f"Scraping article {article_title}...")
                article.click_input()
                time.sleep(3)
                scrape_url_to_md(EdgeDriver, "./articles",channel_scraped,article_title)
                time.sleep(2)
                first_article_scraped=True

            article_count+=1
            if article_count>=update_articles_for_each_channel:
                break
            time.sleep(1)
            mouse.scroll(coords=get_mouse_position(), wheel_dist=-1)
    
    child_window=main_window.child_window(title=channel_scraped, control_type="ListItem")
    child_window.click_input()
    mouse.scroll(coords=get_mouse_position(), wheel_dist=-1)
    time.sleep(1)
    
