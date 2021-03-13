#coding:utf-8
import time
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 导入 webdriver
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.action_chains import ActionChains

# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

# 创建chrome启动选项
chrome_options = webdriver.ChromeOptions()

# 指定chrome启动类型为headless 并且禁用gpu
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')

# 调用环境变量指定的chrome浏览器创建浏览器对象
driver = webdriver.Chrome(options=chrome_options)

def getUserNameList():
    page_text = driver.page_source
    html = etree.HTML(page_text)
    re = html.xpath('//p[@class="columnscontem-title"]/span/text()')
    # print(re)
    # print(len(re));
    return re;

def refreshAll():
    while True:
        # print("拉一次")
        a = driver.find_element_by_id("listLoadMore")
        if a:
            more = a.get_attribute("data-disabled")
            # 获取的更多的视频数据对应的页面数据
            if more == 'true':
                a.click()
            else:
                return;
        # 拉到底操作
        js = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js)
        time.sleep(1)
        driver.execute_script(js)
        time.sleep(1)

# 如果没有在环境变量指定Chrome位置
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/home/wx/application/chromedriver')
# get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
driver.get("https://www.pearvideo.com/userlist.jsp")

kinds = driver.find_elements_by_xpath('//div[@id="domainsList"]/a[@href="javascript:;"]');
indexAll = len(kinds);
for kind in kinds:
    action = ActionChains(driver)
    action.move_to_element(kind).click().perform();

    kindName = kind.get_attribute('textContent')
    print("点击:"+kindName);
    kind.click();
    time.sleep(1);
    
    refreshAll();
    userlist = getUserNameList();
    print("=========")
    print(kind)
    print(userlist)
    print("=========")

# print("end")
# # s = etree.tostring(html, encoding='utf-8').decode('utf-8')

# # 匹配用户名