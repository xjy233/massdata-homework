# coding = utf-8

from urllib import request, parse
from bs4 import BeautifulSoup
import sys
import re
import lxml

inputDecode = sys.stdin.encoding
outputDecode = sys.stdout.encoding

"""
初始化，得到单词列表的url
"""
def getListUrl():
    url = r'http://cet6.koolearn.com/20180927/822884.html'
    html = getWordHtml(url)
    wordSoup = BeautifulSoup(html, "lxml")
    #找到<td height="30" width="82%"><a href="http://cet6.koolearn.com/20180927/822885.html" target="_blank">
    #他返回一个匹配td height="30"的列表，其中有我们要的href
    a = wordSoup.find_all(name="td", height="30")
    LIST = []
    i = 0
    #并不是每个td height="30"都包含一个href
    # 每隔一行是一个url所以用line.a['href']取值
    for line in a:
        if ((i % 2) == 1 and i < 98):
            LIST.append(line.a['href'])
        i += 1
    return LIST

"""
去查找一个单词列表并下载它的单词
输入：单词列表
返回：XML格式的文件
"""
def getWordHtml(url):
    #修改head信息，模仿成手机浏览器
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
        'Connection': 'keep-alive'
    }
    #发出请求并下载得到HTML文件
    req = request.Request(url, headers=headers)
    page = request.urlopen(req).read()

    return page.decode('utf-8')

"""
收集单词
输入：单词列表的全部url
返回：单词列表的List集合
"""
def reWordList(List):
    RelistWord = []
    #将LIST列表的url依次取出，并通过上面的getHTML函数来得到LIST列表里面的内容
    for url in List:
        list1 = []
        html = getWordHtml(url)
        # 创建BeautifulSoup对象
        wordSoup = BeautifulSoup(html, "lxml")
        # 搜索文档树,找出div标签中class为mt40的所有子标签，每一个子标签里面含有一个单词的结构
        a = wordSoup.find_all(name="div", class_="mt40")
        for line in a:
            #将div标签里所有的字符串遍历
            for string in line.stripped_strings:
                list1.append(repr(string))    #["'新东方在线英语六级'", "'频道为大家整理了'","'英语六级高频词汇'",
                #  ..."'：List 1'", "'comprehension 理解'","'access 接近，进入;通道，入口'", "'account 帐(目、户);叙述，说明'"...]
        list1 = list1[10:-1]    #减去前面10个和后面1个多余的
        #再将单词和解释切分开来如access 接近，进入;通道，入口，只要access
        for elem in list1:
            elem = elem.split(" ")
            a = elem[0][1:]
            RelistWord.append(a)
    return RelistWord



if __name__ == '__main__':
    ListUrl = getListUrl()
    a = reWordList(ListUrl)
    #写入单词到words.txt
    file = open('words.txt', 'w', encoding='utf-8')
    pat = '[a-zA-Z]+'     #正则表达式全英文
    for i in a:
        #由于a里的单词爬下来有些单词和汉字在一起没切开，所以使用re.findall匹配所有英文
        new_str = re.findall(pat, i)    #找到全英文的列表
        if(new_str != []):
            a = new_str[0]
            a = re.sub('[^\w\u4e00-\u9fff]+', '', a)#将使用正则表达式过滤非中英文字符因为比如apple①后面带个①
            file.write(str(a)+"\n")
    print("完成")

    # re使用参考
    # pat = '[a-zA-Z]+'
    # text = '"hello123,my name向 is xiaoming ,how are you?" he said.'
    # a = re.findall(pat, text)
    # print(a)
    # ['hello', 'my', 'name', 'is', 'xiaoming', 'how', 'are', 'you', 'he', 'said']


