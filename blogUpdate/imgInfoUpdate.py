import pymysql
import time


def article_img_update(article_id, article_cla, img_num):
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当天的时间
    max_img_id = mysql_search_max()
    if(img_num < 10):
        for i in range(1, img_num + 1):
            list = []
            list.append(max_img_id + i)
            list.append(article_id + "_0" + str(i) + ".jpg")
            list.append("img/article/" + article_id + "/" + article_id + "_0" + str(i) + ".jpg")
            list.append(article_id)
            list.append(article_cla)
            list.append(today)
            mysql_insert(list)
    elif(img_num >= 10 and img_num < 100):
        for i in range(1, 10):
            list = []
            list.append(max_img_id + i)
            list.append(article_id + "_0" + str(i) + ".jpg")
            list.append("img/article/" + article_id + "/" + article_id + "_0" + str(i) + ".jpg")
            list.append(article_id)
            list.append(article_cla)
            list.append(today)
            mysql_insert(list)
        for i in range(10, img_num + 1):
            list = []
            list.append(max_img_id + i)
            list.append(article_id + "_" + str(i) + ".jpg")
            list.append("img/article/" + article_id + "/" + article_id + "_" + str(i) + ".jpg")
            list.append(article_id)
            list.append(article_cla)
            list.append(today)
            mysql_insert(list)
    print('插入成功')


# 写入mysql数据库
def mysql_insert(result_list):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='myapp',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = "insert into art_img_list(img_id, img_name, img_path, article_id, classification_id, release_time) values({},'{}','{}','{}','{}','{}')".format(result_list[0], result_list[1], result_list[2], result_list[3], result_list[4], result_list[5])
    # print(sql)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()

#查询图片最大id
def mysql_search_max():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='myapp',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = "SELECT max(img_id) max_img_id FROM art_img_list;"
    cur.execute(sql)
    search_list = []
    for r in cur:
        search_list.append(r['max_img_id'])
    conn.commit()
    conn.close()
    return search_list[0]

if __name__ == "__main__":
    article_img_update('art11', 'cla1', 84)