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
    a = wordSoup.find_all(name="td", height="30")
    LIST = []
    i = 0

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
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
        'Connection': 'keep-alive'
    }
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
    for url in List:
        list1 = []
        html = getWordHtml(url)
        wordSoup = BeautifulSoup(html, "lxml")
        a = wordSoup.find_all(name="div", class_="mt40")
        for line in a:
            for string in line.stripped_strings:
                list1.append(repr(string))
        list1 = list1[10:-1]    #减去前面10个和后面1个多余的
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
        new_str = re.findall(pat, i)    #找到全英文的列表
        if(new_str != []):
            a = new_str[0]
            a = re.sub('[^\w\u4e00-\u9fff]+', '', a)
            file.write(str(a)+"\n")
    print("完成")
