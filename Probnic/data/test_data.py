"""Тестовые данные для тестов."""


class TestData:
    """Класс для хранения тестовых данных."""

    # Поисковые запросы
    SEARCH_QUERIES = {
        "python": "Python",
        "python_lower": "python",
        "python_russian": "Пайтон",
        "programming": "Программирование",
        "fiction": "Фантастика"
    }

    # Категории товаров
    CATEGORIES = {
        "books": "Книги",
        "audiobooks": "Аудиокниги",
        "stationery": "Канцтовары"
    }

    # Тестовые пользователи
    TEST_USERS = {
        "valid": {
            "email": "test_user@example.com",
            "password": "TestPassword123"
        },
        "invalid": {
            "email": "invalid@example.com",
            "password": "WrongPassword"
        }
    }

    # API endpoints
    API_ENDPOINTS = {
        "search": "/web/api/v1/search/quick",
        "products": "/web/api/v1/products",
        "categories": "/web/api/v1/categories",
        "cart": "/web/api/v1/cart"
    }


test_data = TestData()
