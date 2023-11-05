from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import keyboard
class InstagramCrawler:
    def __init__(self, driver, max_level, max_step,call_back):
        self.driver = driver

        self.MaxLevel = max_level
        self.MaxStep = max_step
        self.people = {}
        self.upcoming = []
        self.state = 0
        self.call_back = call_back

    def change(self, href):
        all_window_handles = self.driver.window_handles
        if href is not None:
            try:
                self.driver.execute_script("window.open('" + href + "', '_blank');")
                all_window_handles = self.driver.window_handles
            except:
                pass

        if len(all_window_handles) == 1:
            return False

        self.driver.close()
        all_window_handles = self.driver.window_handles
        self.driver.switch_to.window(all_window_handles[0])
        return True

    def do_step(self, i):
        if keyboard.is_pressed('ctrl+alt+g'):
            self.state = 2
            self.I = i
            self.call_back()
            return
        
        me = None
        aboutMe = None
        # print(i,self.people,self.upcoming,me)
        try:
            wait = WebDriverWait(self.driver, 0.5)
            me = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.x1ms8i2q.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')))
            aboutMe = self.driver.find_element(By.XPATH, '//*[@class="x7a106z x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xwonja6 x1dyjupv x1onnzdu xwrz0qm xgmu61r x1nbz2ho xbjc6do"]')
            print(me.text)
        except:
            pass

        if me == None or aboutMe == None:
            try:
                NN = self.driver.find_element(By.XPATH, '//span[contains(text(), "發生錯誤")]')
                if i > self.MaxStep or not self.change(self.upcoming.pop(0) if self.upcoming else None):
                    return

                time.sleep(0.5)
                self.do_step(i + 1)
                return
            except:
                if i == 0:
                    return
                pass

            try:
                wait = WebDriverWait(self.driver, 2.5)
                me = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.x1ms8i2q.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')))
                aboutMe = self.driver.find_element(By.XPATH, '//*[@class="x7a106z x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xwonja6 x1dyjupv x1onnzdu xwrz0qm xgmu61r x1nbz2ho xbjc6do"]')
            except:
                if i > self.MaxStep or not self.change(self.upcoming.pop(0) if self.upcoming else None):
                    return

        # print(i,self.people,self.upcoming,me)
        if i == 0:
            self.people[me.text] = {}
            self.people[me.text]["level"] = 0
            self.people[me.text]["at"] = []
            self.people[me.text]["url"] = self.driver.current_url

        ats = aboutMe.find_elements(By.TAG_NAME, 'a')
        for at in ats:
            href = at.get_attribute("href")
            att = at.text[1:]
            self.people[me.text]["at"].append(att)
            if "explore" not in href and "https://www.instagram.com/" in href and "followers" not in href and att not in self.people:

                self.people[att] = {}
                self.people[att]["level"] = self.people[me.text]["level"] + 1
                self.people[att]["at"] = []
                self.people[att]["url"] = href

                if self.people[me.text]["level"] < self.MaxLevel:
                    if len(self.upcoming) < 10:
                        self.driver.execute_script("window.open('" + href + "', '_blank');")
                        self.upcoming.insert(0, None)
                    else:
                        self.upcoming.insert(0, href)

        if i > self.MaxStep or not self.change(self.upcoming.pop(0) if self.upcoming else None):
            return
        time.sleep(0.5)
        self.do_step(i + 1)

    def crawl(self):
        self.state = 1
        self.do_step(0)
        self.state = 0
        return self.people
    
    def Play(self):
        self.state = 1
        self.do_step(self.I)
        print("5555555555555555555555555555")

def DoStop():
    print("!!!!!!!!!!!!!!!!!")

if __name__ == '__main__':
    driver = webdriver.Chrome()
    # driver.get("https://www.instagram.com/xy__0823/?next=%2F")
    driver.get("https://www.instagram.com")
    max_level = 3
    max_step = 100
    input()
    crawler = InstagramCrawler(driver, max_level, max_step,DoStop)

    keyboard.add_hotkey('ctrl+alt+p', crawler.Play )
    people = crawler.crawl()
    print(people)

    keyboard.wait()