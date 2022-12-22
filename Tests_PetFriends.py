import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from config_for_tests import applied_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestPetFriends:
    def setup(self, applied_driver):
        self.applied_driver = applied_driver

    def test_list_my_pets(self, applied_driver):
        '''Проверка получения списка питомцев пользователя'''
        WebDriverWait(applied_driver, 5).until(EC.title_contains('My Pets'))
        info = applied_driver.find_elements(By.XPATH, "//div[@class='.col-sm-4 left']")
        number = info[0].text.split('\n')
        number = number[1].split(' ')
        number = int(number[1])
        pets = applied_driver.find_elements(By.XPATH, "//tbody/tr")
        assert number == len(pets)
        print(f'\t {number} = {len(pets)}')     # для наглядности и общего понимания выведем количество
                                                # питомцев пользователя

    def test_pets_photo(self, applied_driver):
        '''Проверка наличия фотографии более, чем у половины питомцев пользователя'''
        WebDriverWait(applied_driver, 5).until(EC.title_contains('My Pets'))
        info = applied_driver.find_elements(By.XPATH, "//div[@class='.col-sm-4 left']")
        number = info[0].text.split('\n')
        number = number[1].split(' ')
        number = int(number[1]) // 2

        applied_driver.implicitly_wait(5)
        count = 0
        images = applied_driver.find_elements(By.XPATH,  "//tbody/tr/th/img")
        for i in range(len(images)):
            if 'data' in images[i].get_dom_attribute('src'):
                count += 1
        assert number <= count
        print(f'\t {number} <= {count}')           # для наглядности и понимания сравниваем половину от общего количество
                                                # питомцев и тех, у кого есть фотография

    def test_name_breed_age_present(self, applied_driver):
        '''Проверка наличия имени, породы и возраста у всех питомцев пользователя'''
        WebDriverWait(applied_driver, 5).until(EC.title_contains('My Pets'))
        pet_info = applied_driver.find_elements(By.XPATH, '//tbody/tr/td')
        WebDriverWait(applied_driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, '//tbody')))
        for i in range(len(pet_info)):
            assert pet_info[i].get_attribute('text') != ''
        print('\t All my pets have a name, a breed and an age')

    def test_pet_names_array(self, applied_driver):
        '''Сохранение имен всех питомцев пользователя'''
        WebDriverWait(applied_driver, 5).until(EC.title_contains('My Pets'))
        pet_info = applied_driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
        applied_driver.implicitly_wait(5)
        name_array = []
        for i in range(len(pet_info)):
            name_array.append(pet_info[i].text)
        print(f'\t {name_array}')

    def test_no_repeat(self, applied_driver):
        '''Проверка уникальности всех параметров питомцев пользователя'''
        WebDriverWait(applied_driver, 5).until(EC.title_contains('My Pets'))
        pets = applied_driver.find_elements(By.XPATH, '//tbody/tr')
        names = applied_driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
        breeds = applied_driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
        ages = applied_driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
        applied_driver.implicitly_wait(5)
        list_names = []
        for i in range(len(pets)):
            list_names.append(names[i].text)
        # print(set(list_names))            Для наглядности можно вывести множество уникальных имён
        list_breeds = []
        for i in range(len(pets)):
            list_breeds.append(breeds[i].text)
        # print(set(list_breeds))           Для наглядности можно вывести множество уникальных пород
        list_ages = []
        for i in range(len(pets)):
            list_ages.append(ages[i].text)
        # print(set(list_ages))             Для наглядности можно вывести множество уникальных возрастов
        assert len(set(list_ages)) == len(pets)
        assert len(set(list_names)) == len(pets)
        assert len(set(list_breeds)) == len(pets)
