import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


base_url = "https://web-gate.chitai-gorod.ru/api/v2/"
auth_token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIyNDAxMzEwLCJpYXQiOjE3NTc2Nzc2OTEsImV4cCI6MTc1NzY4MTI5MSwidHlwZSI6MjAsImp0aSI6IjAxOTkzZGMxLTIzODgtN2NlNy1iYzQzLTcxMWRiZmM5YjZhOSIsInJvbGVzIjoxMH0.If3xSNyLjUO4hBFFgV4Er6xjSXyaiV0Lq83ADO9i01o"
headers = {"User-Agent": "Mozilla/5.0 ("
           "Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ("
           "KHTML, like Gecko) "
                         "Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36",
           "authorization": auth_token}


@pytest.fixture
def driver() -> WebDriver:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def api_base_url():
    return base_url


@pytest.fixture
def api_headers():
    return headers
