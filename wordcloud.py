import collections
import os
import bs4
import requests
import sys

import wordcloud
from bs4 import BeautifulSoup
import jieba
import re

url_list = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"}

# 获取url
def url_all():
    for page in range(1,7):
        url = 'https://panaceasec.cn/page/'+str(page)
        url_list.append(url)

# 找到所有文章地址
def essay_url():
    blog_urls = []
    for url in url_list:
        html = requests.get(url, headers=headers)
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.text, 'html.parser')
        for titles in soup.find_all(attrs={'class':'post-title-link'}):
            urls = titles['href']
            print(urls)
            blog_urls.append(urls)
    return blog_urls

# 保存文章
def save_path():
    s_path = 'E:/test/'
    if not os.path.isdir(s_path):
        os.mkdir(s_path)
    else:
        pass
    return s_path

# 把文章的文字提取并保存出来
def save_essay(blog_urls,s_path):
    for url in blog_urls:
        blog_html = requests.get(url, headers=headers)
        soup = BeautifulSoup(blog_html.text, 'html.parser')
        content = soup.find_all(attrs={'class': 'post-block'})
        # 正则匹配只选择文字
        content = re.sub('\<.*?\>',"",str(content))
        content = re.sub('&nbsp;', "", content)
        content = re.sub(' ', "", content)
        content = re.sub('\n', "", content)
        try:
            file = open(s_path + url.split("archives/")[1] + '.txt', 'w',encoding='utf-8')
            file.write(content)
            file.close()
        except BaseException as a:
            print(a)
# url_all()
# save_essay(essay_url(),save_path())

# 文本分词存储到txt
def read_word():
    path = "E:\\test"
    files = os.listdir(path)
    object_list = []
    remove_list = []
    with open("2.txt", encoding="utf-8") as f:
        list = f.read()
        for i in list:
            remove_list.append(i)

    # 获取目录下所有的文件
    files = os.listdir(path)
    for file in files:
        loc = os.path.join(path,file)
        with open(loc, encoding="utf-8") as fn:
            fn = fn.read()
            for word in fn:
                if word not in remove_list:
                    object_list.append(word)
    text_save("1.txt",object_list)

# 保存文件1.txt
def text_save(filename, data):
    with open(filename, 'a', encoding='utf-8') as file:
        for i in data:
            if re.findall('[\u4e00-\u9fa5]', i):
                file.write(i)
        print("保存文件成功")


# 生成词云
def word_cloud():
    txt_path = "1.txt"
    with open(txt_path,encoding='utf-8') as f:
        s = f.read()
    ls = jieba.lcut(s)
    text = ' '.join(ls)
    w_c = wordcloud.WordCloud(width=1000,
                                height=700,
                                background_color="white",
                                font_path="C:\Windows\Fonts\msyh.ttc")
    w_c.generate(text)
    w_c.to_file("test1.png")

# read_word()
# word_cloud()

