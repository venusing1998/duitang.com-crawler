import json
import os
import threading
import urllib

import lxml
import requests
from bs4 import BeautifulSoup


# 设置线程锁
thread_lock = threading.BoundedSemaphore(value=10)


# 获取url
def page_from_url(url):
    html = requests.get(url).content.decode('utf-8')
    return html


# 找出相关label
def page_from_label(label):
    pages = []
    label = urllib.parse.quote(label)
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}&limit=1000'
    for i in range(0, 3000, 100):
        new_url = url.format(label, i)
        page = page_from_url(new_url)
        pages.append(page)
    return pages


# 从page中爬出图片
def find_in_page(page, startpart, endpart):
    image_url = []
    end = 0
    while page.find(startpart, end) != -1:
        start = page.find(startpart, end)+len(startpart)
        end = page.find(endpart, start)
        string = page[start:end]
        image_url.append(string)
    return image_url


# 下载图片
def download_pic(url, label, n):
    r = requests.get(url)
    path = 'result/'+str(label)+'/'+str(n)+'.jpg'
    print('正在下载第'+str(n)+'张图片')
    with open(path, 'wb') as f:
        f.write(r.content)
        thread_lock.release()


# url='https://www.duitang.com/napi/blog/list/by_search/?kw=%E7%A9%B9%E5%A6%B9cos&start=0&limit=1000'
def main(label):
    pages = page_from_label(label)
    n = 0
    for page in pages:
        pics_url = find_in_page(page, 'path":"', '"')
        for pic_url in pics_url:
            n += 1
            # download_pic(pic_url, label, n)
            thread_lock.acquire()
            threading.Thread(target=download_pic,
                             args=(pic_url, label, n)).start()


if __name__ == '__main__':
    print('*'*20, 'begin','*'*20, '\n')
    print('author: Chris\n')
    print('*'*47)
    label = input('Please input the keyword:\n')  # label的东西改变即可
    os.makedirs('result/'+str(label))
    main(label)
