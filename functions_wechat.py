import time
from pywinauto.application import Application

def open_wechat():
    # 打开微信
    app = Application(backend="uia").connect(path="WeChat.exe")
    main_window = app.window(title="微信")
    main_window.set_focus()

    main_window.child_window(title="聊天").click_input()
    time.sleep(1)

    # 简化后的代码：查找并点击包含特定文本的按钮
    button_texts = ["文件传输助手","SessionListItem", "列表模式"]
    for text in button_texts:
        try:
            for button in main_window.descendants(control_type="Button"):
                if text in button.window_text():
                    button.click_input()
                    break
                    time.sleep(1)
        except Exception as e:
            print(f"点击'{text}'按钮时出错: {e}")
    return main_window

# main_window=open_wechat()
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

# child_window=main_window.child_window(title="电动内参", control_type="ListItem")
# child_window.click_input()
if __name__ == "__main__":
    main_window=open_wechat()
    channels_first=main_window.child_window(title="会话列表", control_type="Pane").descendants(control_type="ListItem")
    first_channel=channels_first[3]
    first_channel.click_input()
    # Simulate pressing the down arrow key to navigate down in the conversation list
    main_window.type_keys("{DOWN}")
    time.sleep(0.5)  # Small delay to allow UI to respond
    main_window.type_keys("{PGDN}")