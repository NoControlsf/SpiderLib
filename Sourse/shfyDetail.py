import pymysql
import requests
from bs4 import BeautifulSoup
import re
import time

def download_detail(url, headers):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # print(soup)
    return soup

def parse_detail(soup, id):
    table = soup.find('table')
    tr_list = table.find_all('tr')
    result =[]
    result.append(id)
    title_tag = tr_list[0].find('div', class_='style2')
    title = ''
    if title_tag != '':
        title = title_tag.get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace('\"', '')
    fileType_tag = tr_list[1].find('div', class_='style1')
    fileType = ''
    if fileType_tag != '':
        fileType = fileType_tag.get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace('\"', '')
    caseNumber_tag = tr_list[2].find('td', align='right')
    caseNumber = ''
    if caseNumber_tag != '':
        caseNumber = caseNumber_tag.get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace('\"', '')
    doc_tag = tr_list[3].find('td')
    doc = ''
    if doc_tag != '':
        doc = doc_tag.get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000', '').replace('\"', '')
    result.append(title)
    result.append(fileType)
    result.append(caseNumber)
    result.append(doc)
    other = ''
    for tr in tr_list[4:]:
        other += (tr.get_text().replace('\"', '') + ';')
    result.append(other)
    # print(result)
    mysql_insert_detail(result)

#搜索未爬取的链接
def mysql_search():
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
    sql = 'SELECT DISTINCT id FROM shfy_list WHERE NOT  EXISTS (SELECT null  FROM shfy_detail where shfy_detail.id = shfy_list.id);'
    # print(sql)
    cur.execute(sql)
    search_list = []
    for r in cur:
        search_list.append(r['id'])
    conn.commit()
    conn.close()
    return search_list

# 正文写入mysql数据库
def mysql_insert_detail(result_list):
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
    sql = 'insert into shfy_detail values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()


def shfy_detail():
    search_list = mysql_search()
    for i in search_list:
        time.sleep(10)
        print(i)
        url = 'http://www.hshfy.sh.cn/shfy/gweb2017/flws_view.jsp?pa={}'.format(i)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'COLLPCK=1652956724; JSESSIONID=8A128EB9866CD8B6E5B067C84D428CA3; Hm_lvt_0ddb2826e0a06f4a6d8ec0be7cebcd47=1514939919; Hm_lpvt_0ddb2826e0a06f4a6d8ec0be7cebcd47=1514942884',
            'Host': 'www.hshfy.sh.cn',
            'Referer': 'http://www.hshfy.sh.cn/shfy/gweb2017/flws_list.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
        }
        soup = download_detail(url, headers)
        parse_detail(soup, i)


if __name__ == "__main__":
    shfy_detail()