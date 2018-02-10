import requests
from bs4 import BeautifulSoup
import pymysql
import time

def amac_manager_one_for_all():
    conn = pymysql.connect(
        host='192.168.16.231',
        port=3306,
        user='bigdata',
        passwd='bigdata',
        db='bigdata',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = "SELECT DISTINCT id FROM AMACAccountList WHERE  type = '一对多';"
    # print(sql)
    cur.execute(sql)
    search_list = []
    for r in cur:
        search_list.append(r['id'])
    conn.commit()
    conn.close()

    conn = pymysql.connect(
        host='192.168.16.231',
        port=3306,
        user='bigdata',
        passwd='bigdata',
        db='bigdata',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = "SELECT DISTINCT id FROM AMACAccountOFA ;"
    # print(sql)
    cur.execute(sql)

    for r in cur:
        search_list.remove(r['id'])
    conn.commit()
    conn.close()

    for fid in search_list:
        time.sleep(15)
        url = 'http://gs.amac.org.cn/amac-infodisc/res/fund/account/{}.html'.format(fid)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'gs.amac.org.cn',
            'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
        }
        wb_data = requests.get(url, headers=headers)
        wb_data.encoding = 'utf-8'
        soup = BeautifulSoup(wb_data.text, 'lxml')
        #print(soup)
        try:
            table = soup.find('table', class_='table table-center table-info')
            tbody = table.find('tbody')
            tr_list = tbody.find_all('tr')
            result = []
            result.append(fid)
            for tr in tr_list:
                td = tr.find('td', class_='td-content')
                result.append(td.get_text().replace('\r', '').replace('\t', '').replace('\n', ''))
            print(result)
            # mysql
            conn = pymysql.connect(
                host='192.168.16.231',
                port=3306,
                user='bigdata',
                passwd='bigdata',
                db='bigdata',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
            cur = conn.cursor()
            sql = 'insert into AMACAccountOFA values({})'.format(('\"%s\",' * len(result))[:-1])
            # print(sql)
            cur.execute(sql % tuple(result))
            cur.close()
            conn.commit()
            conn.close()
        except Exception:
            print(fid)



if __name__ == '__main__':
    amac_manager_one_for_all()