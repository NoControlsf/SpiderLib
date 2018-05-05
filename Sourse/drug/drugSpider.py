import os

import pymysql
import requests
import time
from bs4 import BeautifulSoup

"""
http://www.yaofang.cn/c/category?cat_id=4454  # 风热感冒 3页
http://www.yaofang.cn/c/category?cat_id=4415  # 清热祛火 4页
http://www.yaofang.cn/c/category?cat_id=2419  # 腹痛腹泻 3页
http://www.yaofang.cn/c/category?cat_id=1526  # 抗菌消炎 5页
http://www.yaofang.cn/c/category?cat_id=6372  # 降脂减肥 1页
"""



def download(link, allpage, drug_type_code,drug_type_name):
    for i in range(allpage):
        page = 40 * i
        if page == 0:
            url = link
        else:
            url = link + '&page={}'.format(page)
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        #print(soup)
        parse(soup, drug_type_code, drug_type_name)


def download_img(imglink, img_name, drug_type_code):
    url = imglink
    html = requests.get(url)
    path = 'd:/drugimg/' + drug_type_code + '/'
    check_filepath(path)
    path_full = path + img_name
    with open(path_full, 'wb') as file:  # 以byte形式将图片数据写入
        file.write(html.content)
        file.flush()
    file.close()  # 关闭文件  )
    time.sleep(1)  # 自定义延时

def parse(soup, drug_type_code, drug_type_name):
    classitfy_drug_list = soup.find_all('div', class_='drug_item')
    for drug_item in classitfy_drug_list:
        result = []
        drug_item_name = drug_item.find('div', class_='drug_item_img').find('a')['title']
        drug_item_code = drug_item.find('div', class_='drug_item_img').find('a')['href'].replace('/goods-', '').replace('.html', '')
        drug_item_imglink = drug_item.find('div', class_='drug_item_img').find('img')['data-original']
        drug_item_imgname = drug_item_code + '.png'
        download_img(drug_item_imglink, drug_item_imgname, drug_type_code)
        drug_size = drug_item.find_all('span')[0].get_text()
        drug_productcompany = drug_item.find_all('span')[1].get_text()

        result.append(drug_item_name)
        result.append(drug_item_code)
        result.append(drug_item_imglink)
        result.append(drug_item_imgname)
        result.append(drug_size)
        result.append(drug_productcompany)
        result.append(drug_type_code)
        result.append(drug_type_name)
        today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 爬取时间
        result.append(today)
        print(result)
        mysql_insert(result)

# 正文写入mysql数据库
def mysql_insert(result_list):
    conn = pymysql.connect(
        host='localhost',
        port=3307,
        user='hmst',
        passwd='hmst',
        db='shares',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = 'insert into drug_info values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

def check_filepath(fn):
    path = os.path.split(fn)[0]
    if not os.path.exists(path):
        os.mkdir(path)


if __name__ == "__main__":
    download('http://www.yaofang.cn/c/category?cat_id=4454', 3, '4454',  '风热感冒')
    download('http://www.yaofang.cn/c/category?cat_id=4415', 4, '4415',  '清热祛火')
    download('http://www.yaofang.cn/c/category?cat_id=2419', 3, '4419',  '腹痛腹泻')
    download('http://www.yaofang.cn/c/category?cat_id=1526', 5, '4426',  '抗菌消炎')
    download('http://www.yaofang.cn/c/category?cat_id=6372', 1, '6372',  '降脂减肥')