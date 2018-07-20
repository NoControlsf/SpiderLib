import pymysql
from pymongo import MongoClient

def mongodb2mysql1():

    conn_mogo = MongoClient('localhost', 27017)
    db = conn_mogo.yugiohdb  # 连接yugiohdb数据库，没有则自动创建
    my_set = db.card_list  # 使用card_list集合，没有则自动创建
    result = my_set.find({}, {"_id": 0})
    for temp in result:
        result_list = []
        print(temp)
        result_list.append(temp['id'])
        result_list.append(temp['hash_id'].replace('\"', '') if temp['hash_id'] != None else '')
        result_list.append(temp['password'].replace('\"', '') if temp['password'] != None else '')
        result_list.append(temp['name'].replace('\"', '') if temp['name'] != None else '')
        result_list.append(temp['name_ja'].replace('\"', '') if temp['name_ja'] != None else '')
        result_list.append(temp['name_en'].replace('\"', '') if temp['name_en'] != None else '')
        result_list.append(temp['locale'].replace('\"', '') if temp['locale'] != None else '')
        result_list.append(temp['type_st'].replace('\"', '') if temp['type_st'] != None else '')
        result_list.append(temp['type_val'].replace('\"', '') if temp['type_val'] != None else '')
        result_list.append('yugioh/' + 'cardimg/' + temp['img_url'].split('/')[-1].replace('\"', '') if temp['img_url'] != None else '')
        result_list.append(temp['level'].replace('\"', '') if temp['level'] != None else '')
        result_list.append(temp['attribute'].replace('\"', '') if temp['attribute'] != None else '')
        result_list.append(temp['race'].replace('\"', '') if temp['race'] != None else '')
        result_list.append(temp['atk'].replace('\"', '') if temp['atk'] != None else '')
        result_list.append(temp['def'].replace('\"', '') if temp['def'] != None else '')
        result_list.append(temp['pend_l'].replace('\"', '') if temp['pend_l'] != None else '')
        result_list.append(temp['pend_r'].replace('\"', '') if temp['pend_r'] != None else '')
        result_list.append(temp['link'].replace('\"', '') if temp['link'] != None else '')
        result_list.append(temp['link_arrow'].replace('\"', '') if temp['link_arrow'] != None else '')
        result_list.append(temp['desc'].replace('\"', '') if temp['desc'] != None else '')
        result_list.append(temp['rare'].replace('\"', '') if temp['rare'] != None else '')
        result_list.append(temp['package'].replace('\"', '') if temp['package'] != None else '')
        result_list.append(temp['href'].replace('\"', '') if temp['href'] != None else '')
        print(result_list)
        mysql_insert(result_list)

#陷阱魔法卡
def mongodb2mysql2():

    conn_mogo = MongoClient('localhost', 27017)
    db = conn_mogo.yugiohdb  # 连接yugiohdb数据库，没有则自动创建
    my_set = db.card_list2  # 使用card_list2集合，没有则自动创建
    result = my_set.find({}, {"_id": 0})
    for temp in result:
        result_list = []
        print(temp)
        result_list.append(temp['id'])
        result_list.append(temp['hash_id'].replace('\"', '') if temp['hash_id'] != None else '')
        result_list.append(temp['password'].replace('\"', '') if temp['password'] != None else '')
        result_list.append(temp['name'].replace('\"', '') if temp['name'] != None else '')
        result_list.append(temp['name_ja'].replace('\"', '') if temp['name_ja'] != None else '')
        result_list.append(temp['name_en'].replace('\"', '') if temp['name_en'] != None else '')
        result_list.append(temp['locale'].replace('\"', '') if temp['locale'] != None else '')
        result_list.append(temp['type_st'].replace('\"', '') if temp['type_st'] != None else '')
        result_list.append(temp['type_val'].replace('\"', '') if temp['type_val'] != None else '')
        result_list.append('yugioh/' + 'cardimg2/' + temp['img_url'].split('/')[-1].replace('\"', '') if temp['img_url'] != None else '')
        result_list.append(temp['desc'].replace('\"', '') if temp['desc'] != None else '')
        result_list.append(temp['rare'].replace('\"', '') if temp['rare'] != None else '')
        result_list.append(temp['package'].replace('\"', '') if temp['package'] != None else '')
        result_list.append(temp['href'].replace('\"', '') if temp['href'] != None else '')
        print(result_list)
        mysql_insert2(result_list)

# 正文写入mysql数据库 怪物卡
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
    sql = 'insert into card_list1 values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

# 正文写入mysql数据库 魔法陷阱卡
def mysql_insert2(result_list):
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
    sql = 'insert into card_list2 values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    mongodb2mysql1()
    mongodb2mysql2()