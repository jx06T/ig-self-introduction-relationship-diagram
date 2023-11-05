from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time


def change(driver,href):
    all_window_handles = driver.window_handles
    if not href == None:
        try:
            driver.execute_script("window.open('" + href + "', '_blank');")
            all_window_handles = driver.window_handles
        except:
            pass
        
    if len(all_window_handles) == 1:
        return False
        
    driver.close()
    all_window_handles = driver.window_handles
    driver.switch_to.window(all_window_handles[0])
    return True

def DoStep(driver,i,MaxLevel,MaxStep,people,upcoming):
    me = None
    try:
        wait = WebDriverWait(driver, 0.5)
        me = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'h2.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.x1ms8i2q.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')))
        aboutMe = driver.find_element(By.XPATH, '//*[@class="x7a106z x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xwonja6 x1dyjupv x1onnzdu xwrz0qm xgmu61r x1nbz2ho xbjc6do"]')
        print(me.text)
    except:
        pass

    if me ==None:
        try:
            NN = driver.find_element(By.XPATH,'//span[contains(text(), "發生錯誤")]')
            if i >  MaxStep or not change(driver,upcoming.pop(0)):
                return people

            time.sleep(0.5)
            people = DoStep(driver,i+1,MaxLevel,MaxStep,people,upcoming)
            return people
        except:
            if i == 0:
                return people
            pass

        try:
            wait = WebDriverWait(driver, 2.5)
            me = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'h2.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.x1ms8i2q.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')))
            aboutMe = driver.find_element(By.XPATH, '//*[@class="x7a106z x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xwonja6 x1dyjupv x1onnzdu xwrz0qm xgmu61r x1nbz2ho xbjc6do"]')
            # print(me.text)
        except:
            if i > MaxStep or not change(driver,upcoming.pop(0)):
                return people

    # print(me.text,i)
    if i==0:
        people[me.text] = {}
        people[me.text]["level"] = 0
        people[me.text]["at"] = []
        people[me.text]["url"] =driver.current_url
    
    ats = aboutMe.find_elements(By.TAG_NAME, 'a')
    for at in ats:
        href = at.get_attribute("href")
        # print( at.text,at.get_attribute("href"))
        att = at.text[1:]
        if "explore" not in  href and  "https://www.instagram.com/" in href and "followers" not in href and att not in people:
            people[me.text]["at"].append(att)

            people[att] = {}
            people[att]["level"] = people[me.text]["level"]+1
            people[att]["at"] = []
            people[att]["url"] = href
            
            if  people[me.text]["level"] < MaxLevel:
                if len(upcoming)<10:
                    driver.execute_script("window.open('" + href + "', '_blank');")
                    upcoming.insert(0, None)
                else:
                    upcoming.insert(0, href)


    if i > MaxStep or not change(driver, upcoming.pop(0) if upcoming else None):
        return people
    time.sleep(0.5)
    people = DoStep(driver,i+1,MaxLevel,MaxStep,people,upcoming)
    
    return people

# %%
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/xy__0823/?next=%2F")
    people = {}
    MaxLevel = 3
    MaxStep = 100
    people = DoStep(driver,0,MaxLevel,MaxStep,people)
    print(people)