# coding = utf-8

from urllib import request, parse
from bs4 import BeautifulSoup
import sys
import lxml

inputDecode = sys.stdin.encoding
outputDecode = sys.stdout.encoding

"""
去有道词典查找一个单词并下载它的HTML
输入：需要查询的单词
返回：XML格式的文件
"""
def getYoudaoHtml(word='bless'):
    url = r'http://dict.youdao.com/search'
    data = {'le': 'eng', 'q': word, 'keyfrom': 'dict'}
    #加上head，模仿成手机浏览器
    headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
    }
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)
    page = request.urlopen(req).read()

    return page.decode('utf-8')

"""
去查找并写入一个单词的爬取内容，并记录到DownData.txt
输入：word - 需要查询的单词
"""
def WriteOneWord(word='application',file=''):
    wordSoup = BeautifulSoup(getYoudaoHtml(word),"lxml")
    writestr = word+"  "
    exsitif = wordSoup.find('div', class_="trans-container")   #先判断能不能查到单词，查不到会返回None

    if(exsitif is not None):
        meaning = wordSoup.find('div', class_="trans-container").li.string
        writestr = writestr + str(meaning)
        example = wordSoup.find_all('div', class_="examples")
        for line in example:
            for string in line.stripped_strings:
                writestr = writestr +str(string)
    file.write(writestr + "\n")
"""
加载单词表
输入：file - 要打开的单词文件
"""
def loadWords(file):
    fr = open(file)
    ListWord = []
    for line in fr.readlines():
        ListWord.append(line.strip())
    return  ListWord


if __name__ == '__main__':
    List = loadWords('words.txt')
    file = open('DownData.txt', 'w', encoding='utf-8')
    i = 1;size = len(List);
    for word in List:
        WriteOneWord(word,file)
        if(1):
            print("i:{}  word:{}   进度:{:.2%}".format(i,word,i/len(List)))
        i += 1
    print("完成")

    # WriteOneWord('ap258')
    # print(type("asd")== str)

