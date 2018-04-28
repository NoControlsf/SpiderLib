import json
import re

import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient


class travelSpider:
    #批量下载
    def download_link(self):
        l_stamp = int(time.time() * 1000) - 2
        for i in range(1, 50):
            for j in range(1, 4):
                time.sleep(5)
                l_stamp += 2
                # today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当天的时间
                time_stamp = int(time.time() * 1000)
                #print(time_stamp)
                url = 'http://interface.sina.cn/travel/2017/index_newslist.d.json'
                headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Connection': 'keep-alive',
                    #'Cookie': 'statuid=__10.79.244.19_1522300778_0.46904700; statuidsrc=Mozilla%2F5.0+%28Windows+NT+6.1%3B+WOW64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F62.0.3195.0+Safari%2F537.36%6010.79.244.19%60http%3A%2F%2Finterface.sina.cn%2Ftravel%2F2017%2Findex_newslist.d.json%3Fcallback%3DjQuery172011130977803100306_1522300771635%26type%3Dhot%26cardpage%3D1%26page%3D1%26_%3D1522300773550%60http%3A%2F%2Ftravel.sina.com.cn%2F%60__10.79.244.19_1522300778_0.46904700; ustat=__10.79.244.19_1522300778_0.46904700; genTime=1522300778; vt=4',
                    'Host': 'interface.sina.cn',
                    #'Referer': 'http://travel.sina.com.cn/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
                }
                form_data = {
                    'callback': 'jQuery17209175601412405212_' + str(l_stamp),
                    'type': 'domestic',
                    'cardpage': str(j),
                    'page': str(i),
                    '_': time_stamp
                }
                response = requests.get(url, headers=headers, params=form_data)

                self.parse_link(response)
    #解析
    def parse_link(self, response):
        #print(response.text)
        #res = json.loads(response.text)
        #print(res['data']['docs'])
        """
        json_u = BeautifulSoup(response.text, 'lxml').find('p')
        """
        pattern = re.compile(r'\((.*?)\)')
        result = pattern.findall(response.text)
        #print(result)
        res_json = json.loads(result[0])
        #print(res_json['data'])
        try:
            for tmp in res_json['data']['docs']:
                print(tmp)
                #self.mongodb_insert(tmp)
        except Exception:
            print('error')
            pass
    #入库
    def mongodb_insert(self, b_json):
        conn = MongoClient('localhost', 27017)
        db = conn.sinadb  # 连接sinadb数据库，没有则自动创建
        my_set = db.travel  # 使用travel集合，没有则自动创建
        my_set.insert(b_json)
        print('ok')
    #下载文章
    def download_article(self):
        items = self.mongodb_select()
        for item in items:
            time.sleep(5)
            print(item)
            url = item['url']
            response = requests.get(url)
            response.encoding = 'utf-8'
            self.parse_article(response, item)


    #解析文章
    def parse_article(self, response, item):
        html = BeautifulSoup(response.text, 'lxml').find('div', id='artibody')
        sc = html.find('script')
        s = str(html).replace(str(sc), '')
        #print(s)
        str_html = s.replace('\"', '\\\"')
        #print(str_html)
        item['article'] = str_html
        self.mongodb_insert_article(item)




    #搜索链接
    def mongodb_select(self):
        conn = MongoClient('localhost', 27017)
        db = conn.sinadb  # 连接sinadb数据库，没有则自动创建
        my_set = db.travel  # 使用travel集合，没有则自动创建
        items = my_set.find({}, {"docID": 1, "title": 1, "url": 1, "_id": 0})
        return items

    #存放正文
    def mongodb_insert_article(self, item):
        conn = MongoClient('localhost', 27017)
        db = conn.sinadb  # 连接sinadb数据库，没有则自动创建
        my_set = db.travel_article  # 使用travel_article集合，没有则自动创建
        my_set.insert(item)
        print('ok')


if __name__ == "__main__":
    travelSpider = travelSpider()
    travelSpider.download_link()
    #travelSpider.download_article()