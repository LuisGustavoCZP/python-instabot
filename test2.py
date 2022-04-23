import instaauto as iato

users = iato.load("conta_insta.json")

class InstaRobot:
    def __init__(self, browser, user):
        self.user = user
        self.automato = iato.InstaAuto(browser, user["username"], user["userpass"])
            
    def execute(self):
        auto = self.automato
        paginas = auto.pesquisar("#peitos")
        p = 0
        for pagina in paginas:
            if(p > 1): break
            p += 1
            print("Rodando {}".format(p))
            auto.rolar(pagina, 1, auto.curtir_foto)
    
    def exit (self):
        self.automato.logout()

browser = iato.new_browser()
for user in users:
    print("Checking if {} is denied ({})".format(user["username"], user["denied"]))
    #if user["denied"] == True: continue
    #else: 
    
    try:
        if iato.has_browser(browser) == False:
            browser = iato.new_browser()
        
        bot = InstaRobot(browser, user)
        bot.execute()
        bot.exit()
    except BaseException as e:
        print(e)
        browser.close()
        
if iato.has_browser(browser) == True: browser.close()