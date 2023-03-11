from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
browser = webdriver.Chrome('C:\lolzteamusers\chromedriver.exe')

fromcount = 1
tocount = 50000

usersGroupsStyles = {
    "style18" : "Заблокирован",
    "style2" : "Новорег",
    "style21" : "Местный",
    "style22" : "Постоялец",
    "style23" : "Эксперт",
    "style60" : "Гуру",
    "style351" : "Искусственный интеллект",
    "style7" : "Разработчик",
    "style29" : "Куратор",
    "style9" : "Дизайнер",
    "style350" : "Главный дизайнер",
    "style365" : "Редактор",
    "style353" : "Главный арбитр",
    "style4" : "Модератор",
    "style12" : "Главный Модератор",
    "style3" : "Админестратор",
    "style65" : "Привлегии на маркете",
    "style11" : "Продавец на форуме",
    "style26" : "Легенда",
    "style8" : "Суприм"
}
def infoDistribution(info):
    #Определене даты рождения и даты регистрации
    try:
        months = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
        for i in range(len(months)):
            if info.find(months[i]) != -1:
                if 2023 - int(info[-4:]) < 12:
                    return "regDay"
                else:
                    return "birthDay"
        #Определение пола
        if info == "Мужской" or info == "Женский":
            return "gender"
        #Определение Vk
        elif "vk.com" in info: 
            return "vkLink"
        #Определение Qiwi
        elif "qiwi" in info:
            return "qiwi"
        #Определение Discord
        elif "#" in info:
            return "discord"
        #Определение Steam
        elif "steamcommunity.com" in info:
            return "steam"
        #Определение Jabber
        elif "@" in info:
            return "jabber"
        return ""
    except:
        return"steam"
    
def deleteGarbageInfo(info):
    for i in range(len(info)):
        if "Темы от" in info[i]:
            info[i] = ""
        if info[i] in ["Регистрация:","Пол:","День рождения:","Telegram:","ВКонтакте:","QIWI никнейм:","Discord:","Steam:","Jabber:","Сайт:","Род занятий:","Адрес:","Интересы:","Аккаунты на маркете","Открыть чат в Telegram"]:
            info[i] = ""
    return info
a = []
count = 0
df = pd.DataFrame({'id': [], 'name': [], 'regDay': [], 'gender': [], 'birthDay': [], 'vkLink': [], 'qiwi': [], 'discord': [], 'steam': [], 'jabber': [], 'telegram': [], 'likes': [], 'messages': [], 'trophies': [], 'lottery': [], 'subscriptions': [], 'subscribers': [], 'userGroup': []})
for i in range(fromcount,tocount):
    
    user = {
    'id' : "",
    'name' : "",
    'regDay' : "",
    'gender' : "",
    'birthDay' : "",
    'vkLink' : "",
    'qiwi' : "",
    'discord' : "",
    'steam' : "",
    'jabber' : "",
    'telegram' : "",
    'likes' : "",
    'messages' : "",
    'trophies' : "",
    'lottery' : "",
    'subscriptions' : "",
    'subscribers' : "",
    'userGroup' : ""
    }
    print("Текущая итерация - {}".format(i))
    browser.get('https://zelenka.guru/members/{}/'.format(i))
    try:
        if browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[4]/div/label').text == "Запрашиваемый пользователь не найден.":
            print("Пользователь {} не найден".format(i))
            continue
    except:
        print("Пользователь {} найден".format(i))
    user["id"] = str(i)
    #Поиск основной информации по xpath
    userInfo =  browser.find_element(By.XPATH, '//*[@id="profile_short"]').text
    #Разделение на строки и удаление не нужной инфы
    userInfo = deleteGarbageInfo(userInfo.split('\n'))
    #Заполнение словоря user
    for i in range(len(userInfo)):
        infoType = infoDistribution(userInfo[i])
        if (infoType in user):
            user[infoType] = userInfo[i]
    #Поиск никнейма
    user["name"] = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div/div[1]/div[1]/h1/div/span').text
    #Поиск телеграм
    try:
        user["telegram"] = browser.find_element(By.XPATH, '//*[@id="profile_short"]/div[1]/div[4]/div[2]/div[2]/a').get_attribute('href')[20:]
    except:
        user["telegram"] = ""
    #Поиск симпатий/сообщений/трофеев/розыгрышей/подписок/подписчиков
    user["likes"] = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div/div[2]/a[1]/div[1]').text
    user["messages"] = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div/div[2]/a[2]/div[1]').text
    user["trophies"] = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div/div[2]/a[3]/div[1]').text
    user["lottery"] = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div/div[2]/a[4]/div[1]').text
    user["subscriptions"] = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div/div[2]/a[5]/div[1]').text
    user["subscribers"] = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div/div[2]/a[6]/div[1]').text
    #Поиск группы пользователя
    group = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div/div[1]/div[1]/h1/div/span').get_attribute("class")
    style = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div/div[1]/div[1]/h1/div/span').get_attribute("style")
    if group in usersGroupsStyles:
        user['userGroup'] = usersGroupsStyles[group]
    if "background" in style or "color" in style:
        user['userGroup'] = "Уник"


    a.append([user["id"],user["name"],user["regDay"],user["gender"],user["birthDay"],user["vkLink"],user["qiwi"],user["discord"],user["steam"],user["jabber"],user["telegram"],user["likes"],user["messages"],user["trophies"],user["lottery"],user["subscriptions"],user["subscribers"],user["userGroup"]])
    count += 1
    if count == 1000:
        count = 0
        df = pd.DataFrame(a, columns=df.columns)
        df.to_csv (r'C:\\lolzteamusers\\{}по{}.csv'.format(fromcount,tocount), index= False )
    print(a)
#print(userInfo)
