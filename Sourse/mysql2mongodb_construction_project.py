import pymysql
from pymongo import MongoClient

def mysql2mongodb():
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
    #sql = "SELECT link_address, link_title, link_date, project_state, belong_area, text_content FROM construction_project;"
    sql = "SELECT link_address, link_title, link_date, text_content FROM government_procurement;"
    cur.execute(sql)
    conn_mogo = MongoClient('localhost', 27017)
    db = conn_mogo.gxlzzbdb  # 连接gxlzzbdb数据库，没有则自动创建
    #my_set = db.construction_project_list  # 使用construction_project_list集合，没有则自动创建
    my_set = db.government_procurement_list  # 使用government_procurement_list集合，没有则自动创建
    for r in cur:
        result_json = {}
        result_json['链接地址'] = r['link_address']
        result_json['链接标题'] = r['link_title']
        result_json['发布时间'] = r['link_date']
        #result_json['工程状态'] = r['project_state']
        #result_json['归属辖区'] = r['belong_area']
        result_json['正文内容'] = r['text_content']

        my_set.insert(result_json)
        print('ok')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    mysql2mongodb()