"""Конфигурация pytest с фикстурами."""

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import settings
from data.test_data import test_data  # Добавляем импорт
import os
import allure
from selenium.common.exceptions import WebDriverException


@pytest.fixture(scope="session")
def browser_options():
    """Фикстура настроек браузера."""
    options = Options()
    if settings.HEADLESS:
        options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return options


@pytest.fixture(scope="function")
def driver(browser_options):
    """Фикстура WebDriver."""
    os.makedirs(settings.SCREENSHOTS_DIR, exist_ok=True)

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=browser_options
        )

        # Устанавливаем таймауты
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)

        yield driver

    except WebDriverException as e:
        pytest.fail(f"Не удалось инициализировать WebDriver: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()


@pytest.fixture(scope="function")
def wait(driver):
    """Фикстура WebDriverWait."""
    return WebDriverWait(driver, 15)


@pytest.fixture(scope="function")
def api_session():
    """Фикстура API сессии."""
    session = requests.Session()
    session.timeout = settings.API_TIMEOUT
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.chitai-gorod.ru/',
    })
    return session


@pytest.fixture(scope="function")
def api_base_url():
    """Фикстура базового URL API."""
    return settings.API_URL


@pytest.fixture(scope="function")
def api_endpoints():
    """Фикстура эндпоинтов API."""
    return test_data.API_ENDPOINTS  # Теперь test_data доступен


@pytest.fixture(scope="function")
def main_page(driver, wait):
    """Фикстура главной страницы."""
    from pages.main_page import MainPage
    try:
        page = MainPage(driver, wait)
        page.open()
        page.accept_cookies()
        return page
    except Exception as e:
        pytest.fail(f"Не удалось загрузить главную страницу: {e}")


@pytest.fixture(scope="function")
def test_search_queries():
    """Фикстура поисковых запросов."""
    return test_data.SEARCH_QUERIES


@pytest.fixture(scope="function")
def test_categories():
    """Фикстура категорий."""
    return test_data.CATEGORIES


@pytest.fixture(scope="function")
def screenshot_on_failure(request, driver):
    """Фикстура для создания скриншотов при падении тестов."""
    yield

    if request.node.rep_call.failed:
        test_name = request.node.name.replace(" ", "_")
        screenshot_path = f"{settings.SCREENSHOTS_DIR}/failure_{test_name}.png"
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name="failure_screenshot",
                          attachment_type=allure.attachment_type.PNG)


@pytest.fixture(scope="function")
def cleanup_cookies(driver):
    """Фикстура для очистки cookies после теста."""
    yield
    driver.delete_all_cookies()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания отчетов."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_configure(config):
    """Конфигурация pytest."""
    os.makedirs(settings.ALLURE_RESULTS_DIR, exist_ok=True)
    os.makedirs(settings.SCREENSHOTS_DIR, exist_ok=True)


def pytest_html_report_title(report):
    """Заголовок HTML отчета."""
    report.title = "Тесты для сайта Читай-Город"
