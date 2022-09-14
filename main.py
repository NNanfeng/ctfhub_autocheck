from selenium import webdriver
from selenium.webdriver import Edge, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from chaojiying import Chaojiying_Client#这里是导入了超级鹰的api
from time import sleep
import re
import requests

options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# s= Service(r"F:\PyCharm\ctfhub_auto_check\chromedriver.exe")
# driver = webdriver.Edge(service=s)
driver = Edge(options=options)#这个设置是用来消除[浏览器正在受到自测软件控制]的影响
driver.get('https://www.ctfhub.com/#/user/login')
driver.find_element(By.ID,'account').clear()
driver.find_element(By.ID,'password').clear()
driver.find_element(By.ID,'account').send_keys('account') #填入你的ctfhub账号
driver.find_element(By.ID,'password').send_keys('password') #填入你的ctfhub密码
sleep(1)
cjy = Chaojiying_Client('账号', '密码', '软件id')
while True:
    sleep(1)#这个sleep是我当时想先看看输入的验证码对不对而写的
    img = driver.find_element(By.CLASS_NAME,'getCaptcha').get_attribute('src')
    #print(img)
    b64 = re.findall(r'data:image/png;base64,(.*)', img)[0]
    #print(b64)
    dic = cjy.PostPic_base64(b64, 1902)#这里的b64是加密字符串，1902是超级鹰的验证码类型参数，dic是返回的带有解析出来的验证码的字典
    #print(dic)
    driver.find_element(By.ID,'imgCaptcha').send_keys(dic['pic_str'])  # 写入得到的验证码
    sleep(1)
    driver.find_element(By.ID,'imgCaptcha').send_keys(Keys.ENTER)  # 写入enter，代替了  点击[确定]键 的行为
    sleep(3)
    print(driver.current_url)
    if (driver.current_url == 'https://www.ctfhub.com/#/user/login'):
        print('验证码错误，正在重试')
        cjy.ReportError(dic['pic_id'])
        driver.find_element(By.XPATH,'//*[@id="formLogin"]/div[1]/div[3]/div/div[4]/div[2]').click()#url不变，则登录失败
    else:
        break#改变则登录成功，跳出循环
try:
    driver.refresh()
    print('test pass: refresh successful')#登录成功后先刷新，消除掉弹窗
except Exception as e:
    print("Exception found", format(e))
sleep(3)
move = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div[1]/div/div/div[2]/span[2]')
ActionChains(driver).move_to_element(move).perform()#将鼠标悬停在个人名称上，唤出二级菜单
sleep(3) # 防止二级菜单没出来就点了签到，会出现一些bug
driver.find_element(By.XPATH,'/html/body/div[2]/div/div/ul/li[1]').click()#点击签到
# sleep(3)
message_url = 'https://sctapi.ftqq.com/XXXXXXX.send' #这里我使用了server酱的消息推送 把xxxxx换成你自己的key就可以，如不想使用直接把53-59行代码删除即可
post = {
    'title' : "CTFhub自动签到",
    'desp' : "签到成功",
    'short' : "签到成功"
}
s = requests.post(url=message_url,data=post)
