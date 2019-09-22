"""
下载所有的妹子图:
下载所有分组下的图片
"""

import os
import requests
from bs4 import BeautifulSoup
import random

def get_ip_list():
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, features='lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

def get_img():
    url = 'http://www.mzitu.com'
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235',
        'Referer': 'https://www.mzitu.com'
    }
    # proxies = get_random_ip(get_ip_list())
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_li = soup.find('ul', id='pins').find_all('li')
    alt_list = []
    # os.makedirs('Images',exist_ok = True)
    for li in all_li:
        alt = li.find('a').find('img')['alt']
        print(alt)
        alt_list.append(alt)
        page_url = li.find('a')['href']
        print(page_url)
        os.makedirs(os.path.join("Images",alt),exist_ok=True)
        response = requests.get(page_url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 倒数第二项为最大的页数
        max_page = int(soup.find('div', class_='pagenavi').find_all('a')[-2].text)
        index = 1
        for page in range(1, max_page + 1):
            url = page_url + '/' + str(page)
            print(url)
            response = requests.get(url, headers=header)
            soup = BeautifulSoup(response.text, 'html.parser')
            body = soup.body
            img_url = body.find('img')['src']
            img_content = requests.get(img_url, headers=header)
            img_name = str(index) + '.jpg'
            with open(os.path.join("Images",alt, img_name), mode='wb') as f:
                print('正在下载图片...')
                for x in img_content.iter_content(chunk_size=32):
                    f.write(x)
            index += 1



    print('Done')

if __name__ =="__main__":
    get_img()
