import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 设置日志文件夹和日志文件名
log_folder = '/Users/chensibin/Documents/pythonLogs'
log_file = 'operation_log.log'

# 确保日志文件夹存在
os.makedirs(log_folder, exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    handlers=[
        logging.FileHandler(os.path.join(log_folder, log_file)),  # 写入日志文件
        logging.StreamHandler()  # 输出到控制台
    ]
)

def click_button_and_handle_popup(driver, button_xpath, popup_xpath, button_name):
    """
    点击指定的按钮，并处理弹出窗口。

    :param driver: WebDriver 实例
    :param button_xpath: 要点击的按钮的 XPath
    :param popup_xpath: 弹出窗口中关闭按钮的 XPath
    :param button_name: 按钮名称，用于日志记录
    """
    try:
        # 等待并点击按钮
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        button.click()
        logging.info(f"{button_name} 按钮已点击。")

        # 等待并处理弹出窗口
        time.sleep(5)  # 等待弹出窗口加载
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, popup_xpath))
            ).click()
            logging.info(f'{button_name} 弹窗关闭按钮已点击。')
        except Exception as e:
            logging.error(f"处理 {button_name} 弹出窗口时出现异常: {e}")

    except Exception as e:
        logging.error(f"点击 {button_name} 按钮时出现异常: {e}")


# 初始化WebDriver
# driver = webdriver.Chrome(ChromeDriverManager().install())
# 使用 Service 对象传递 ChromeDriver 路径
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # 打开指定网址
    logging.info('打开网址: https://myoa.omenow.com/Schedule/MySchedule/')
    driver.get('https://myoa.omenow.com/Schedule/MySchedule/')

    # 输入用户名和密码
    logging.info('输入用户名和密码')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
    ).send_keys('BANS.C')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
    ).send_keys('000000')

    # 点击登录按钮
    logging.info('点击登录按钮')
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loginbtn"]/button'))
    ).click()

    time.sleep(20)

    # 检查并点击签出按钮
    logging.info('检查移动办公签入按钮状态')
    btnHomeWorkingCheckIn_xpath = '//*[@id="btnHomeWorkingCheckIn"]'
    popup_xpath = '//*[@id="popupWindow"]/div/input'

    btnHomeWorkingCheckIn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, btnHomeWorkingCheckIn_xpath))
    )

    if btnHomeWorkingCheckIn.is_enabled():
        click_button_and_handle_popup(driver, btnHomeWorkingCheckIn_xpath, popup_xpath, '移动办公签入')
        time.sleep(5)
    else:
        logging.info('移动办公签入按钮当前处于禁用状态，无法点击。')

    time.sleep(20)

except Exception as e:
    logging.error(f"发生异常: {str(e)}")

finally:
    # 关闭浏览器
    logging.info('关闭浏览器')
    driver.get('https://mycenter.omenow.com/attendance/index/')
    time.sleep(10)
    driver.quit()
