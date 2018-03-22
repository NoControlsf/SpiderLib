import pymysql
from bs4 import BeautifulSoup
from pymongo import MongoClient

#打开页面
def open_text_content():
    link_address = 'http://www.gxlzzb.com/gxlzzbw/ZBGG_Detail.aspx?InfoID=df099c97-5857-4da3-81be-aebbc3c9f99b&CategoryNum=001001009'
    link_address2 = 'http://www.gxlzzb.com/gxlzzbw/ZBGG_Detail.aspx?InfoID=383d3d0f-a0e6-4e36-b845-e7832b7caadf&CategoryNum=001001009'
    search_list = mysql_search_links()
    for link_address_tmp in search_list:
        text_content = mysql_search_text_content(link_address_tmp)
        soup = BeautifulSoup(text_content, 'lxml')
        parse_text_content(link_address_tmp, soup)

#解析页面
def parse_text_content(link_address, soup):
    #print(soup)
    table = soup.find('table', id='tblInfo')
    link_title = table.find('span', id='lblTitle').get_text()
    word_info = table.find('h4', class_='word-info').get_text()
    content = table.find('td', id='TDContent')
    result = content.find('table')
    #判断是否有table，特殊情况不处理
    if(result):
        #print(result)
        td_list = result.find_all('td')
        td_length = len(td_list)

        if(td_length % 2 == 0 and td_length >= 2):
            td_json = {}
            td_json['link_address'] = link_address
            for i in range(0, td_length, 2):
                tmp_key = td_list[i].get_text().replace('\n', '')
                tmp_value = td_list[i+1].get_text().replace('\n', '')
                td_json[tmp_key] = tmp_value
            try:
                mongodb_insert(td_json)
            except:
                print('error')
        elif(td_length % 2 != 0 and td_length >=2):
            td_json = {}
            td_json['link_address'] = link_address
            for i in range(0, td_length-1, 2):
                tmp_key = td_list[i].get_text().replace('\n', '')
                tmp_value = td_list[i+1].get_text().replace('\n', '')
                td_json[tmp_key] = tmp_value
            try:
                mongodb_insert(td_json)
            except:
                print('error')
        else:
            print('error')
    else:
        print('error')


#查询未爬取的链接
def mysql_search_links():
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
    sql = "SELECT link_address FROM construction_project  where ISGET is null LIMIT 200 ;"
    cur.execute(sql)
    search_list = []
    for r in cur:
        search_list.append(r['link_address'])
    conn.commit()
    conn.close()
    return search_list

#通过链接从数据库中获取页面
def mysql_search_text_content(link_address):
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
    sql = "SELECT text_content FROM construction_project  where link_address={} ;".format('\"' + link_address + '\"')
    cur.execute(sql)
    search_list = []
    for r in cur:
        search_list.append(r['text_content'])
    conn.commit()
    conn.close()
    return search_list[0]


def mongodb_insert(b_json):
    conn = MongoClient('localhost', 27017)
    db = conn.gxlzzbdb  # 连接gxlzzbdb数据库，没有则自动创建
    my_set = db.construction_project  # 使用construction_project集合，没有则自动创建
    my_set.insert(b_json)
    print('ok')

if __name__ == "__main__":
    open_text_content()