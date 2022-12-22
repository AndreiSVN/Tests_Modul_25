import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


email = 'svnandr@yandex.ru'
password = 'Aaaa1111'


@pytest.fixture(autouse=True)
def applied_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--new-window')
    applied_driver = webdriver.Chrome('/chromedriver.exe', options=chrome_options)

    # Если используется Firefox, используем эти параметры webdriver
    # firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument('--no-sandbox')
    # firefox_options.add_argument('--new-window')
    # applied_driver= webdriver.Firefox('/firefoxdriver.exe', options=firefox_options)

    applied_driver.get('https://petfriends.skillfactory.ru')

    applied_driver.find_element(By.XPATH, '//button[contains(text(),"Зарегистрироваться")]').click()
    WebDriverWait(applied_driver, 5).until(
        EC.presence_of_all_elements_located((By.LINK_TEXT, 'У меня уже есть аккаунт')))
    applied_driver.find_element(By.LINK_TEXT, 'У меня уже есть аккаунт').click()
    WebDriverWait(applied_driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Войти')]")))
    applied_driver.find_element(By.ID, 'email').send_keys(email)
    applied_driver.find_element(By.ID, 'pass').send_keys(password)
    applied_driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()
    WebDriverWait(applied_driver, 5).until(
        EC.presence_of_all_elements_located((By.LINK_TEXT, 'Мои питомцы')))
    applied_driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
    applied_driver.implicitly_wait(10)
    assert WebDriverWait(applied_driver, 5).until(EC.title_contains('My Pets'))
    yield applied_driver
