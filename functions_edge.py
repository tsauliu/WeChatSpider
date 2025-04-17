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
import sqlite3
from database_mgmt import DB_NAME

edge_options = Options()
edge_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
service = Service(executable_path="C:/edgedriver_win32/msedgedriver.exe")
EdgeDriver = webdriver.Edge(service=service, options=edge_options)

def close_mp_weixin_tab(driver):
    for tab in driver.window_handles:
        driver.switch_to.window(tab)
        url=driver.current_url
        if 'mp.weixin' in url:
            print(f"Closing tab: {url}")
            driver.close()

close_mp_weixin_tab(EdgeDriver)

def save_to_db(channel_scraped, article_title, url, pub_time):
    """Saves scraped article information to the SQLite database."""
    
    if not 'mp.weixin' in url:
        return
    
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Use INSERT OR IGNORE to avoid errors if the URL already exists (due to UNIQUE constraint)
        cursor.execute("""
        INSERT OR IGNORE INTO articles (channel_scraped, article_title, url, pub_time)
        VALUES (?, ?, ?, ?)
        """, (channel_scraped, article_title, url, pub_time))
        conn.commit()
        print(f"Successfully saved  details to database {article_title}")
    except sqlite3.Error as e:
        print(f"Database error when saving {url}: {e}")
    finally:
        if conn:
            conn.close()

def scrape_url_to_md(driver, output_dir, channel_scraped, article_title):
    for tab in driver.window_handles:
        driver.switch_to.window(tab)
        url=driver.current_url
        if 'mp.weixin' in url:
            break
   
    if not 'mp.weixin' in url:
        print(f"Not a WeChat article: {url}")
        return False

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

    # Skip if file already exists，验证放在了WeChatSpider.py中，打开url之前
    # if os.path.exists(output_path):
    #     print(f"File already exists: {output_path}, skipping...")
    #     close_mp_weixin_tab(driver)
    #     return
    
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
        try:
            pub_time = soup.find('em', id='publish_time').text.strip()
        except:
            pub_time = ""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)

        print(f"Successfully saved {article_title} to {output_path}")
        # Save details to database
        save_to_db(channel_scraped, article_title, url, pub_time)
        time.sleep(1)
        close_mp_weixin_tab(driver)        
        time.sleep(3) 
        return True
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        close_mp_weixin_tab(driver)
        time.sleep(3) 
    
if __name__ == "__main__":
    scrape_url_to_md(EdgeDriver, "./articles", "Example Channel", "Example Title")

