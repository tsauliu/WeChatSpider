# link to browser (how to use pywinauto to control the browser)
# save the links
# deploy to the windows server
   #把hk 服务器改成windows server，host公众号抓取
    # 用JP 或者tw 服务器做总结
#%%
from functions_wechat import *
from functions_edge import *
from database_mgmt import read_articles_to_dataframe,setup_database
from parameters import friday_date

setup_database()
markdown_dir=f"./data/articles/{friday_date}/"
os.makedirs(markdown_dir, exist_ok=True)

#%%

print("Starting in 3 seconds...please move your mouse alway")
time.sleep(3)
print("Starting to scrape data now!")

main_window = open_wechat()
time.sleep(1)
update_articles_for_each_channel=20 # 每个公众号抓取30篇文章
channels_done=[]

def scrape_channel(channel_scraped):
    print(f"Scraping channel: {channel_scraped}")
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
    article_loop_count=0
    for article in articles:
        article_title=article.window_text()
        if len(article_title)>=5:
            try: 
                if article_title in articles_scraped and first_article_scraped:
                    print(f"{channel_scraped}: Article {article_title} already scraped, skipping...")
                else:
                    print(f"{channel_scraped}: Scraping article {article_title}...")
                    article.click_input()
                    time.sleep(3)
                    result=scrape_url_to_md(EdgeDriver, markdown_dir,channel_scraped,article_title)
                    if not result:
                        main_window.type_keys("{PGDN}")
                        article.click_input()
                        time.sleep(3)
                        result=scrape_url_to_md(EdgeDriver, markdown_dir,channel_scraped,article_title)
                    time.sleep(2)
                    first_article_scraped=True

                article_count+=1
                if article_count>=update_articles_for_each_channel:
                    break
            except Exception as e:
                print(f"{channel_scraped}: Error scraping article {article_title}: {e}")
            time.sleep(1)
            main_window.type_keys("{DOWN}")
            article_loop_count+=1
            # if article_loop_count>=3:
            #     main_window.type_keys("{PGDN}")
            #     article_loop_count=0
            #     time.sleep(1)
    
    child_window=main_window.child_window(title=channel_scraped, control_type="ListItem")
    try:
        child_window.click_input()
    except:
        print(f"{channel_scraped}: Error clicking on child window")
    time.sleep(1)


# move to the top of channel list
channels_first=main_window.child_window(title="会话列表", control_type="Pane").descendants(control_type="ListItem")
first_channel=channels_first[3]
first_channel.click_input()
main_window.type_keys("{PGUP}")
main_window.type_keys("{PGUP}")
channels_first=main_window.child_window(title="会话列表", control_type="Pane").descendants(control_type="ListItem")
channels_first=[channel.window_text() for channel in channels_first]
print(channels_first)

for i in range(10):
    print(f"Scraping the {i+1}th time")
    try:
        for channel_scraped in channels_first:
            if len(channel_scraped)<3 or channel_scraped in channels_done:
                continue
            scrape_channel(channel_scraped)
            channels_done.append(channel_scraped)
            child_window=main_window.child_window(title=channel_scraped, control_type="ListItem")
            close_mp_weixin_tab(EdgeDriver)
            child_window.click_input()
            time.sleep(1)
            main_window.type_keys("{DOWN}")

        main_window.type_keys("{PGDN}")
        channels_new=main_window.child_window(title="会话列表", control_type="Pane").descendants(control_type="ListItem")
        channels_new=[channel.window_text() for channel in channels_new]
        newchannels=[channel for channel in channels_new if channel not in channels_first]
        print(newchannels)

        for channel_scraped in newchannels:
            if len(channel_scraped)<3 or channel_scraped in channels_done:
                continue
            scrape_channel(channel_scraped)
            channels_done.append(channel_scraped)
            child_window=main_window.child_window(title=channel_scraped, control_type="ListItem")
            close_mp_weixin_tab(EdgeDriver)
            child_window.click_input()
            time.sleep(1)
            main_window.type_keys("{DOWN}")
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
        continue