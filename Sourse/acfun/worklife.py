import json

import pymysql
import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

# 下载器
def download(url, headers):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    print(soup)
    return soup

# 解析器
def parse(soup):
    json_data = soup.find('p')
    result = json.loads(json_data.get_text())
    articleList = result.get('data').get('articleList')
    for article in articleList:
        # print(article)
        art_list = []
        art_list.append(article['channel_id'])
        art_list.append(article['channel_name'])
        art_list.append(article['channel_path'])
        #转换成localtime
        time_local = time.localtime(article['contribute_time']/1000)
        #转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        art_list.append(dt)  # 处理后的时间
        art_list.append(article['description'])
        art_list.append(article['id'])
        art_list.append(article['parent_channel_id'])
        art_list.append(article['parent_channel_name'])
        art_list.append(article['realm_id'])
        art_list.append(article['realm_name'])
        art_list.append(article['title'])
        img_url = article['user_avatar']
        img_name = img_url.split('/')[-1]
        art_list.append(img_name)
        art_list.append(img_url)
        art_list.append(article['user_id'])
        art_list.append(article['username'])
        print(art_list)
        mysql_insert(art_list)
        #mongodb_insert(art_list)


# 写入mysql数据库
def mysql_insert(result_list):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123',
        db='shares',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = "insert into acf_article values({},\"{}\",\"{}\",\"{}\",\"{}\",{},{},\"{}\",{},\"{}\",\"{}\",\"{}\",\"{}\",{},\"{}\")".format(result_list[0], result_list[1], result_list[2],
                                                                                                result_list[3], result_list[4], result_list[5],
                                                                                                result_list[6], result_list[7], result_list[8],
                                                                                                result_list[9], result_list[10], result_list[11],
                                                                                                result_list[12], result_list[13], result_list[14])
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


#写入MongoDB
def mongodb_insert(art_list):
    conn = MongoClient('localhost', 27017)
    db = conn.blogdb  # 连接blogdb数据库，没有则自动创建
    my_set = db.acf  # 使用acf集合，没有则自动创建
    my_list = my_set.find({}, {'_id': 0, 'id': 1})
    print(list(my_list))
    col = {}
    col['channel_id'] = art_list[0]
    col['channel_name'] = art_list[1]
    col['channel_path'] = art_list[2]
    col['contribute_time'] = art_list[3]
    col['description'] = art_list[4]
    col['id'] = art_list[5]
    col['parent_channel_id'] = art_list[6]
    col['parent_channel_name'] = art_list[7]
    col['realm_id'] = art_list[8]
    col['realm_name'] = art_list[9]
    col['title'] = art_list[10]
    col['head_img_name'] = art_list[11]
    col['head_img_url'] = art_list[12]
    col['user_id'] = art_list[13]
    col['username'] = art_list[14]
    #my_set.insert(col)


# 主程序
def work_life():
    url = 'http://webapi.aixifan.com/query/article/list?pageNo=1&size=10&realmIds=6&originalOnly=false&orderType=2&filterTitleImage=true'
    headers = {
                  'Accept': '*/*',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Connection': 'keep-alive',
                  'Origin': 'http://www.acfun.cn',
                  'Host': 'webapi.aixifan.com',
                  'Referer': 'http://www.acfun.cn/v/as6',
                  'User-Agent': 'Mozilla/.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    soup = download(url, headers)
    parse(soup)


if __name__ == "__main__":
    url = 'http://www.acfun.cn/v/as6'
    work_life()