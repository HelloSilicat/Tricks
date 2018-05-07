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
    for i in range(number):
        dic = auto_gernerate_single()
        item.append(dic)
    outfile(item, title, author)

def sent(filename):
    header = {    
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Cookie':''
    datas = {
        'content':'',
        'topicid':''
    }
    content = open(filename, "r",encoding="utf-8").read()
    topicid = ""
    datas["content"]=content
    datas["topicid"]=topicid
    response = requests.post("https://www.ketangpai.com/TopicDiscussApi/addDiscuss", headers=header, data=datas).content
    print("Submit is successful!")


#Pei
while(True):
    t = datetime.datetime.now()
    if (t.hour == 10 and t.minute == 30):
        time.sleep(60)
        auto_gernerate("The Call of the Wild", "Jack London")
        sent("pei.txt") 



