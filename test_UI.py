import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.main_page import MainPage


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
class TestBookSearch:
    @allure.title("Поиск книги по заголовку")
    @allure.description("Тест проверяет возможность "
                        "поиска книги по заголовку 'капитанская'.")
    def test_by_name(self, driver):
        driver.implicitly_wait(20)
        main_page = MainPage(driver)
        main_page.open()
        main_page.search_book("капитанская")
        assert ("Показываем результаты по запросу «капитанская», "
                "найдено:") in main_page.get_search_results_text()

    @allure.title("Поиск автора")
    @allure.description("Тест проверяет возможность поиска автора 'пушкин'.")
    def test_by_name_author(self, driver):
        driver.implicitly_wait(20)
        main_page = MainPage(driver)
        main_page.open()
        main_page.search_book("пушкин")
        assert ("Показываем результаты по запросу «пушкин», "
                "найдено:") in main_page.get_search_results_text()

    @allure.title("Поиск книги на английском")
    @allure.description("Тест проверяет поиск книги с "
                        "использование английского названия")
    def test_by_name_language_english(self, driver):
        driver.implicitly_wait(20)
        main_page = MainPage(driver)
        main_page.open()
        main_page.search_book("house")
        assert ("Показываем результаты по запросу «house», найдено:"
                in main_page.get_search_results_text())

    @allure.title("Поиск книги с символами вместо названия")
    @allure.description("Тест проверяет поиск книги с "
                        "использование символов вместо названия")
    def test_negative_by_symbols(self, driver):
        driver.implicitly_wait(20)
        main_page = MainPage(driver)
        main_page.open()
        main_page.search_book("#$%")
        assert ("Поиск по запросу «#$%» не принёс результатов"
                in main_page.get_search_results_text())

    @allure.title("Поиск книги на тайском языке")
    @allure.description("Тест проверяет поиск книги с "
                        "использование тайских символов в названии")
    def test_negative_by_language_thai(self, driver):
        driver.implicitly_wait(20)
        main_page = MainPage(driver)
        main_page.open()
        main_page.search_book("เกาะมหาสมบัต")
        assert ("Поиск по запросу «เกาะมหาสมบัต» не принёс результатов"
                in main_page.get_search_results_text())
