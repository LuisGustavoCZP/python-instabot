from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def has_browser (browser):
    try:
        _ = browser.window_handles
    except exceptions.InvalidSessionIdException as e:
        return False

def new_browser ():
    browser = webdriver.Firefox()
    browser.implicitly_wait(3)
    return browser

def load (arquivo):
    f = open(arquivo, "r")
    return json.load(f)

class ProtonCreationPage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://protonmail.com/pt_BR/')
        try:
            create_button = browser.find_element(By.XPATH, '//ul[@class="nav navbar-nav navbar-right"]/li[9]/a')
            create_button.click()
        except BaseException as e:
            print("Não foi possivel clicar no botão principal")

    def free_plan(self): 
        try:
            WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-controls="plan-free"]'))).click()
            self.browser.find_element(By.XPATH, '//button[@id="freePlan"]').click()
            return True
        except BaseException as e:
            print(e)
            return False

    def user_creation(self):
        try:
            input_username = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@id="username"]')))
            input_username.send_keys(user['username'])
            return True
        except BaseException as e:
            print("Deu erro aqui mermão!\n{}".format(e))
            return False

users = load("contas_email.json")
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[starts-with(@aria-describedby, 'ui-id-')]//span[@class='ui-button-text' and text()='Continue']"))).click()
browser = new_browser()   
creationPage = ProtonCreationPage(browser)
if creationPage.free_plan():
    if creationPage.user_creation():
        print("Pronto!")
    
    