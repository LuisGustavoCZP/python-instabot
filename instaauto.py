from time import sleep
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium import webdriver
import json

last_browser = None

def has_browser (browser):
    try:
        _ = browser.window_handles
    except exceptions.InvalidSessionIdException as e:
        return False

def new_browser ():
    browser = webdriver.Firefox()
    browser.implicitly_wait(3)
    last_browser = browser
    return browser

class InstaAuto: 
    def __init__(self, browser, username, password):
        self.browser = browser
        self.browser.get('https://www.instagram.com/')
        self.login(username, password)

    def login(self, username, password):
        browser = self.browser
        username_input = browser.find_element(By.CSS_SELECTOR, "input[name='username']")
        password_input = browser.find_element(By.CSS_SELECTOR, "input[name='password']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = browser.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        #sleep(2)
        login_button = browser.find_element(By.XPATH, "//button[text()='Agora não']")
        login_button.click()
        login_button = browser.find_element(By.XPATH, "//button[text()='Agora não']")
        login_button.click()
    
    def open_profile (self):
        try:
            profile_button = self.browser.find_element(By.CSS_SELECTOR, "div.MWDvN > div.ctQZg.KtFt3 > div.J5g42 > div.XrOey > span._2dbep.qNELH")
            profile_button.click()
            return profile_button
        except:
            return None
    
    def logout(self):
        profile_button = self.open_profile()
        if profile_button != None:
            logout_area = profile_button.parent.find_element(By.CSS_SELECTOR, "div.poA5q > div > div._01UL2")
            logout_button = logout_area.find_element(By.XPATH, "//div[@class='-qQT3'][2]")
            logout_button.click()
    
    def pesquisar(self, assunto):
        browser = self.browser
        input_search = browser.find_element(By.XPATH, '//input[@aria-label="Entrada da pesquisa"]')
        input_search.send_keys(assunto) 
        search_results = []
        for option in browser.find_elements(By.CSS_SELECTOR, 'div.fuqBx > div > a'):
            search_results.append(option.get_attribute("href"))
        
        return search_results
    
    def rolar(self, pagina, total, interação):
        browser = self.browser #"https://www.instagram.com/explore/tags/{}/".format(pagina)
        browser.get(pagina)
        fotos_abertas = {}
        #sleep(3)
        print("Abriu feed...")
        if total > 0:
            for i in range(1, total):
                sleep(1.1)
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                for option in browser.find_elements(By.CSS_SELECTOR, 'div.Nnq7C.weEfm > div._bz0w > a'):
                    link_atual = option.get_attribute("href")
                    if fotos_abertas.get(link_atual, None) == None:
                        interação(link_atual)
                        fotos_abertas.update({link_atual:option})
        else:
            try:
                browser.find_element(By.CSS_SELECTOR, "div._4emnV")
                while True:
                    sleep(1.1)
                    print("Rolando feed...")
                    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    try: 
                        browser.find_element(By.CSS_SELECTOR, "div._4emnV")
                    except: 
                        break
            except:
                return
        sleep(1)        
        
        print("Acabou feed")
    
    def curtir_foto(self, link):
        browser = self.browser
        last_window = browser.current_window_handle
        browser.execute_script('window.open("{}","_blank");'.format(link))
        browser.switch_to.window(window_name=browser.window_handles[-1])
        like_button = browser.find_element(By.CSS_SELECTOR, "section.ltpMr.Slqrh > span.fr66n > button.wpO6b")
        like_button.click()
        browser.execute_script('window.close();')
        browser.switch_to.window(window_name=last_window)
        print("Curtiu {} !".format(link))
    

def load (arquivo):
    f = open(arquivo, "r")
    return json.load(f)