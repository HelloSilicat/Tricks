import json
import requests
from bs4 import BeautifulSoup
from urllib import request
from urllib.error import HTTPError

def input_manual(mode = 1):
    title = input("Title:\n>")
    author = input("Author:\n>")
    item = []
    number = int(input("Number:\n>"))
    for i in range(number):
        print("Add %dth items......\n"%(i + 1))
        dic = {}
        dic["Vocabulary"] = input("Vocabulary:\n>")
        dic["Definition"] = input("Definition:\n>")
        dic["Example"] = input("Example:\n>")
        dic["Remark"] = input("Remark:\n>")
        item.append(dic)
    with open("temp.json","a") as outfile:
        json.dump(item, outfile, ensure_ascii=False)
        outfile.write('\n')
    return item,title,author

def outfile(item,title,author):
    number = len(item)
    dot = "<b>·</b>"
    content = ""
    # add title
    content = content + "<h3><i>{0}-{1}</i></h3>\n".format(title, author)
    # add items
    for i in range(number):
        # add Vocabulary
        #print("debug info")
        content = content + "<b>{0}. {1}</b>\n".format(i+1, item[i]["Vocabulary"])
        # add Definition
        content = content + dot + "Definition: {0}\n".format(item[i]["Definition"])
        # add Example
        content = content + dot + "Example: {0}\n".format(item[i]["Example"])
        # add Remark
        if (item[i]["Remark"] != "None"):
            content = content + dot + "Remark: {0}\n".format(item[i]["Remark"])
    # outfile
    with open("Look here.txt","a",encoding="utf-8") as file:
        file.write(content)
        print("Finished.\n")

def auto_gernerate_single():
    root_url = "http://dict.youdao.com/w/eng/"
    voc = input("What is your vocabulary?\n>").strip().replace(" ","_")
    url = root_url + voc
    print("debug info:",url)
    dic = {}
    # get the whole page of the voc
    flag = False
    while (not flag):
        try:
            flag = True
            soup = BeautifulSoup(request.urlopen(url),"lxml")
        except HTTPError as e:
            print("This vocabulary is missing! Why not change another one?")
            voc = input("What is your vocabulary?\n>").strip().replace(" ","_")
            url = root_url + voc
            print("debug info:",url)
            flag = False
    # get the definition of the voc
    flag = False
    while (not flag):
        try:
            flag = True
            trans_container = soup.find("div",{"class":"trans-container"})
        except HTTPError as e:
            print("ERROR: trans_container is not found!")
            flag = False
    Definition = str(trans_container.find("ul").text).replace("\n","  ")
    # get the example of the voc
    flag = False
    while (not flag):
        try:
            flag = True
            examplesToggle = soup.find("div",{"id":"examplesToggle"})
        except HTTPError as e:
            print("ERROR: examplesToggle is not found!")
            flag = False
    temp = examplesToggle.find("li").findAll("p")
    Example = (str(temp[0].text) + str(temp[1].text)).replace("\n"," ")
    # get the remark of the voc
    print("Definition: ", Definition)
    print("Example: ", Example)
    s = input("Do you need a remark?(Y/N)").upper().strip()
    while (not (s == 'Y' or s == 'N')):
        print("Your input is invalid, please input again.")
        s = input("Do you need a remark?(Y/N)").upper().strip()
    if (s == 'Y'):
        Remark = input("What is your remark?\n>").strip()
    else :
        Remark = "None"
    dic["Vocabulary"] = voc.replace("_"," ")
    dic["Definition"] = Definition
    dic["Example"] = Example
    dic["Remark"] = Remark
    return dic

def auto_gernerate(title, author):
    number = int(input("Number:\n>"))
    item = []
    for i in range(number):
        dic = auto_gernerate_single()
        item.append(dic)
    outfile(item, title, author)

def sent(filename):
    header = {    
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Cookie':'PHPSESSID=sh3ql2ecsdlo9e3o45jjqp4rf2; ketangpai_home_remember=think%3A%7B%22username%22%3A%22MDAwMDAwMDAwMLOGy5iGqauwhbh-mLLfo54%22%2C%22expire%22%3A%22MDAwMDAwMDAwMLOGud2GqdGwhbiclbKmdZ4%22%2C%22token%22%3A%22MDAwMDAwMDAwMMurrpWavLehhs1-3LGphduFp3-WepuomcWmmqaMiHtnr5ylzYWosKKZq6HQxtOK0ZCme5p-q6iZu2yrn4uNhJ3KedDYk7ivboS4it2xqaPZhLeZlX96YW0%22%7D'
    }
    datas = {
        'content':'',
        'topicid':''
    }
    content = open(filename, "r",encoding="utf-8").read()
    topicid = "MDAwMDAwMDAwMLOGpZmHz7Nr"
    datas["content"]=content
    datas["topicid"]=topicid
    response = requests.post("https://www.ketangpai.com/TopicDiscussApi/addDiscuss", headers=header, data=datas).content
    print("Submit is successful!")


title = input("Title:\n>")
author = input("Author:\n>")
# item,title,author = input_manual(1)
#outfile(item,title,author)
auto_gernerate(title, author)
input("Click anything to submit!\n")
sent("Look here.txt")
    



