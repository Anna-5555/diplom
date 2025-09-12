import requests
import allure


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска книги по автору")
@allure.description("Проверка, что API возвращает книги с ожидаемым автором.")
def test_api_book_by_author(api_base_url, api_headers):
    with allure.step("Отправка запроса поиска по автору 'джоан роулинг'"):
        resp = requests.get(
        f"{api_base_url}search/product?phrase=джоан роулинг", headers=api_headers
        )

    with allure.step("Проверка статус кода 200"):
        assert resp.status_code == 200
        assert 'джоан роулинг' in resp.text

@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска книги по названию")
@allure.description("Проверка, что API возвращает книгу с ожидаемым названием")
def test_api_book_by_title(api_base_url, api_headers):
    with allure.step("Отправка запроса поиска по названию 'капитанская дочка'"):
        resp = requests.get(
        f"{api_base_url}search/product?phrase=капитанская дочка", headers=api_headers
        )
    with allure.step("Проверка статус кода 200"):
        assert resp.status_code == 200
        assert 'капитанская дочка' in resp.text


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска книги по автору на английском")
@allure.description(
    "Проверка, что API возвращает книгу с ожидаемым названием на английском.")
def test_search_by_language_english(api_base_url, api_headers):
    with allure.step("Отправка запроса поиска по фразе 'The lord of rings'"):
        resp = requests.get(
        f"{api_base_url}search/product?phrase=The lord of rings", headers=api_headers
        )

    with allure.step("Проверка статус кода 200"):
        assert resp.status_code == 200
        assert 'The Lord of the Rings' in resp.text


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска с недопустимой японской фразой")
@allure.description(
    "Проверка, что API возвращает ошибку "
    "при поиске с недопустимой японской фразой.")
def test_negative_api_Japanese(api_base_url, api_headers):
    with allure.step("Отправка запроса с японской фразой"):
        resp = requests.get(
        f"{api_base_url}search/product?phrase=人で座ってください", headers=api_headers)

    with allure.step("Проверка статус кода 422"):
        assert resp.status_code == 422


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска с пустым запросом")
@allure.description(
    "Проверка, что API возвращает ошибку при пустом поисковом запросе.")
def test_negative_api_empty_search(api_base_url, api_headers):
    with allure.step("Отправка запроса с пустым поисковым запросом"):
        resp = requests.get(
        f"{api_base_url}search/product?phrase=", headers=api_headers)

    with allure.step("Проверка статус кода 400"):
        assert resp.status_code == 400
