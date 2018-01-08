import pymysql
import requests
import time
from bs4 import BeautifulSoup
import json

def download(url, headers):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # print(soup)
    return soup

def parse(soup):
    json_data = json.loads(soup.get_text())
    # print(json_data)
    data = json_data['data']
    searchResult = data['searchResult']
    judgements = searchResult['judgements']
    # print(judgements)
    for i in range(len(judgements)):
        tmp = judgements[i]
        tmp_list = []
        tmp_list.append(tmp['id'])
        tmp_list.append(tmp['title'])
        tmp_list.append(tmp['caseType'] if 'caseType' in tmp.keys() else '')
        tmp_list.append(tmp['publishBatch'] if 'publishBatch' in tmp.keys() else '')
        tmp_list.append(tmp['judgementType'] if 'judgementType' in tmp.keys() else '')
        tmp_list.append(tmp['courtName'] if 'courtName' in tmp.keys() else '')
        tmp_list.append(tmp['caseNumber'] if 'caseNumber' in tmp.keys() else '')
        tmp_list.append(tmp['judgementDate'] if 'judgementDate' in tmp.keys() else '')
        tmp_list.append(tmp['courtOpinion'] if 'courtOpinion' in tmp.keys() else '')
        tmp_list.append(tmp['publishDate'] if 'publishDate' in tmp.keys() else '')
        tmp_list.append(tmp['publishType'] if 'publishType' in tmp.keys() else '')
        # print(tmp_list)
        mysql_insert(tmp_list)

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
    sql = 'SELECT count(*) AS ct FROM itslaw_list;'
    # print(sql)
    cur.execute(sql)
    count = 0
    for r in cur:
        count = int(int(r['ct'])/20)
    conn.commit()
    conn.close()
    return count

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
    sql = 'insert into itslaw_list values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

def download_detail(url, headers):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # print(soup)
    return soup

def parse_detail(soup):
    json_data = json.loads(soup.get_text())
    tmp = json_data['data']['fullJudgement']
    # print(tmp)
    """
    tmp_list.append(tmp['caseType'] if 'caseType' in tmp.keys() else '')
    tmp_list.append(tmp['publishBatch'] if 'publishBatch' in tmp.keys() else '')
    tmp_list.append(tmp['judgementType'] if 'judgementType' in tmp.keys() else '')
    tmp_list.append(tmp['courtName'] if 'courtName' in tmp.keys() else '')
    tmp_list.append(tmp['caseNumber'] if 'caseNumber' in tmp.keys() else '')
    tmp_list.append(tmp['judgementDate'] if 'judgementDate' in tmp.keys() else '')
    tmp_list.append(tmp['courtOpinion'] if 'courtOpinion' in tmp.keys() else '')
    tmp_list.append(tmp['publishDate'] if 'publishDate' in tmp.keys() else '')
    tmp_list.append(tmp['publishType'] if 'publishType' in tmp.keys() else '')
    tmp_list.append(tmp['sourceUrl'] if 'sourceUrl' in tmp.keys() else '')
    tmp_list.append(tmp['sourceName'] if 'sourceName' in tmp.keys() else '')
    tmp_list.append(tmp['paragraphs'] if 'paragraphs' in tmp.keys() else '')
    """
    # print(tmp['paragraphs'])
    for i in range(len(tmp['paragraphs'])):
        # print(tmp['paragraphs'][i])
        t = tmp['paragraphs'][i]
        t_list = []
        t_list.append(tmp['id'])
        t_list.append(tmp['title'])
        t_list.append(t['typeText'] if 'paragraphs' in t.keys() else '')
        subParagraphs = ''
        for doc in t['subParagraphs']:
            subParagraphs += (doc['text'].replace('\"', '\''))
        t_list.append(subParagraphs)
        # print(t_list)
        mysql_insert_detail(t_list)

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
    sql = 'SELECT DISTINCT id FROM itslaw_list WHERE NOT  EXISTS (SELECT null  FROM itslaw_detail where itslaw_detail.id = itslaw_list.id);'
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
    sql = 'insert into itslaw_detail values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()



def itlaw_detail():
    search_list = mysql_search()
    for i in search_list:
        time.sleep(5)
        print(i)
        millis = int(round(time.time() * 1000))
        url = 'https://www.itslaw.com/api/v1/detail?timestamp={}&judgementId={}&area=1&sortType=1&conditions=searchWord%2B%E7%A8%8E%E5%8A%A1%E5%B1%80%2B1%2B%E7%A8%8E%E5%8A%A1%E5%B1%80'.format(millis, i)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.itslaw.com',
            'If-Modified-Since': 'Mon, 26 Jul 1997 05:00:00 GMT',
            'Pragma': 'no-cache',
            'Referer': 'https://www.itslaw.com/detail?judgementId={}&area=1&index=1&sortType=1&count=125780&conditions=searchWord%2B%E7%A8%8E%E5%8A%A1%E5%B1%80%2B1%2B%E7%A8%8E%E5%8A%A1%E5%B1%80'.format(i),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
        }
        soup = download_detail(url, headers)
        parse_detail(soup)

def itslaw():
    count = mysql_search_count()
    for i in range(6289 - count):
        time.sleep(5)
        numb = (i + count)*20
        print(numb)
        url = 'https://www.itslaw.com/api/v1/caseFiles?startIndex={}&countPerPage=20&sortType=1&conditions=searchWord%2B%E7%A8%8E%E5%8A%A1%E5%B1%80%2B1%2B%E7%A8%8E%E5%8A%A1%E5%B1%80'.format(numb)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.itslaw.com',
            'If-Modified-Since': 'Mon, 26 Jul 1997 05:00:00 GMT',
            'Pragma': 'no-cache',
            'Referer': 'https://www.itslaw.com/search?searchMode=judgements&sortType=1&conditions=searchWord%2B%E7%A8%8E%E5%8A%A1%E5%B1%80%2B1%2B%E7%A8%8E%E5%8A%A1%E5%B1%80',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
        }
        soup = download(url, headers)
        parse(soup)





if __name__ == "__main__":
    # itslaw()
    itlaw_detail()