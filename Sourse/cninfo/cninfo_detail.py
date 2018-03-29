import pymysql
import requests
import time
from bs4 import BeautifulSoup

from Sourse.cninfo import settings

class cninfoSpider:
    #获取数据库配置
    MYSQL_HOSTS = settings.MYSQL_HOSTS
    MYSQL_USER = settings.MYSQL_USER
    MYSQL_PASSWORD = settings.MYSQL_PASSWORD
    MYSQL_PORT = settings.MYSQL_PORT
    MYSQL_DB = settings.MYSQL_DB
    MYSQL_CHARSET = settings.MYSQL_CHARSET
    #获取消息头配置
    USER_AGENT = settings.USER_AGENT

    #下载公司概况
    def download_detail(self, listed_category, stock_code):
        category_code = ''
        if(listed_category == '深市主板'):
            category_code = 'szmb'
        elif(listed_category == '中小板'):
            category_code = 'szsme'
        elif(listed_category == '创业板'):
            category_code = 'szcn'
        elif(listed_category == '沪市主板'):
            category_code = 'shmb'
        url = 'http://www.cninfo.com.cn/information/brief/{}{}.html'.format(category_code, stock_code)
        headers = {
            'User-Agent': self.USER_AGENT
        }
        wb_data = requests.get(url, headers=headers, timeout=15)
        wb_data.encoding = 'gbk'
        self.parse_detail(listed_category, stock_code, wb_data)

    #解析公司概况
    def parse_detail(self, listed_category, stock_code, response):
        #print(BeautifulSoup(response.text, 'lxml'))
        full_name = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[0].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        english_name = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[1].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        registered_address = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[2].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        company_abbreviation = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[3].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        legal_person = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[4].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        company_secretaries = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[5].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        registered_capital = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[6].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        industry_category = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[7].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        postal_code = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[8].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        company_telephone = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[9].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        company_fax = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[10].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        company_website = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[11].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        time_to_market = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[12].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        stock_time = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[13].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        distribution_quantity = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[14].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        issue_price = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[15].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        IPO = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[16].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        distribution_mode = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[17].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        main_underwriter = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[18].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        listed_recommendation = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[19].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')
        sponsor_institution = BeautifulSoup(response.text, 'lxml').find('div', class_='zx_left').find_all('td', class_='zx_data2')[20].get_text().replace('\r', '').replace('\n', '').replace('\xa0', '')

        values = []
        values.append(stock_code)
        values.append(listed_category)
        values.append(full_name)
        values.append(english_name)
        values.append(registered_address)
        values.append(company_abbreviation)
        values.append(legal_person)
        values.append(company_secretaries)
        values.append(registered_capital)
        values.append(industry_category)
        values.append(postal_code)
        values.append(company_telephone)
        values.append(company_fax)
        values.append(company_website)
        values.append(time_to_market)
        values.append(stock_time)
        values.append(distribution_quantity)
        values.append(issue_price)
        values.append(IPO)
        values.append(distribution_mode)
        values.append(main_underwriter)
        values.append(listed_recommendation)
        values.append(sponsor_institution)
        print(values)
        try:
            self.mysql_insert(values)
            self.mysql_update(listed_category, stock_code)
        except Exception:
            print('存储失败')

    #写入数据库
    def mysql_insert(self, values):
        conn = pymysql.connect(
            host=self.MYSQL_HOSTS,
            port=self.MYSQL_PORT,
            user=self.MYSQL_USER,
            passwd=self.MYSQL_PASSWORD,
            db=self.MYSQL_DB,
            charset=self.MYSQL_CHARSET,
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        sql = 'insert into company_profile(stock_code, listed_category, full_name, english_name, registered_address, ' \
              'company_abbreviation, legal_person, company_secretaries, registered_capital, industry_category, postal_code, ' \
              'company_telephone, company_fax, company_website, time_to_market, stock_time, distribution_quantity, issue_price, ' \
              'IPO, distribution_mode, main_underwriter, listed_recommendation, sponsor_institution) ' \
              'values({})'.format(('\"%s\",' * len(values))[:-1])
        # print(sql)
        cur.execute(sql % tuple(values))
        cur.close()
        conn.commit()
        conn.close()

    #查询未爬取的企业
    def mysql_select(self):
        conn = pymysql.connect(
            host=self.MYSQL_HOSTS,
            port=self.MYSQL_PORT,
            user=self.MYSQL_USER,
            passwd=self.MYSQL_PASSWORD,
            db=self.MYSQL_DB,
            charset=self.MYSQL_CHARSET,
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        sql = "SELECT bankuai, daima  FROM shangshi_company  where isget is null and bankuai in('深市主板', '中小板', '创业板', '沪市主板') LIMIT 1000 ;"
        cur.execute(sql)
        search_list = []
        for r in cur:
            company ={
                'listed_category': r['bankuai'],
                'stock_code': r['daima']
            }
            search_list.append(company)
        conn.commit()
        conn.close()
        return search_list

        # 更新状态
    def mysql_update(self, listed_category, stock_code):
        conn = pymysql.connect(
            host=self.MYSQL_HOSTS,
            port=self.MYSQL_PORT,
            user=self.MYSQL_USER,
            passwd=self.MYSQL_PASSWORD,
            db=self.MYSQL_DB,
            charset=self.MYSQL_CHARSET,
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        sql = "UPDATE shangshi_company SET isget = {} WHERE bankuai = {} and daima = {};".format(1, "\"" + str(listed_category) + "\"", "\"" + str(stock_code) + "\"")
        #print(sql)
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

if __name__ == "__main__":

    cninfoSpider = cninfoSpider()
    search_list = cninfoSpider.mysql_select()
    for company in search_list:
        time.sleep(2)
        cninfoSpider.download_detail(company['listed_category'], company['stock_code'])
