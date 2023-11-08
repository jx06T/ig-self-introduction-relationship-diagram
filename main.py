from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
from draw import PeopleGraph
import threading
import json
import time
import datetime

import HTML_JS
import reptile

def ShowGUI(driver):
    global crawler
    print("14",crawler.state)
    driver.switch_to.window(driver.window_handles[-1])
    if crawler.state == 0:
        try:
            driver.execute_script(HTML_JS.remove_button)
        except:
            pass

        try:
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            current_url = driver.current_url

        if "https://www.instagram.com/" in current_url:
            driver.execute_script(HTML_JS.injection_button)
        t = None

        try:
            t = WebDriverWait(driver, timeout=6, poll_frequency=0.4).until(EC.alert_is_present())
        except:
            pass
        
        if not t == None:
            tt =t.text.split('^')
            data = {}
            data["MaxLevel"] = tt[1]
            data["MaxStep"] = tt[2]
            start(driver,data)
            return
            
        try:
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            pass

        try:
            driver.execute_script(HTML_JS.remove_button)
        except:
            pass
        
    elif crawler.state == 1:
        Stoppp()

def Stoppp():
    print("暫停")
    global crawler
    driver.switch_to.window(driver.window_handles[-1])
    driver.execute_script(HTML_JS.injection_button2)
    for i in range(60):
        t = None
        try:
            t = WebDriverWait(driver, timeout=1.5 ,poll_frequency=0.5).until(EC.alert_is_present())
        except:
            pass
    
        if not t == None:
            crawler.Play()
            return

        if keyboard.is_pressed('ctrl+alt+g'):
            Stoppp()
            return
        time.sleep(0.5)

    try:
        alert = driver.switch_to.alert
        alert.dismiss()
    except:
        pass
    try:
        driver.execute_script(HTML_JS.remove_button2)
    except:
        pass


def Getdatetime():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%y%m%d_%H_%M")
    return formatted_datetime

def start(driver,data):
    MaxLevel = data["MaxLevel"]
    MaxStep =data["MaxStep"]
    try:
        alert = driver.switch_to.alert
        alert.dismiss()
    except:
        pass
    try:
        wait = WebDriverWait(driver, 0.5)
        me = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.x1ms8i2q.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')))
        me = me.text
    except:
        print("錯誤77")
        me = "people_graph"

    MaxLevel = int(MaxLevel) if not MaxLevel == "" else 4
    MaxStep = int(MaxStep) if not MaxStep == "" else 300
    print("開始掃描",me,MaxLevel,MaxStep)
    global crawler
    crawler = reptile.InstagramCrawler(driver, MaxLevel, MaxStep,Stoppp)
    people = crawler.crawl()
    print(people)
    if not people:
        return
    graph = PeopleGraph(people)
    filename = f"output/{me}_{Getdatetime()}"
    graph.show_graph(filename,driver)
    with open(f"{filename}.json", "w") as f:
        json.dump(people, f)
        
    print("完成")

# %%
driver = webdriver.Chrome()
driver.get("https://www.instagram.com/")
time.sleep(1)
driver.execute_script(HTML_JS.note)
crawler = reptile.InstagramCrawler(driver,1,1,Stoppp)
keyboard.add_hotkey('ctrl+alt+g',lambda: ShowGUI(driver) )
keyboard.wait()

input()
driver.quit()
