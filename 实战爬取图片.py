import requests
from bs4 import BeautifulSoup
import time
import os
def fire():
    page = 0
    for i in range(0, 120, 30):
        print("开始爬取第 %s 页" % page)
        url = 'https://movie.douban.com/celebrity/1011562/photos/?type=C&start={}&sortby=like&size=a&subtype=a'.format(i)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        try:
            res = requests.get(url,headers=headers).text
            data = get_poster_url(res)
            download_picture(data)
        except Exception as e:
            print("爬取第 %s 页时出错: %s" % (page, str(e)))
        page += 1
        time.sleep(1)

def get_poster_url(res):
    content = BeautifulSoup(res, "html.parser")
    data = content.find_all('div', attrs={'class': 'cover'})
    picture_list = []
    for d in data:
        plist = d.find('img')['src']
        picture_list.append(plist)
    return picture_list

def download_picture(pic_l):
    if not os.path.exists('picture'):
        os.makedirs('picture')
    for i, pic_url in enumerate(pic_l):
        try:
            pic = requests.get(pic_url)
            if pic.status_code == 200:
                p_name = pic_url.split('/')[-1]
                with open(os.path.join('picture', p_name), 'wb') as f:
                    f.write(pic.content)
                print("已下载图片 %s" % p_name)
            else:
                print("下载失败：图片 %s 不存在" % pic_url)
        except Exception as e:
            print("下载图片时出错: %s" % str(e))


if __name__ == '__main__':
    fire()
