"""Базовый класс для всех Page Object моделей."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
from config.settings import settings


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, driver, wait=None):
        """
        Инициализация базовой страницы.

        Args:
            driver: WebDriver instance
            wait: WebDriverWait instance (optional)
        """
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, settings.TIMEOUT)
        self.base_url = settings.BASE_URL

    @allure.step("Открыть страницу: {url}")
    def open(self, url=""):
        """Открыть указанный URL."""
        full_url = self.base_url + url.lstrip('/')
        self.driver.get(full_url)
        return self

    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator, timeout=None):
        """
        Найти элемент с ожиданием.

        Args:
            locator: Кортеж (By, selector)
            timeout: Время ожидания в секундах

        Returns:
            WebElement: Найденный элемент
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    @allure.step("Найти элементы: {locator}")
    def find_elements(self, locator, timeout=None):
        """
        Найти элементы с ожиданием.

        Args:
            locator: Кортеж (By, selector)
            timeout: Время ожидания в секундах

        Returns:
            List[WebElement]: Список найденных элементов
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step("Кликнуть на элемент: {locator}")
    def click(self, locator, timeout=None):
        """Кликнуть на элемент."""
        element = self.find_element(locator, timeout)
        element.click()
        return self

    @allure.step("Ввести текст '{text}' в элемент: {locator}")
    def type_text(self, locator, text, timeout=None):
        """Ввести текст в поле ввода."""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        return self

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator, timeout=None):
        """Получить текст элемента."""
        element = self.find_element(locator, timeout)
        return element.text

    @allure.step("Проверить видимость элемента: {locator}")
    def is_visible(self, locator, timeout=None):
        """Проверить видимость элемента."""
        try:
            wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Сделать скриншот: {name}")
    def take_screenshot(self, name="screenshot"):
        """Сделать скриншот текущей страницы."""
        self.driver.save_screenshot(f"{settings.SCREENSHOTS_DIR}/{name}.png")
        return self
