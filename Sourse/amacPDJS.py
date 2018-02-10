from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置userAgent
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")

driver = webdriver.PhantomJS(executable_path='E:\Learning\phantomjs.exe', desired_capabilities=dcap) #加载网址
driver.set_page_load_timeout(10)
driver.get('http://gs.amac.sql.org.cn/amac.sql-infodisc/res/pof/manager/managerList.html')#打开网址
print(driver.page_source)
driver.quit()