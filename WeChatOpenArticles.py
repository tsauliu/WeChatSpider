# link to browser (how to use pywinauto to control the browser)
# save the links
# deploy to the windows server
   #把hk 服务器改成windows server，host公众号抓取
    # 用JP 或者tw 服务器做总结
#%%
import time
from pywinauto.application import Application

# 打开微信
app = Application(backend="uia").connect(path="WeChat.exe")
main_window = app.window(title="微信")
main_window.set_focus()

# 点击通讯录
# main_window.child_window(title="消息").click_input()
# time.sleep(1)

# 简化后的代码：查找并点击包含特定文本的按钮
button_texts = ["SessionListItem", "列表模式"]
for text in button_texts:
    try:
        for button in main_window.descendants(control_type="Button"):
            if text in button.window_text():
                button.click_input()
                break
                time.sleep(1)
    except Exception as e:
        print(f"点击'{text}'按钮时出错: {e}")

# with open("window_controls.txt", "w", encoding="utf-8") as f:
#     # 临时将标准输出重定向到文件
#     import sys
#     sys.stdout = f
#     main_window.print_control_identifiers()
#     sys.stdout = sys.__stdout__  # 恢复标准输出

# target_article = main_window.child_window(
#     title="沃尔沃全新XC90正式上市",
#     control_type="Pane"
# )

# target_article.click_input()

time.sleep(2)

# child_window=main_window.child_window(title="梁中华宏观研究", control_type="ListItem")
# child_window.click_input()
# main_window.type_keys("{PGDN}")

channels=main_window.descendants(control_type="ListItem")
# 将按钮文本写入外部文件
with open("channels.csv", "w", encoding="utf-8") as f:
    for channel in channels:
        f.write(channel.window_text() + "\n")

articles = main_window.descendants(control_type="Pane")

# 若只要控件名列表
with open("articles.csv", "w", encoding="utf-8") as f:
    for article in articles:
        text=article.window_text()
        if len(text)>=5:
            article.click_input()
            f.write(text + "\n")












