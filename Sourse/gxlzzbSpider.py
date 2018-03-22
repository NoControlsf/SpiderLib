import pymysql
import requests
import time
from bs4 import BeautifulSoup

#下载链接
def download():
    '''
    url = 'http://www.gxlzzb.com/gxlzzbw//showinfo/jyxxmore.aspx?catgorynum1=004&catgorynum2=007&xiaqu=&type=2'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ASP.NET_SessionId=f20feb55bub4lir1sddi30yi; __CSRFCOOKIE=3a1db239-4490-47a7-b3fc-4b5190cbf0aa; lzzbj=20111113',
        'Host': 'www.gxlzzb.com',
        #'Origin': 'http://www.gxlzzb.com',
        #'Referer': 'http://www.gxlzzb.com/gxlzzbw//showinfo/jyxxmore.aspx?catgorynum1=001&catgorynum2=009&xiaqu=&type=1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    #下载第一页
    wb_data = requests.post(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    print(soup)
    #解析第一页
    view_state, csrf_token, view_stategenerator = parse(soup)
    time.sleep(10)
    '''

    #下载其他网页
    for i in range(1, 21):
        print(i)
        loop_url = 'http://www.gxlzzb.com/gxlzzbw//showinfo/jyxxmore.aspx?catgorynum1=001&catgorynum2=009&xiaqu=&type=1'
        loop_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            #'Content-Length': '6179',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'ASP.NET_SessionId=f20feb55bub4lir1sddi30yi; __CSRFCOOKIE=3a1db239-4490-47a7-b3fc-4b5190cbf0aa; lzzbj=20111113',
            'Host': 'www.gxlzzb.com',
            'Origin': 'http://www.gxlzzb.com',
            'Referer': 'http://www.gxlzzb.com/gxlzzbw//showinfo/jyxxmore.aspx?catgorynum1=001&catgorynum2=009&xiaqu=&type=1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
        }
        form_data = {
            '__CSRFTOKEN': '/wEFJDNhMWRiMjM5LTQ0OTAtNDdhNy1iM2ZjLTRiNTE5MGNiZjBhYQ==',
            '__VIEWSTATE': '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',
            '__VIEWSTATEGENERATOR': 'D38D4441',
            '__EVENTTARGET': 'JyxxSearch1$Pager',
            '__EVENTARGUMENT': i
        }
        #下载
        loop_wb_data = requests.post(loop_url, headers=loop_headers, data=form_data)
        loop_soup = BeautifulSoup(loop_wb_data.text, 'lxml')
        #print(loop_soup)
        #解析
        parse(loop_soup)

def parse(soup):
    table = soup.find('table', id='JyxxSearch1_DataGrid1')
    #print(table)
    td_list = table.find_all('td')
    for td in td_list:
        result = []
        link = td.find('a')
        link_address = 'http://www.gxlzzb.com' + link['href'] #地址
        #print(link_address)
        result.append(link_address)
        link_title = link['title'] #标题
        #print(link_title)
        result.append(link_title)
        link_date = td.find('span', class_='wb-data-date').get_text() #时间
        #print(link_date)
        result.append(link_date)
        span_list = link.find_all('span')
        if(span_list):
            #print(span_list[0].get_text()) #工程状态
            result.append(span_list[0].get_text())
            #print(span_list[1].get_text()) #归属辖区
            result.append(span_list[1].get_text())
        else:
            result.append('')
            result.append('')
        print(result)
        mysql_insert(result)

# 写入mysql数据库
def mysql_insert(result_list):
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
    sql = 'insert into construction_project(link_address, link_title, link_date, project_state, belong_area) values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

#下载详细内容
def download_detail():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId=f20feb55bub4lir1sddi30yi; __CSRFCOOKIE=3a1db239-4490-47a7-b3fc-4b5190cbf0aa; lzzbj=20111113',
        'Host': 'www.gxlzzb.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    #从数据库抽取链接
    search_list = mysql_search_links()
    for link_address in search_list:
        time.sleep(5)
        print(link_address)
        wb_data = requests.get(link_address, headers=headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        parse_detail(link_address, soup)



def parse_detail(link_address, soup):
    table = soup.find('table', id='tblInfo')
    #print(table.get_text())
    link_title = table.find('span', id='lblTitle').get_text()
    word_info = table.find('h4', class_='word-info').get_text()
    table_str = str(table).replace('\"', '\\\"') #符号转义
    mysql_insert2(link_address, table_str)




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


# 原始页面写入mysql数据库
def mysql_insert2(link_address, text_content):
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
    sql = "UPDATE construction_project SET text_content = {} WHERE link_address = {};".format("\"" + str(text_content) + "\"", "\"" + link_address + "\"")
    print(sql)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    #download()
    download_detail()