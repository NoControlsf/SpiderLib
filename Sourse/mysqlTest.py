#查询未爬取的企业
import pymysql


def mysql_search_companys():
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
    #sql = "SELECT NSRMC FROM dj_nsrxx  where char_length(NSRMC) >= 4 AND ISGET is null LIMIT 100 ;"
    sql = "SELECT NSRMC FROM dj_nsrxx  where NSRMC = '北京方家廿七餐饮管理有限公司'"
    # print(sql)
    cur.execute(sql)
    search_list = []
    for r in cur:
        search_list.append(r['NSRMC'])
    conn.commit()
    conn.close()
    return search_list

if __name__ == '__main__':
    list = mysql_search_companys()
    for tmp in list:
        print(tmp)