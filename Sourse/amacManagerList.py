import requests
import json
import time
import pymysql

def amac_manager_list():
    for i in range(432):
        print(i)
        time.sleep(20)
        url = 'http://gs.amac.org.cn/amac-infodisc/api/fund/account?page={}&size=100'.format(i)
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '2',
            'Content-Type': 'application/json',
            'Host': 'gs.amac.org.cn',
            'Origin': 'http://gs.amac.org.cn',
            'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        payload = {}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        print(r)
        r_json = json.loads(r.text)
        list = r_json['content']
        for tmp in list:
            print(tmp)
            result = []
            result.append(tmp['id'])

            timeStamp = tmp['registerDate']/1000
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            result.append(otherStyleTime)
            result.append(tmp['registerCode'])
            result.append(tmp['name'])
            result.append(tmp['type'])
            result.append(tmp['manager'])
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
            sql = 'insert into AMACAccountList values({})'.format(('\"%s\",' * len(result))[:-1])
            # print(sql)
            cur.execute(sql % tuple(result))
            cur.close()
            conn.commit()
            conn.close()

if __name__ == '__main__':
    amac_manager_list()