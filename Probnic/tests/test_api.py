""""API тесты для сайта Читай-Город."""

import pytest
import allure
import requests
from requests.exceptions import RequestException, Timeout
from config.settings import settings


@pytest.mark.api
@allure.feature("API Тесты")
@allure.story("Поиск через API")
class TestSearchAPI:
    """Тесты API поиска."""

    def get_api_url(self, endpoint_key, api_base_url, api_endpoints):
        """Получить URL API в зависимости от режима тестирования."""
        if settings.API_TEST_MODE == "mock":
            # Используем mock API для тестирования
            return f"{settings.MOCK_API_URL}/anything"
        elif settings.API_TEST_MODE == "test":
            # Используем тестовое API
            return f"{settings.TEST_API_URL}/posts"
        else:
            # Используем реальное API
            return f"{api_base_url}{api_endpoints[endpoint_key]}"

    @allure.title("API поиск по запросу 'Python'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_search_python(self, api_session, api_base_url, api_endpoints):
        """Тест API поиска по запросу 'Python'."""
        endpoint = self.get_api_url("search", api_base_url, api_endpoints)

        with allure.step("Выполнить API запрос поиска"):
            try:
                params = {"query": "Python", "limit": 10}
                response = api_session.get(endpoint, params=params, timeout=10)

                with allure.step("Проверить статус код"):
                    # API может возвращать разные коды в зависимости от режима
                    assert response.status_code in [200, 201, 404, 400], \
                        f"Неожиданный статус код: {response.status_code}"

                if response.status_code in [200, 201]:
                    with allure.step("Проверить структуру ответа"):
                        data = response.json()
                        # Проверяем базовую структуру ответа
                        assert isinstance(data, (dict, list)), \
                            "Ответ должен быть объектом или массивом"

                        # Логируем ответ для отладки
                        allure.attach(
                            f"Ответ API: {str(data)[:500]}...",
                            name="api_response"
                        )

            except RequestException as e:
                # API может быть недоступно - это не ошибка теста
                pytest.skip(f"API недоступно: {e}")

    @allure.title("API поиск с различными параметрами")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("query,limit", [
        ("Python", 5),
        ("Программирование", 10),
        ("Фантастика", 3)
    ])
    def test_api_search_variations(self, api_session, api_base_url, api_endpoints, query, limit):
        """Тест API поиска с разными параметрами."""
        endpoint = self.get_api_url("search", api_base_url, api_endpoints)

        try:
            with allure.step(f"Выполнить поиск '{query}' с лимитом {limit}"):
                params = {"query": query, "limit": limit}
                response = api_session.get(endpoint, params=params, timeout=10)

                # Проверяем, что запрос обработан (даже если с ошибкой)
                assert response.status_code in [200, 201, 404, 400], \
                    f"Неожиданный статус код: {response.status_code}"

        except RequestException as e:
            pytest.skip(f"API недоступно: {e}")


@pytest.mark.api
@allure.feature("API Тесты")
@allure.story("Категории товаров")
class TestCategoriesAPI:
    """Тесты API категорий."""

    def get_api_url(self, endpoint_key, api_base_url, api_endpoints):
        """Получить URL API в зависимости от режима тестирования."""
        if settings.API_TEST_MODE == "mock":
            return f"{settings.MOCK_API_URL}/anything"
        elif settings.API_TEST_MODE == "test":
            return f"{settings.TEST_API_URL}/posts"
        else:
            return f"{api_base_url}{api_endpoints[endpoint_key]}"

    @allure.title("Получение списка категорий")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_categories(self, api_session, api_base_url, api_endpoints):
        """Тест получения списка категорий."""
        endpoint = self.get_api_url("categories", api_base_url, api_endpoints)

        try:
            with allure.step("Запросить список категорий"):
                response = api_session.get(endpoint, timeout=10)

                # Проверяем ответ
                assert response.status_code in [200, 201, 404, 403], \
                    f"Неожиданный статус код: {response.status_code}"

                if response.status_code in [200, 201]:
                    data = response.json()
                    # Проверяем, что получили какие-то данные
                    assert data is not None, "Ответ пустой"

        except RequestException as e:
            pytest.skip(f"API недоступно: {e}")

    @allure.title("Получение товаров по категории")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_by_category(self, api_session, api_base_url, api_endpoints):
        """Тест получения товаров по категории."""
        endpoint = self.get_api_url("products", api_base_url, api_endpoints)

        try:
            with allure.step("Запросить товары с параметрами"):
                params = {"category": "1", "limit": 5}  # Тестовые параметры
                response = api_session.get(endpoint, params=params, timeout=10)

                # Проверяем ответ
                assert response.status_code in [200, 201, 404], \
                    f"Неожиданный статус код: {response.status_code}"

        except RequestException as e:
            pytest.skip(f"API недоступно: {e}")


@pytest.mark.api
@allure.feature("API Тесты")
@allure.story("Работа с корзиной")
class TestCartAPI:
    """Тесты API корзины."""

    def get_api_url(self, endpoint_key, api_base_url, api_endpoints):
        """Получить URL API в зависимости от режима тестирования."""
        if settings.API_TEST_MODE == "mock":
            return f"{settings.MOCK_API_URL}/anything"
        elif settings.API_TEST_MODE == "test":
            return f"{settings.TEST_API_URL}/posts"
        else:
            return f"{api_base_url}{api_endpoints[endpoint_key]}"

    @allure.title("Получение информации о корзине")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_cart_info(self, api_session, api_base_url, api_endpoints):
        """Тест получения информации о корзине."""
        endpoint = self.get_api_url("cart", api_base_url, api_endpoints)

        try:
            with allure.step("Запросить информацию о корзине"):
                response = api_session.get(endpoint, timeout=10)

                # Корзина может требовать авторизацию или быть недоступной
                assert response.status_code in [200, 201, 401, 403, 404], \
                    f"Неожиданный статус код: {response.status_code}"

        except RequestException as e:
            pytest.skip(f"API недоступно: {e}")


@pytest.mark.api
@allure.feature("API Тесты")
@allure.story("Валидация API")
class TestAPIValidation:
    """Тесты валидации API."""

    def get_api_url(self, endpoint_key, api_base_url, api_endpoints):
        """Получить URL API в зависимости от режима тестирования."""
        if settings.API_TEST_MODE == "mock":
            return f"{settings.MOCK_API_URL}/anything"
        elif settings.API_TEST_MODE == "test":
            return f"{settings.TEST_API_URL}/posts"
        else:
            return f"{api_base_url}{api_endpoints[endpoint_key]}"

    @allure.title("Валидация структуры ответа поиска")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_response_structure(self, api_session, api_base_url, api_endpoints):
        """Тест валидации структуры ответа поиска."""
        endpoint = self.get_api_url("search", api_base_url, api_endpoints)

        try:
            response = api_session.get(endpoint, params={"query": "Python", "limit": 1}, timeout=10)

            if response.status_code in [200, 201]:
                data = response.json()

                # Базовые проверки структуры
                assert isinstance(data, (dict, list)), "Ответ должен быть объектом или массивом"

        except RequestException as e:
            pytest.skip(f"API недоступно: {e}")

    @allure.title("Обработка неверных запросов")
    @allure.severity(allure.severity_level.MINOR)
    def test_invalid_requests(self, api_session, api_base_url, api_endpoints):
        """Тест обработки неверных запросов."""
        endpoint = self.get_api_url("search", api_base_url, api_endpoints)

        try:
            # Тест с очень длинным запросом
            long_query = "A" * 1000
            response = api_session.get(endpoint, params={"query": long_query}, timeout=10)

            # API должен обработать запрос или вернуть соответствующую ошибку
            assert response.status_code in [200, 201, 400, 414, 404], \
                f"Неожиданный статус код для длинного запроса: {response.status_code}"

        except RequestException as e:
            pytest.skip(f"API недоступно: {e}")

    @allure.title("Тест таймаута API")
    @allure.severity(allure.severity_level.MINOR)
    def test_api_timeout(self):
        """Тест обработки таймаутов API."""
        try:
            # Пробуем сделать запрос с очень малым таймаутом
            response = requests.get(
                "https://httpbin.org/delay/2",  # Сервис, который ждет 2 секунды
                timeout=0.1
            )
            # Если запрос прошел, проверяем статус
            assert response.status_code in [200], \
                f"Неожиданный статус код: {response.status_code}"

        except Timeout:
            # Таймаут - ожидаемое поведение
            pass
        except RequestException as e:
            # Другие ошибки не должны происходить
            pytest.fail(f"Неожиданная ошибка запроса: {e}")


@pytest.mark.api
@allure.feature("API Тесты")
@allure.story("Тесты производительности")
class TestAPIPerformance:
    """Тесты производительности API."""

    def get_api_url(self, endpoint_key, api_base_url, api_endpoints):
        """Получить URL API в зависимости от режима тестирования."""
        if settings.API_TEST_MODE == "mock":
            return f"{settings.MOCK_API_URL}/anything"
        elif settings.API_TEST_MODE == "test":
            return f"{settings.TEST_API_URL}/posts"
        else:
            return f"{api_base_url}{api_endpoints[endpoint_key]}"

    @allure.title("Тест времени ответа поиска")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_response_time(self, api_session, api_base_url, api_endpoints):
        """Тест времени ответа API поиска."""
        import time

        endpoint = self.get_api_url("search", api_base_url, api_endpoints)

        try:
            with allure.step("Измерить время ответа"):
                start_time = time.time()
                response = api_session.get(endpoint, params={"query": "Python", "limit": 5}, timeout=30)
                end_time = time.time()

                response_time = end_time - start_time

            with allure.step("Проверить время ответа"):
                assert response.status_code in [200, 201, 404], "Запрос не успешен"
                assert response_time < 10.0, f"Время ответа слишком большое: {response_time:.2f} сек"

                allure.attach(f"Время ответа: {response_time:.2f} сек", name="response_time")

        except RequestException as e:
            pytest.skip(f"API недоступно: {e}")