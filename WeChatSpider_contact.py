# link to browser (how to use pywinauto to control the browser)
# save the links
# deploy to the windows server
   #把hk 服务器改成windows server，host公众号抓取
    # 用JP 或者tw 服务器做总结
#%%
import os
from functions_wechat import *
# from functions_edge import *
from database_mgmt import read_articles_to_dataframe,setup_database
from parameters import friday_date

setup_database()
markdown_dir=f"./data/articles/{friday_date}/"
os.makedirs(markdown_dir, exist_ok=True)

# #%%

# print("Starting in 3 seconds...please move your mouse alway")
# time.sleep(3)
# print("Starting to scrape data now!")

# main_window = open_wechat()
app = Application(backend="uia").connect(path="WeChat.exe")
main_window = app.window(title="微信")
main_window.set_focus()
main_window.child_window(title="通讯录").click_input()

[button for button in main_window.descendants(control_type="Button") if button.window_text()=='ContactListItem'][-1].click_input()

with open("window_controls.txt", "w", encoding="utf-8") as f:
    # 临时将标准输出重定向到文件
    import sys
    sys.stdout = f
    main_window.print_control_identifiers()
    sys.stdout = sys.__stdout__  # 恢复标准输出

[button for button in main_window.descendants(control_type="Button") if button.window_text()=='ContactListItem']
# main_window.child_window(title="公众号", control_type="Text").click_input()
