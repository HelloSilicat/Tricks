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
    with open("temp.txt","w",encoding="utf-8") as file:
        file.write(content)

def auto_gernerate_single():
    root_url = "http://dict.youdao.com/w/eng/"
    print("Begin search voclabury...")
    voclist = BeautifulSoup(request.urlopen("http://dict.yqie.com/GRE_glossary.htm"),"lxml").findAll("p")
    voc = voclist[random.randint(0,len(voclist) - 1)].text
    print("Find voc:" ,voc)
    dic = {}
    flag = True
    while(flag):
        try:
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
            flag = False
        except:
            print("Error: can't construct dic.")
    return dic

def auto_gernerate(title, author):
    number = 2
    item = []
    i = 0
    while (i < 2):
        dic = auto_gernerate_single()
        item.append(dic)
        i = i + 1
    outfile(item, title, author)

def sent(filename,cookie):
    header = {    
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Cookie': None
    }
    header['Cookie'] = cookie
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

# configuration
cookie_pei = "ketangpai_home_remember=think%3A%7B%22username%22%3A%22MDAwMDAwMDAwMLOGy5iGqauwhbh-mLLfo54%22%2C%22expire%22%3A%22MDAwMDAwMDAwMLOGud2GqdGwhah2mLKmdZ4%22%2C%22token%22%3A%22MDAwMDAwMDAwMMurrpWavLehhs1-3LGphduFp3-WepuomcWmmqaMiHtnr5ylzYWosKKZq6HQxtOK0ZCme5p-q6iZu2yrn4uNhJ3KedDYk7ivboS4it2xqaPZhKdzmH96YW0%22%7D; PHPSESSID=nihdn7or3qmhle02h2agtds4f6"
cookie_sbfw = "PHPSESSID=8td0oo7qmssgjn0rnja87ikgq5; ketangpai_home_wchatUser=think%3A%7B%22openid%22%3A%22oOsrhwJOJinQ3LMUT6OCje0Duggs%22%2C%22nickname%22%3A%22Frank%2BFan%22%2C%22sex%22%3A%221%22%2C%22language%22%3A%22zh_CN%22%2C%22city%22%3A%22%22%2C%22province%22%3A%22%22%2C%22country%22%3A%22%25E9%2598%25BF%25E9%25B2%2581%25E5%25B7%25B4%22%2C%22headimgurl%22%3A%22http%253A%252F%252Fthirdwx.qlogo.cn%252Fmmopen%252Fvi_32%252FQ0j4TwGTfTJAFtPscrxXIkia6LGcf02yBGwKtIJdMSd0dopV5mxLBh0zElxQIsBh5ibf7dibQwicDvzJV3S486JCmg%252F132%22%2C%22privilege%22%3Anull%2C%22unionid%22%3A%22od_0Gw2HCsSrUMsZVyz7Bzu8zqts%22%7D; ketangpai_home_remember=think%3A%7B%22username%22%3A%22MDAwMDAwMDAwMMdlttuGqa-whLh23rHfidiEtG-h%22%2C%22expire%22%3A%22MDAwMDAwMDAwMLOGud2G37uwhqiclrG2dZ4%22%2C%22token%22%3A%22MDAwMDAwMDAwMMurrpWavLehhs1-3LGphduFp5XcepuomcWmmqaMiHtnr5ylzYWosKKZq6HQxtOK0ZCme5p-q6iZu2yrn4uNhJ3KedDYk7ivboS4it2x343ZhaeZln6KYW0%22%7D"
cookie_lyt = "PHPSESSID=rm0tvdibfkrhoooeu59jdq8qf2; ketangpai_home_wchatUser=think%3A%7B%22openid%22%3A%22oOsrhwNPHDTBJdCTgdDdUF8S_VK8%22%2C%22nickname%22%3A%22.%22%2C%22sex%22%3A%221%22%2C%22language%22%3A%22zh_CN%22%2C%22city%22%3A%22%22%2C%22province%22%3A%22%22%2C%22country%22%3A%22%25E4%25B8%25AD%25E5%259B%25BD%22%2C%22headimgurl%22%3A%22http%253A%252F%252Fthirdwx.qlogo.cn%252Fmmopen%252Fvi_32%252FDYAIOgq83epiaGndmVyhJDVaW7biaHbOoWlNOGAoyZ8EGE8sSrSRngHFF2ibTGvscSXhT8zYqMBE4JcjZoHkibKc2Q%252F132%22%2C%22privilege%22%3Anull%2C%22unionid%22%3A%22od_0Gw9UaDvWDTkzh_k24lPlBg3g%22%7D; ketangpai_home_remember=think%3A%7B%22username%22%3A%22MDAwMDAwMDAwMMdlttuGqa-whLh23rHfidiDym-h%22%2C%22expire%22%3A%22MDAwMDAwMDAwMLOGud2Huclohrh6lrGmdZ4%22%2C%22token%22%3A%22MDAwMDAwMDAwMMurrpWavLehhs1-3LGphduFp4uYepuomcWmmqaMiHtnr5ylzYWosKKZq6HQxtOK0ZCme5p-q6iZu2yrn4uNhJ3KedDYk7ivboS4it2yuZuRhbd3ln56YW0%22%7D"
cookie_gyc = "gr_user_id=1a88fc17-2a05-4952-8232-15e882bce2c5; _ga=GA1.2.1178122871.1507559518; ketangpai_home_remember=think%3A%7B%22username%22%3A%22MDAwMDAwMDAwMLV2vZSGz7NthLiGmLWtftmC0IDak4NubQ%22%2C%22expire%22%3A%22MDAwMDAwMDAwMLOGud2G39FrhbiKlbGmdZ4%22%2C%22token%22%3A%22MDAwMDAwMDAwMMurrpWavLehhs1-3LGphduFp4OWepuomcWmmqaMiHtnr5ylzYWosKKZq6HQxtOK0ZCme5p-q6iZu2yrn4uNhJ3KedDYk7ivboS4it2x36OUhLeHlX56YW0%22%7D; PHPSESSID=6c7818fh2apj30ra57mt0bimc5"


h_pei = 10; m_pei = 30
h_sbfw = 6; m_sbfw = 30
h_lyt = 16; m_lyt = 38
h_gyc = 21; m_gyc = 22

flag_pei = True
flag_sbfw = True
flag_lyt = True
flag_gyc = True

# run
debug = True
while(True):
    t = datetime.datetime.now()
    
    if (debug and t.second == 0):
        pass
        #print(t.hour, t.minute)
    
    #pei
    if (t.hour == h_pei and t.minute == m_pei and flag_pei):
        print("Pei Start")
        flag_pei = False
        auto_gernerate("The Call of the Wild", "Jack London")
        sent("temp.txt",cookie_pei) 
        print("Pei Finish")
    if (t.hour != h_pei or t.minute != m_pei):
        flag_pei = True

    #sbfw
    if (t.hour == h_sbfw and t.minute == m_sbfw and flag_sbfw):
        print("SBFW Start")
        flag_sbfw = False
        auto_gernerate("", "")
        sent("temp.txt",cookie_sbfw) 
        print("SBFW Finish")
    
    if (t.hour != h_sbfw or t.minute != m_sbfw):
        flag_sbfw = True
    
    #lyt
    if (t.hour == h_lyt and t.minute == m_lyt and flag_lyt):
        print("Lyt Start")
        flag_lyt = False
        auto_gernerate("The Catcher in the Rye", "Jerome David Salinger")
        sent("temp.txt",cookie_lyt) 
        print("Lyt Finish")
    
    if (t.hour != h_lyt or t.minute != m_lyt):
        flag_lyt = True
    
    #gyc
    if (t.hour == h_gyc and t.minute == m_gyc and flag_gyc):
        print("Gyc Start")
        flag_gyc = False
        auto_gernerate("Computer NetWork", "Andrew")
        sent("temp.txt",cookie_gyc) 
        print("Gyc Finish")
    if (t.hour != h_gyc or t.minute != m_gyc):
        flag_gyc = True




