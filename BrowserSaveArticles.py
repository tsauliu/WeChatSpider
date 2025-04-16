#%%
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time

edge_options = Options()
edge_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
# edge_options.add_experimental_option("debuggerAddress", "localhost:9222")

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
