from flask import Flask, render_template, request, redirect
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import pymysql


app = Flask(__name__, template_folder='../templates')


@app.route('/register', methods=['GET', 'POST'])
def register():
    r = render_template('register.html')
    return r


@app.route('/register2', methods=['GET', 'POST'])
def register2():
    r = render_template('register2.html', rname=request.form.get("rusername"))
    username = request.form.get("username")
    pw = request.form.get("password")
    rusername = request.form.get('rusername')
    rpw = request.form.get('rpassword')
    if username is not None:
        with open('/templates/users_info.txt', 'r+', encoding='utf-8') as f:
            if '姓名：{} 密码：{}\n'.format(username, pw) in f.readlines():
                return redirect('/register3')
            else:
                return '用户名或密码错误 \n <a href="/register">重新登陆</a>'

    elif rusername is not None:
        with open('/templates/users_info.txt', 'a+', encoding='utf-8') as f1:
            f1.write('姓名：{} 密码：{}'.format(rusername, rpw))
            f1.write('\n')
        return r


@app.route('/register3', methods=['GET', 'POST'])
def register3():
    r = render_template('register3.html')
    return r


@app.route('/downLoad', methods=['GET', 'POST'])
def downLoad():
    r = render_template('downLoad.html')
    url = request.form.get("url")
    # 连接数据库
    conn = pymysql.connect(user='root', password='zhangxinrong0122', database='test', port=3306)
    cursor = conn.cursor()
    sql = "select url,download_url from down"
    cursor.execute(sql)
    urls = cursor.fetchall()

    for i in urls:
        if i[0] == url:
            return i[1]
    else:
        # 爬虫
        options = webdriver.ChromeOptions()
        # 处理证书错误
        options.add_argument('--ignore-certificate-errors')
        # 修改windows.navigator.webdriver,防机器人识别机制，selenium自动登陆判别机制
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe', options=options)

        driver.get(url)

        driver.find_element_by_xpath("//div[@class='toolbar-btn toolbar-btn-login csdn-toolbar-fl ']/a").click()
        login = driver.find_elements_by_xpath('/html//li[@class="text-tab border-right"]/a')
        login[1].click()
        driver.find_element_by_id('all').send_keys(u'18152674954')
        driver.find_element_by_name('pwd').send_keys(u'zhangxinrong0122')
        driver.find_element_by_class_name('btn.btn-primary').click()
        wait = ui.WebDriverWait(driver, 10)
        wait.until(lambda browser: browser.find_element_by_class_name("c_dl_btn.download_btn.normal_download").click())
        driver.find_element_by_class_name("c_dl_btn.download_btn.normal_download").click()
    return r


if __name__ == '__main__':
    app.run()
