import random
import datetime
import time
import requests
from bs4 import BeautifulSoup
from urllib import request
from urllib.error import HTTPError

def outfile(item,title,author):
    number = len(item)
    dot = "<b>·</b>"
    content = ""
    content = content + "<h3><i>{0}-{1}</i></h3>\n".format(title, author)
    for i in range(number):
        content = content + "<b>{0}. {1}</b>\n".format(i+1, item[i]["Vocabulary"])
        content = content + dot + "Definition: {0}\n".format(item[i]["Definition"])
        content = content + dot + "Example: {0}\n".format(item[i]["Example"])
    with open("pei.txt","w",encoding="utf-8") as file:
        file.write(content)
        print("Finished.\n")

def auto_gernerate_single():
    root_url = "http://dict.youdao.com/w/eng/"
    print("Begin search")
    voclist = BeautifulSoup(request.urlopen("http://dict.yqie.com/GRE_glossary.htm"),"lxml").findAll("p")
    voc = voclist[random.randint(0,len(voclist) - 1)].text
    print(voc)
    dic = {}
    soup = BeautifulSoup(request.urlopen(root_url+voc),"lxml")
    trans_container = soup.find("div",{"class":"trans-container"})
    Definition = str(trans_container.find("ul").text).replace("\n","  ")
    # get the example of the voc
    examplesToggle = soup.find("div",{"id":"examplesToggle"})
    temp = examplesToggle.find("li").findAll("p")
    Example = (str(temp[0].text) + str(temp[1].text)).replace("\n"," ")
    dic["Vocabulary"] = voc.replace("_"," ")
    dic["Definition"] = Definition
    dic["Example"] = Example
    return dic

def auto_gernerate(title, author):
    number = 2
    item = []
    i = 0
    while (i < 2):
        print(i)
        dic = auto_gernerate_single()
        item.append(dic)
        i = i + 1
    outfile(item, title, author)

def sent(filename):
    header = {    
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Cookie':'ketangpai_home_remember=think%3A%7B%22username%22%3A%22MDAwMDAwMDAwMLOGy5iGqauwhbh-mLLfo54%22%2C%22expire%22%3A%22MDAwMDAwMDAwMLOGud2GqdGwhah2mLKmdZ4%22%2C%22token%22%3A%22MDAwMDAwMDAwMMurrpWavLehhs1-3LGphduFp3-WepuomcWmmqaMiHtnr5ylzYWosKKZq6HQxtOK0ZCme5p-q6iZu2yrn4uNhJ3KedDYk7ivboS4it2xqaPZhKdzmH96YW0%22%7D; PHPSESSID=nihdn7or3qmhle02h2agtds4f6'
    }
    datas = {
        'content':'',
        'topicid':''
    }
    content = open(filename, "r",encoding="utf-8").read()
    topicid = "MDAwMDAwMDAwMLOGx9uHz6dt"
    datas["content"]=content
    datas["topicid"]=topicid
    response = requests.post("https://www.ketangpai.com/TopicDiscussApi/addDiscuss", headers=header, data=datas).content
    print("Submit is successful!")


#Pei
while(True):
    t = datetime.datetime.now()
    h = 10
    m = 21
    if (t.hour == h and t.minute == m and flag):
        flag = False
        auto_gernerate("The Call of the Wild", "Jack London")
        sent("pei.txt") 
    if (t.hour != h or t.minute != m):
        flag = True



