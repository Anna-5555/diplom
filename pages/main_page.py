from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self):
        self.driver.get("https://www.chitai-gorod.ru")

    def search_book(self, query: str):
        search_field = self.driver.find_element(By.NAME, "search")
        search_field.clear()
        search_field.send_keys(query)
        self.driver.find_element(
            By.CLASS_NAME, "search-form__icon-search").click()
        WebDriverWait(self.driver, 40).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "search-title"), query))

    def get_search_results_text(self):
        return self.driver.find_element(By.CLASS_NAME, "search-title").text
