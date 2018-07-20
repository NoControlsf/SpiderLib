import json
import os

import requests
import time
from pymongo import MongoClient

def search():
    conn_mogo = MongoClient('localhost', 27017)
    db = conn_mogo.yugiohdb  # 连接gxlzzbdb数据库，没有则自动创建
    #my_set = db.construction_project_list  # 使用construction_project_list集合，没有则自动创建
    my_set = db.card_list  # 使用card_list集合，没有则自动创建  怪物卡
    #my_set = db.card_list2  # 使用card_list2集合，没有则自动创建 魔法陷阱
    result = my_set.find({}, {"img_url": 1, "_id": 0})
    for tmp in result[3364:]:
        print(tmp['img_url'])
        img_name = tmp['img_url'].split('/')[-1]
        print(img_name)
        download_img(tmp['img_url'], img_name)


def download_img(imglink, img_name):
    url = imglink
    html = requests.get(url)
    path = 'f:/yugioh/cardimg/'
    check_filepath(path)
    path_full = path + img_name
    with open(path_full, 'wb') as file:  # 以byte形式将图片数据写入
        file.write(html.content)
        file.flush()
    file.close()  # 关闭文件  )
    time.sleep(1)  # 自定义延时

def check_filepath(fn):
    path = os.path.split(fn)[0]
    if not os.path.exists(path):
        os.mkdir(path)


if __name__ == "__main__":
    search()