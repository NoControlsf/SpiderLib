import re

import pymysql
import requests
from bs4 import BeautifulSoup

def download_over():
    url = "http://www.jsgs.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=61&endrecord=103&perpage=20"
    headers = {
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        #Content-Length:210
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=HNDCFvWlHV7GNIenFNI1M4bG5Ix0Gpel38n34gTYXJtBXRq360Kg!-1062579983; gwdshare_firstime=1523602459104; cookie=20111113; JSESSIONID1=j8XXhRxPM1Wk9RQqhnrFS7QMv11KTG2lDGTpD0KVbNVrmYXqBBFf!1388393642; _gscs_836343758=23673794p3ivh717|pv:4; _gscbrs_836343758=1; _gscu_836343758=23602458dsb3q517',
        'Host': 'www.jsgs.gov.cn',
        #Origin:http://www.jsgs.gov.cn
        #Referer:http://www.jsgs.gov.cn/col/col1060/index.html?uid=2115&pageNum=2
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    form_data = {
        'col': 1,
        'appid': 1,
        'webid': 1,
        'path': '/',
        'columnid': 1027,
        'sourceContentType': 3,
        'unitid': 1169,
        'webname': '江苏省国家税务局门户网站',
        'permissiontype': 0
    }
    wb_data = requests.post(url, headers=headers, data=form_data)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    parse_over(soup)

def parse_over(soup):
    recordset = soup.find("recordset")
    records = recordset.find_all('record')
    for tr in records:
        result = []
        company_name = tr.find('a').get_text().replace('\n', '').replace('\r', '').replace(' ', '')
        company_link = 'http://www.jsgs.gov.cn' + tr.find('a')['href']
        bt_time = tr.find('span', class_='bt_time').get_text()
        result.append('江苏省')
        result.append(company_name)
        result.append(company_link)
        result.append(bt_time)
        num = mysql_search_links(company_link)
        if num == 0:
            mysql_insert(result)
            print('ok')



def page_change():
    for i in range(1, 720, 60):
        print(i)
        print(i+59)
        download_over2(i, i+59)
    download_over2(721, 755)

def download_over2(startrecord, endrecord):
    url = "http://www.jsgs.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=20".format(startrecord, endrecord)
    headers = {
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        #Content-Length:210
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=HNDCFvWlHV7GNIenFNI1M4bG5Ix0Gpel38n34gTYXJtBXRq360Kg!-1062579983; gwdshare_firstime=1523602459104; cookie=20111113; JSESSIONID1=j8XXhRxPM1Wk9RQqhnrFS7QMv11KTG2lDGTpD0KVbNVrmYXqBBFf!1388393642; _gscs_836343758=23673794p3ivh717|pv:4; _gscbrs_836343758=1; _gscu_836343758=23602458dsb3q517',
        'Host': 'www.jsgs.gov.cn',
        #Origin:http://www.jsgs.gov.cn
        #Referer:http://www.jsgs.gov.cn/col/col1060/index.html?uid=2115&pageNum=2
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    form_data = {
        'col': 1,
        'appid': 1,
        'webid': 1,
        'path': '/',
        'columnid': 1027,
        'sourceContentType': 3,
        'unitid': 1169,
        'webname': '江苏省国家税务局门户网站',
        'permissiontype': 0
    }
    wb_data = requests.post(url, headers=headers, data=form_data)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    parse_over(soup)

def jsgsSpider():
    url = 'http://www.jsgs.gov.cn/col/col1026/index.html'
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup)
    area_links = soup.find_all('div', class_='acco_title1')
    for tmp in area_links[2:]:
        #print(tmp)
        area_link = 'http://www.jsgs.gov.cn' + tmp.find('a')['href']
        area_name = tmp.find('a').get_text()
        print(area_name)
        download_by_area(area_link, area_name)

def download_by_area(area_link, area_name):
    wb_data = requests.get(area_link)
    wb_data.encoding = 'utf-8'
    #print(wb_data.text)
    #nextgroup = re.findall(r'<nextgroup>(.*?)</nextgroup>', wb_data.text)
    recordset = re.findall(r'<!\[CDATA\[(.*?)\]\]>', wb_data.text.replace('\n', '').replace('\r', ''))
    if len(recordset) != 0:
        for record in recordset[1:]:
            tr = BeautifulSoup(record, 'lxml')
            result = []
            company_name = tr.find('a').get_text().replace('\n', '').replace('\r', '').replace(' ', '')
            company_link = 'http://www.jsgs.gov.cn' + tr.find('a')['href']
            bt_time = tr.find('span', class_='bt_time').get_text()
            result.append(area_name)
            result.append(company_name)
            result.append(company_link)
            result.append(bt_time)
            mysql_insert(result)

# 正文写入mysql数据库
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
    sql = 'insert into jsgs_link values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

#查询未爬取的链接
def mysql_search_links(company_link):
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
    sql = "SELECT count(*) AS num FROM jsgs_link  where company_link ='{}';".format(company_link)
    cur.execute(sql)
    search_list = []
    for r in cur:
        search_list.append(r['num'])
    conn.commit()
    conn.close()
    return search_list[0]


if __name__ == "__main__":
    #download_over()
    #jsgsSpider()
    page_change()