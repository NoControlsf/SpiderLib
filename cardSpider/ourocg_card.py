import json
import requests
import time
from pymongo import MongoClient

def extract(link):
    url = link
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        #'content-length': 2,
        'content-type': 'application/json;charset=UTF-8',
        'cookie': 'pgv_pvi=106384384; pgv_si=s2519507968; _ga=GA1.2.790554509.1525489278; _gid=GA1.2.87575370.1525489278; Hm_lvt_2259a0f4fb9d5c553cd1ec998df4fd58=1525489278,1525489405; Hm_lpvt_2259a0f4fb9d5c553cd1ec998df4fd58=1525491350; XSRF-TOKEN=eyJpdiI6IklcL1VxVFY0eHJ2ZktubHdBMFZxU1JnPT0iLCJ2YWx1ZSI6IjJnSkhvUWpUOXRnRFZKeXlURU81YndzaFFYSURiMkdDZnJia0YxQkJHVVlXWXdoa0xuV2pyRFJhSThQWHBaYUt6UUtXdGdCek5vdERhQWtoQlUwTjh3PT0iLCJtYWMiOiJkZjZlYTJhZDBmOGY4MDhiOTRmOTI5OTg1ZGQwODA4MTg1OTllNGRmMzNlODQxMWM4OGQ5OTU5YTMwZDQxNDhjIn0%3D; ourocg_session=eyJpdiI6ImdWdFZ0Mzdwc0J6MXFmT0p3cmdVNnc9PSIsInZhbHVlIjoiV3ZpUVRnVzJrM0VtTHZBZEhUTERcLzhzOXVJM1Q1Q29ObFhrZWQ0bTYrQ2hhUERKMGdObVNUNjMwNEgyNmV2Sm9GVnp6WDlGUkpDTG5vdXdtQm52N093PT0iLCJtYWMiOiJhYWVhYjhjZTkzNGI2ZWU5ZmRjOWIwYmRhMTlkY2VkNTdhM2NlYmNhZjVhNzNlYjExMzZiZjMyNTQ1NTk0ZDlkIn0%3D; _gat=1',
        'origin': 'https://www.ourocg.cn',
        #referer:https://www.ourocg.cn/card/list-1/2
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'x-csrf-token': 'UPEGLpEdCDSpa79LOJn3BE3xh0Z3rc6seDKpBX3Y',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': 'eyJpdiI6IklcL1VxVFY0eHJ2ZktubHdBMFZxU1JnPT0iLCJ2YWx1ZSI6IjJnSkhvUWpUOXRnRFZKeXlURU81YndzaFFYSURiMkdDZnJia0YxQkJHVVlXWXdoa0xuV2pyRFJhSThQWHBaYUt6UUtXdGdCek5vdERhQWtoQlUwTjh3PT0iLCJtYWMiOiJkZjZlYTJhZDBmOGY4MDhiOTRmOTI5OTg1ZGQwODA4MTg1OTllNGRmMzNlODQxMWM4OGQ5OTU5YTMwZDQxNDhjIn0='
    }
    wb_data = requests.post(url, headers=headers)
    result_json = json.loads(wb_data.text)
    print(result_json['cards'])
    for tmp in result_json['cards']:
        print(tmp)
        conn_mogo = MongoClient('localhost', 27017)
        db = conn_mogo.yugiohdb  # 连接gxlzzbdb数据库，没有则自动创建
        #my_set = db.construction_project_list  # 使用construction_project_list集合，没有则自动创建
        #my_set = db.card_list  # 使用card_list集合，没有则自动创建  怪物卡
        my_set = db.card_list2  # 使用card_list2集合，没有则自动创建 魔法陷阱
        my_set.insert(tmp)


if __name__ == "__main__":
    #for i in range(1, 603):
        #extract('https://www.ourocg.cn/card/list-1/{}'.format(i))
        #time.sleep(2)
    for i in range(271, 301):
        extract('https://www.ourocg.cn/card/list-2/{}'.format(i))