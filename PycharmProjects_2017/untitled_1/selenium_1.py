import time
from selenium import webdriver


page = None


def auto_login():
    global page
    page = webdriver.Chrome()
    page.get('http://jxgl.cqu.edu.cn/')
    page.switch_to.frame('frmLogin')

    edit_user = page.find_element_by_id('txt_dsdsdsdjkjkjc')
    edit_user.send_keys('20144297')

    edit_pass = page.find_element_by_id('txt_dsdfdfgfouyy')
    edit_pass.send_keys('zxcvbnm')

    button_login = page.find_element_by_id('Logon')
    button_login.submit()


def auto_select():
    global page
    page.get('http://jxgl.cqu.edu.cn/wsxk/stu_whszk.aspx')
    button_query = page.find_element_by_id('queryButton')
    button_query.submit()

    # classes_list = ['winSKBJ0', 'winSKBJ1', 'winSKBJ2', 'winSKBJ3', 'winSKBJ4', 'winSKBJ5', 'winSKBJ6', 'winSKBJ7', 'winSKBJ8', 'winSKBJ9', 'winSKBJ10', 'winSKBJ11', 'winSKBJ12', 'winSKBJ13' ]
    classes_list = ['winSKBJ13']

    while True:
        time.sleep(5)
        #
        for c in classes_list:
            page.switch_to.frame('frmRpt')
            link_check_course = page.find_element_by_id(c)
            link_check_course.click()
            #
            old_window_handle = page.current_window_handle
            all_window_handles = page.window_handles
            for handle in all_window_handles:
                if handle != old_window_handle:
                    page.switch_to.window(handle)
            #
            check_course = page.find_element_by_id('J')
            if check_course.get_attribute('disabled'):
                page.close()
                page.switch_to.window(old_window_handle)
                continue
            else:
                check_course.click()
                button_sure = page.find_element_by_id('sure')
                button_sure.click()
                page.switch_to.window(old_window_handle)
                break


def auto_submit():
    page.switch_to.default_content()
    button_submit = page.find_element_by_id('actionForm')
    button_submit.submit()


if __name__ == '__main__':
    while True:
        try:
            auto_login()
            auto_select()
            auto_submit()
        except Exception as e:
            print(e)
            time.sleep(20)
        finally:
            page.close()
