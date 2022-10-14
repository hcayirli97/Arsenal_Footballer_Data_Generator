import bs4
import requests
from selenium import webdriver
import os
import time

def download_image(url, folder_name, num):

    # write image to file
    reponse = requests.get(url)
    if reponse.status_code==200:
        with open(os.path.join(folder_name, str(num)+".jpg"), 'wb') as file:
            file.write(reponse.content)

f = open("Arsenal_players.txt","r",encoding="utf-8")
data = f.readlines()
f.close()

url1 = "https://www.google.com/search?q=" 
url2 = "+&tbm=isch"


chromePath='chromedriver.exe'
driver=webdriver.Chrome(chromePath)
for dat in data:
    
    if "&" in dat:
        dat =dat.replace("&","")
        dat = dat.replace("  "," ")
    dat = dat.strip()

    dat = dat.replace(" ","+")
    folder_name = "D:/Dataset/Arsenal_Players/"+ dat.replace("+","_")
    if not os.path.isdir(folder_name):
         os.makedirs(folder_name)
    else:
        continue
        
    search_URL = url1 + dat+"+Arsenal+" + url2
    driver.get(search_URL)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    page_html = driver.page_source
    pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
    containers = pageSoup.findAll('div', {'class':"isv-r PNCib MSM1fd BUooTd"} )
    len_containers = len(containers)


    for i in range(1, len_containers+1):
        if i % 25 == 0:
            continue

        xPath = """//*[@id="islrg"]/div[1]/div[%s]"""%(i)

        previewImageXPath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%(i)
        previewImageElement = driver.find_element("xpath",previewImageXPath)
        previewImageURL = previewImageElement.get_attribute("src")

        driver.find_element("xpath",xPath).click()
        timeStarted = time.time()
        while True:

            imageElement = driver.find_element("xpath" , """//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img""")
            imageURL= imageElement.get_attribute('src')

            if imageURL != previewImageURL:
                #print("actual URL", imageURL)
                break

            else:
                #making a timeout if the full res image can't be loaded
                currentTime = time.time()

                if currentTime - timeStarted > 20:
                    break


        #Downloading image
        try:
            download_image(imageURL, folder_name, i)
        except:
            pass
    dir = os.listdir(folder_name)
    print(folder_name.split("/")[-1] + " {} images\n".format(len(dir)))
    dir = []

    