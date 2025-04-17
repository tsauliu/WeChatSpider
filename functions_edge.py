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
from selenium.webdriver.common.by import By

import time
import os,re
from bs4 import BeautifulSoup

edge_options = Options()
edge_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
service = Service(executable_path="C:/edgedriver_win32/msedgedriver.exe")
EdgeDriver = webdriver.Edge(service=service, options=edge_options)

def scrape_url_to_md(driver, output_dir):
    for tab in driver.window_handles:
        driver.switch_to.window(tab)
        url=driver.current_url
        if 'mp.weixin' in url:
            break
   
    print(url)
    
    url_id = url.split('/')[-1]
    filename = f"{url_id}.md"
    output_path = os.path.join(output_dir, filename)
    
    # Check if the file already exists and contains error message
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "完成验证后即可继续访问" in content:
                    print(f"File contains error message, deleting: {output_path}")
                    os.remove(output_path)
        except Exception as e:
            print(f"Error checking existing file {output_path}: {str(e)}")

    # Skip if file already exists
    if os.path.exists(output_path):
        print(f"File already exists: {output_path}, skipping...")
        driver.close()
        return
    
    try:        
        page_source = driver.page_source        
        soup = BeautifulSoup(page_source, 'html.parser')
        text_content = soup.get_text()
        
        if "完成验证后即可继续访问" in text_content:
            button = driver.find_element(By.ID, 'js_verify')
            button.click()
            time.sleep(3)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        text_content = soup.get_text()
        text_content = re.sub(r'\n{3,}', '\n\n', text_content)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        time.sleep(5)        
        print(f"Successfully saved {url} to {output_path}")
        driver.close()
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
    
    

if __name__ == "__main__":
    scrape_url_to_md(EdgeDriver, "./articles")

