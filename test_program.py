from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from helium import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time

username = "username"
password = "password"

default_options = ["--disable-extensions", "--disable-user-media-security=true",
                   "--allow-file-access-from-files", "--use-fake-device-for-media-stream",
                   "--use-fake-ui-for-media-stream", "--disable-popup-blocking",
                   "--disable-infobars", "--enable-usermedia-screen-capturing",
                   "--disable-dev-shm-usage", "--no-sandbox",
                   "--auto-select-desktop-capture-source=Screen 1",
                   "--disable-blink-features=AutomationControlled"]
headless_options = ["--headless", "--use-system-clipboard",
                    "--window-size=1920x1080"]


def browser_options(chrome_type):
    webdriver_options = webdriver.ChromeOptions()
    notification_opt = {"profile.default_content_setting_values.notifications": 1}
    webdriver_options.add_experimental_option("prefs", notification_opt)

    if chrome_type == "headless":
        var = default_options + headless_options
    else:
        var = default_options

    for d_o in var:
        webdriver_options.add_argument(d_o)
        return webdriver_options


def get_webdriver_instance(browser=None):
    base_url = "https://accounts.teachmint.com/"
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"
    driver = webdriver.Chrome(options=browser_options(browser))
    driver.command_executor._commands["send_command"] = ("POST",
                                                         '/session/$sessionId/chromium/send_com,mand')
    driver.maximize_window()
    driver.get(base_url)
    set_driver(driver)
    return driver


def enter_phone_number_otp(driver, creds):
    driver.find_element("xpath", "//input[@type='text']").send_keys(creds[0])
    time.sleep(1)
    print("entered user phone number {}".format(creds[0]))
    driver.find_element("id", "send-otp-btn-id").click()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
    time.sleep(1)
    _input_otp_field = "//input[@data-group-idx='{}']"

    for i, otp in enumerate(creds[1]):
        otp_field = _input_otp_field.format(str(i))
        write(otp, into=S(otp_field))

    print("entered otp {}".format(creds[1]))
    time.sleep(1)
    driver.find_element("id", "submit-otp-btn-id").click()
    time.sleep(2)

    driver.find_element("xpath", '//img[@alt="arrow"]').click()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
    time.sleep(1)
    print("successfully entered user phone number and otp")


def navigate_to_certificate(driver):
    driver.implicitly_wait(5)
    action_object = ActionChains(driver)
    element = driver.find_element("xpath", '//div[text()="Administration"]')
    action_object.move_to_element(element).perform()
    driver.find_element("xpath", '//span[@data-qa="icon-administrator"]').click()
    driver.find_element("xpath", '//a[text()="Certificates"]').click()
    print("navigated to certificate page")


def select_certificate_type(driver):
    driver.implicitly_wait(5)
    driver.find_element("xpath", '//h6[text()="School leaving certificate"]').click()
    print("selected certificate")


def click_on_generate(driver):
    driver.implicitly_wait(5)
    driver.find_element("xpath", '//div[text()="Generate"]').click()
    print("generating the certificate")


def searching_and_select_student(driver):
    driver.implicitly_wait(5)
    driver.find_element("xpath",'// input[ @ name = "search"]').send_keys("sam")
    driver.find_element("xpath", '//div[text()="Generate"]').click()
    print("searching snd selecting the student")


def remarks_update(driver):
    driver.implicitly_wait(5)
    action_object = ActionChains(driver)
    result = driver.find_element("xpath", '//input[@placeholder="Date"]')
    action_object.scroll_to_element(result).send_keys("28/03/2024").perform()
    result2 = driver.find_element("xpath", '//input[@placeholder="Remarks"]')
    action_object.scroll_to_element(result2).send_keys("Good").perform()
    print("updated the remarks")


def generate_and_download(driver):
    driver.find_element("xpath", '//div[text()="Generate"]').click()
    time.sleep(4)
    driver.find_element("xpath", "//div[text()='Download']").click()
    time.sleep(50)
    print("certificate downloaded successfully")


def validation(driver):
    driver.implicitly_wait(3)
    res=driver.find_element("xpath", '///p[@class="krayon__Para-module__VmUAA krayon__Para-module__Qddrw krayon__Para-module__5m3qF krayon__Para-module__Bz9pG"]').text # Sam
    if res.is_displayed():
        print(res,"is displayed ",",","validation complited")
    else:print(" not displayed.....")


def login(admin_credentials=["0000020232", "120992", "@Automation-2"], account_name="@Automation-2"):
    driver = get_webdriver_instance()
    driver.implicitly_wait(5)
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
    time.sleep(1)
    enter_phone_number_otp(driver, admin_credentials)
    user_name = "//div[@class='profile-user-name']/..//div[text()='" + account_name + "']"

    dashboard_xpath = "//a[text()='Dashboard']"
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, dashboard_xpath)))
    time.sleep(20)
    refresh()
    time.sleep(10)
    navigate_to_certificate(driver)
    time.sleep(4)
    select_certificate_type(driver)
    time.sleep(4)
    click_on_generate(driver)
    time.sleep(4)
    searching_and_select_student(driver)
    time.sleep(2)
    remarks_update(driver)
    time.sleep(2)
    generate_and_download(driver)
    return driver


def main():
    login()


# driver.quit()

if __name__ == "__main__":
    print("start")
    main()
    print("end")
