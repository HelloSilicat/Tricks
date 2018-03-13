import json
import requests

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
        print("debug info")
        content = content + "<b>{0}. {1}</b>\n".format(i+1, item[i]["Vocabulary"])
        # add Definition
        content = content + dot + "Definition: {0}\n".format(item[i]["Definition"])
        # add Example
        content = content + dot + "Example: {0}\n".format(item[i]["Example"])
        # add Remark
        content = content + dot + "Remark: {0}\n".format(item[i]["Remark"])
    # outfile
    with open("Look here.txt","a",encoding="utf-8") as file:
        file.write(content)
        print("Finished.\n")


def sent(filename):
    header = {    
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Cookie':'*********************' #自己填充
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
    print(response)


item,title,author = input_manual(1)
outfile(item,title,author)
sent("Look here.txt")
    



