'''
# 设置Edge 浏览器
1. 需要提前将Edge浏览器的启动路径设置成:
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9223 --profile-directory=Default
2. 然后关掉所有Edge 浏览器的进程, 重启Edge 浏览器
3. 如果打开127.0.0.1:9223, 没有报错，则设置成功

# 设置Edge drvier
下载driver
https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver?form=MA13LH
最好32位和64位都下载, 尝试哪个可以work
'''
#%%
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time

edge_options = Options()
edge_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")

# # EdgeDriver 路径，有些情况下可以不用写
service = Service(executable_path="C:/edgedriver_win32/msedgedriver.exe")

driver = webdriver.Edge(service=service, options=edge_options)

# 设置调试地址
# edge_options.add_experimental_option("debuggerAddress", "localhost:9222")

# 创建WebDriver实例
# driver = webdriver.Edge(options=edge_options)
handles = driver.window_handles
for tab in driver.window_handles:
    driver.switch_to.window(tab)
    print(driver.title)
driver.switch_to.window(handles[0])
print(driver.title)
print(driver.current_url)
