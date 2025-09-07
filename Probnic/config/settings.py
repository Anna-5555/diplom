"""Настройки окружения для тестов."""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Класс для хранения настроек проекта."""

    # URL сайта
    BASE_URL = "https://www.chitai-gorod.ru/"

    # API URL - используем реалистичные значения
    # Для тестового режима можно использовать mock API или реальные endpoints если доступны
    API_URL = os.getenv("API_URL", "https://api.chitai-gorod.ru/")

    # Альтернативные API URLs для тестирования
    MOCK_API_URL = "https://httpbin.org/"  # Для тестирования HTTP запросов
    TEST_API_URL = "https://jsonplaceholder.typicode.com/"  # Для тестирования JSON API

    # Настройки браузера
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "15"))

    # API настройки
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))

    # Режим тестирования API
    API_TEST_MODE = os.getenv("API_TEST_MODE", "mock")  # mock, real, test

    # Пути
    SCREENSHOTS_DIR = "screenshots"
    ALLURE_RESULTS_DIR = "allure-results"

settings = Settings()
