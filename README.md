# wordcloud

通过爬虫爬取我博客里面的所有文章并且down到本地，因为我想要生成全中文的词云，所以只提取了中文字符

# 写在前面

​    这学期开了python课，寻思着之前学的有点忘记了正好趁这个课再温习一下，然后我大意了啊，没想到遇到一个一瓶子不满半瓶子咣当的老师，我单纯的老师甚至连魔法上网的都不知道，他说他都是在晚上一二点下载python的第三方库，这个年纪还得熬夜下载三方库，实属可敬。傻乎乎的老师带着我们上课敲敲书上的案例，我也愉快的摸鱼度过，这不到期末了嘛，听学长说上年作业是爬虫和词云任选一个来写，这才让我这个lazydog重新开了pycharm，哦对了，我傻乎乎的老师还只让我们用IDLE。

![image-20220530182919959](https://s2.loli.net/2022/05/30/rWmVsL6KCA5uPnp.png)

# 准备工作

有了这个想法之后，就开始着手了，关键是我很长时间没写过爬虫了，很多知识点都忘了，不过我的凯华兄弟给了我一个好用的插件，可以直接抓取网页的元素属性，[传送门](https://github.com/huangwc94/scraping-helper-chrome-extension)

![image-20220530183344244](https://s2.loli.net/2022/05/30/B9WMXH6tjnReULv.png)

# 开始动手

我的文章是有好几页的，然后格式就是https://panaceasec.cn/page/1这样子，而每篇文章是不固定的，所以我第一步就是获取所有的url

## 获取url

```
def url_all():
    for page in range(1,7):
        url = 'https://panaceasec.cn/page/'+str(page)
        url_list.append(url)
```

获取url之后，里面有其他文章的标题

![image-20220530184020359](https://s2.loli.net/2022/05/30/wc1r28zDZXnjASk.png)

那么就可以找到具体文章的链接了

## 获取文章链接

通过数据抓取工具得到标题的属性，**post-title-link**，那么就获取到了所有文章的链接

```
def essay_url():
    blog_urls = []
    for url in url_list:
        html = requests.get(url, headers=headers)
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.text, 'html.parser')
        for titles in soup.find_all(attrs={'class':'post-title-link'}):
            urls = titles['href']
            blog_urls.append(urls)
    return blog_urls
```

![image-20220530184523234](https://s2.loli.net/2022/05/30/5wJGxQBrIcvAbph.png)

## 提取并保存文章

然后就可以把每篇文章的源码给爬下来的，以文章标题命名存储为txt

```
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
```

![image-20220530184738060](https://s2.loli.net/2022/05/30/NL2CgXeK57OIMrV.png)

## 提取文章中的关键词到txt

因为有很多不关键的词和符号，就像“的”、“然后”这种，所以需要进行提取一下

```
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
```

里面提到的2.txt里面就是不想要的字，我一开始是直接在代码里面写了个列表，但是后来发现有漏掉的还要一个个加到列表里面，这样很不方便，所以写了个新的txt来设置

![image-20220530185443259](https://s2.loli.net/2022/05/30/o64ZcmNXqDKg7yM.png)

## 提取中文

因为我的词云只想要中文的，但是文章里面不可避免的会有代码这些英文字母，所以在这里直接提取中文字符

```
def text_save(filename, data):
    with open(filename, 'a', encoding='utf-8') as file:
        for i in data:
            if re.findall('[\u4e00-\u9fa5]', i):
                file.write(i)
        print("保存文件成功")
```

这里就可以看到1.txt里面只剩下中文了

![image-20220530185921652](https://s2.loli.net/2022/05/30/RvdoOLgieJm26yz.png)

## 生成词云

接下来就是最后一步啦，读取1.txt，使用jieba库来进行分词和生成图片

```
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
```

## 效果图

![image-20220530190047487](https://s2.loli.net/2022/05/30/nbw7vKEHQY9WeOC.png)

# 写在后面

磨磨唧唧把这个写好了，很多东西都忘掉了，真就面向百度编程了哈哈哈哈哈哈哈哈哈哈，这个爬虫主要是对之前学习的一个回顾吧。不过希望傻乎乎的老师还用上年的课设题目，这样我就不用再写一个了哈哈哈哈哈哈哈哈哈哈

另外附一张之前没提取中文生成的

![image-20220530190414105](https://s2.loli.net/2022/05/30/UwAOxREaohZnIrM.png)

[完整代码](https://github.com/panacea-6/wordcloud)
