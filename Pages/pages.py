from datetime import datetime
from symtable import Class
import logging

import pytest
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Tests.conftest import driver



class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = int(timeout)
        self.wait = WebDriverWait(driver, timeout)
        self.page_url = ''
        self.logger = logging.getLogger()

    def find_element(self, by: By or int, value: str) -> WebElement:
        return self.wait.until(expected_conditions.visibility_of_element_located((by, value)),
                               message=f'Элемент {by, value} не найден')

    def find_elements(self, by: By or int, value: str) -> [WebElement]:
        return self.wait.until(expected_conditions.visibility_of_all_elements_located((by, value)),
                               message=f'Элементы {by, value} не найдены')

    def get_current_url(self) -> str:
        return self.driver.current_url


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.login = (By.ID, 'user-name')           #Локатор по ID для элемента строки ввода login
        self.password = (By.ID, 'password')         #Локатор по ID для элемента строки ввода password
        self.login_btn = (By.NAME, 'login-button')  #Локатор по Name для элемента кнопка Login
        self.error_win = (By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]') #Локатор
        self.menu_button = (By.ID,'react-burger-menu-btn')
        self.logout = (By.ID, 'logout_sidebar_link')

    @pytest.mark.parametrize("username, password", [
        ("standard_user", "secret_sauce"),
        ("problem_user", "secret_sauce"),
        ("performance_glitch_user", "secret_sauce"),
        ("error_user", "secret_sauce"),
        ("visual_user", "secret_sauce"),
    ])

    def input_login(self, locator) -> None:
        self.find_element(*self.login).send_keys(locator)

    def input_password(self, locator) -> None:
        self.find_element(*self.password).send_keys(locator)

    def login_button_click(self) -> None:
        self.find_element(*self.login_btn).click()

    def check_error(self):
        # locator = (By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        try:
            self.wait.until(expected_conditions.visibility_of_all_elements_located(self.error_win))
            error_mes = self.find_element(*self.error_win).text
            assert "Epic sadface: Username and password do not match any user in this service" in error_mes
        except:
            expected_url = "https://www.saucedemo.com/inventory.html"
            assert self.get_current_url() == expected_url

    def check_empty_pass(self):
        try:
            self.wait.until(expected_conditions.visibility_of_all_elements_located(self.error_win))
            error_mes = self.find_element(*self.error_win).text
            assert "Epic sadface: Password is required" in error_mes
        except:
            expected_url = "https://www.saucedemo.com/inventory.html"
            assert self.get_current_url() == expected_url

    def all_users(self):
        users = [("standard_user", "secret_sauce"),("problem_user", "secret_sauce"),("performance_glitch_user", "secret_sauce"),("error_user", "secret_sauce"),("visual_user", "secret_sauce"),]
        for username, password in users:
            self.input_login(username)
            self.input_password(password)
            self.login_button_click()
            # self.WaitLoadJQuery()
            # self.find_element(*self.menu_button).click()
            # self.find_element(*self.logout).click()

            expected_url = "https://www.saucedemo.com/inventory.html"
            assert self.get_current_url() == expected_url

            self.find_element(*self.menu_button).click()
            self.find_element(*self.logout).click()

    def WaitLoadJQuery(self):
        try:
            self.wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        except common.exceptions.NoSuchElementException:
            self.logger.info(str(datetime.datetime.now()) + "   ")

class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=5)

        self.page_url = 'https://www.saucedemo.com/inventory.html'

    def check_inventory_page_open(self) -> bool:
        return self.get_current_url() == self.page_url








