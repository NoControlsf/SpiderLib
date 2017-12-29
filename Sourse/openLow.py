
import time

import pymysql
import requests
from bs4 import BeautifulSoup
import re

class OpenLawSpider:
    #页面初始化
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
        }
    # 获取url
    def getLawList(self):
        for i in range(5531):
            num = i+1
            print('当前爬取页是第%d页' % num)
            time.sleep(10)
            url = 'http://openlaw.cn/search/judgement/default?type=&typeValue=&courtId=&lawFirmId=&lawyerId=&docType=&causeId=&judgeDateYear=&lawSearch=&litigationType=&judgeId=&procedureType=&judgeResult=&courtLevel=&procedureType=&zone=&keyword=%E7%A8%8E%E5%8A%A1%E5%B1%80&page={}'.format(num)
            host = {'host': 'openlaw.cn',}
            headers = self.headers.copy()
            headers.update(host, )
            # 第一步，获取js文件内容
            ret_origin = requests.get(url, headers=headers)
            # print(ret_origin.text)
            cookies = requests.utils.dict_from_cookiejar(ret_origin.cookies)
            # 第二步，js代码并还原j_token计算过程，正则匹配window.v
            cmp = re.compile('window.v="(.*)";')
            rst = cmp.findall(ret_origin.text)
            # print(rst)
            v_token = 'abcdefghijklmnopqrstuvwxyz'
            if len(rst):
                v_token = rst[0]
            j_token = v_token[2:4] + 'n' + v_token[0:1] + 'p' + v_token[4:8] + 'e' + v_token[1:2] + v_token[len(v_token)-17:] + v_token[8:16]
            cookies['j_token'] = j_token
            time.sleep(2)
            ret_next = requests.get(url, headers=headers, cookies=cookies)
            # response = html.fromstring(ret_next.text)
            # items = response.cssselect("div[id=primary] .ht-container .entry-title a")
            # for item in items:
                # title = item.text_content()
                # print(title)
            soup = BeautifulSoup(ret_next.text, 'lxml')
            print(soup)
            h3_list = soup.find_all('h3', class_='entry-title')
            for h3 in h3_list:
                link = h3.find('a')
                link_href = 'http://openlaw.cn%s' % link['href']
                link_title = link.get_text()
                # print(link_href)
                # print(link_title)
                result = []
                result.append(link_href)
                result.append(link_title)
                mysql_insert(result)

    # 获取详细信息
    def getLawDetail(self):
        url = 'http://openlaw.cn/judgement/b8d0c17e14f746308d1a896696e0a246?keyword=%E7%A8%8E%E5%8A%A1%E5%B1%80'
        host = {'host': 'openlaw.cn',}
        headers = self.headers.copy()
        headers.update(host, )
        # 第一步，获取js文件内容
        ret_origin = requests.get(url, headers=headers)
        print(ret_origin.text)
        cookies = requests.utils.dict_from_cookiejar(ret_origin.cookies)
        # 第二步，js代码并还原j_token计算过程，正则匹配window.v
        cmp = re.compile('window.v="(.*)";')
        rst = cmp.findall(ret_origin.text)
        # print(rst)
        v_token = 'abcdefghijklmnopqrstuvwxyz'
        if len(rst):
            v_token = rst[0]
        j_token = v_token[2:4] + 'n' + v_token[0:1] + 'p' + v_token[4:8] + 'e' + v_token[1:2] + v_token[len(v_token)-17:] + v_token[8:16]
        cookies['j_token'] = j_token
        time.sleep(2)
        # 第三步，获取每一个细节内容
        headers['Referer'] = url
        url_detail = 'http://openlaw.cn/judgement/b8d0c17e14f746308d1a896696e0a246?keyword=%E7%A8%8E%E5%8A%A1%E5%B1%80'
        ret_last = requests.get(url_detail, headers=headers, cookies=cookies)
        soup = BeautifulSoup(ret_last.text, 'lxml')
        print(soup)




# 写入mysql数据库
def mysql_insert(result_list):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='shares',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = 'insert into openLaw_list(openlaw_url, openlaw_title) values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    spider = OpenLawSpider()
    spider.getLawList()
    # spider.getLawDetail()

