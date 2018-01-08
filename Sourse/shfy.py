import pymysql
import requests
from bs4 import BeautifulSoup
import re
import time

def download(url, headers, values):
    wb_data = requests.get(url, headers=headers, params=values)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # print(soup)
    return soup

def parse(soup):
    table = soup.find('table')
    tr_list = table.find_all('tr')
    for tr in tr_list[1:]:
        # print(tr)
        str = tr['onclick']
        id_str = re.search('\'(.*)\'', str).group(0)
        id = re.sub('\'(.*?)\'', r'\1', id_str)
        td_list = tr.find_all('td')
        result = []
        result.append(id)
        for td in td_list:
            if td.get_text() != '':
                result.append(td.get_text().replace('\xa0', ''))
            else:
                result.append('')
        print(result)
        mysql_insert(result)

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
    sql = 'insert into shfy_list values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

#搜索爬取页数
def mysql_search_count():
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
    sql = 'SELECT count(*) AS ct FROM shfy_list;'
    # print(sql)
    cur.execute(sql)
    count = 0
    for r in cur:
        count = int(int(r['ct'])/15)
    conn.commit()
    conn.close()
    return count

def shfy():
    count = mysql_search_count()
    for i in range(1348 - count):
        time.sleep(5)
        numb = i+1+count
        url = 'http://www.hshfy.sh.cn/shfy/gweb2017/flws_list_content.jsp'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '127',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'COLLPCK=1652956724; JSESSIONID=8A128EB9866CD8B6E5B067C84D428CA3; Hm_lvt_0ddb2826e0a06f4a6d8ec0be7cebcd47=1514939919; Hm_lpvt_0ddb2826e0a06f4a6d8ec0be7cebcd47=1514942884',
            'Host': 'www.hshfy.sh.cn',
            'Origin': 'http://www.hshfy.sh.cn',
            'Referer': 'http://www.hshfy.sh.cn/shfy/gweb2017/flws_list.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        values = {
            'qwjs': '%E7%A8%8E%E5%8A%A1',
            'pagesnum': numb
        }
        soup = download(url, headers, values)
        parse(soup)


if __name__ == "__main__":
    shfy()