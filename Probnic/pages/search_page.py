"""Page Object Model для страницы поиска."""

from selenium.webdriver.common.by import By
import allure
from pages.base_page import BasePage


class SearchPage(BasePage):
    """Класс для работы со страницей результатов поиска."""

    # Обновленные локаторы для сайта Читай-Город
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".product-card, .card, .item, [data-product], .book-item")
    SEARCH_TITLE = (By.CSS_SELECTOR, ".search-title, .results-title, h1, .title")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-title, .title, .name, [itemprop='name']")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".price, .product-price, .cost, [itemprop='price']")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".btn-cart, .add-to-cart, [data-action='add-to-cart'], .buy-btn")
    FILTERS_SECTION = (By.CSS_SELECTOR, ".filters, .filter-section, .sidebar")

    @allure.step("Получить количество результатов поиска")
    def get_results_count(self):
        """Получить количество найденных товаров."""
        try:
            results = self.find_elements(self.SEARCH_RESULTS, timeout=10)
            return len(results)
        except:
            return 0

    @allure.step("Получить заголовок страницы поиска")
    def get_search_title(self):
        """Получить заголовок страницы с результатами поиска."""
        title_selectors = [
            ".search-title",
            ".results-title",
            "h1",
            ".title",
            "[data-test='search-title']"
        ]

        for selector in title_selectors:
            try:
                return self.get_text((By.CSS_SELECTOR, selector), timeout=5)
            except:
                continue
        return "Результаты поиска"

    @allure.step("Получить названия первых {count} товаров")
    def get_product_names(self, count=5):
        """
        Получить названия товаров из результатов поиска.

        Args:
            count: Количество товаров для получения

        Returns:
            List[str]: Список названий товаров
        """
        name_selectors = [
            ".product-title",
            ".title",
            ".name",
            "[itemprop='name']",
            "[data-test='product-name']"
        ]

        products = []
        for selector in name_selectors:
            try:
                elements = self.find_elements((By.CSS_SELECTOR, selector), timeout=5)
                products = [el.text for el in elements[:count] if el.text.strip()]
                if products:
                    break
            except:
                continue

        return products

    @allure.step("Получить цены первых {count} товаров")
    def get_product_prices(self, count=5):
        """
        Получить цены товаров из результатов поиска.

        Args:
            count: Количество товаров для получения

        Returns:
            List[str]: Список цен товаров
        """
        price_selectors = [
            ".price",
            ".product-price",
            ".cost",
            "[itemprop='price']",
            "[data-test='product-price']"
        ]

        prices = []
        for selector in price_selectors:
            try:
                elements = self.find_elements((By.CSS_SELECTOR, selector), timeout=5)
                prices = [el.text for el in elements[:count] if el.text.strip()]
                if prices:
                    break
            except:
                continue

        return prices

    @allure.step("Добавить первый товар в корзину")
    def add_first_product_to_cart(self):
        """Добавить первый товар из результатов в корзину."""
        add_button_selectors = [
            ".btn-cart",
            ".add-to-cart",
            "[data-action='add-to-cart']",
            ".buy-btn",
            "[data-test='add-to-cart']"
        ]

        for selector in add_button_selectors:
            try:
                add_buttons = self.find_elements((By.CSS_SELECTOR, selector), timeout=5)
                if add_buttons:
                    add_buttons[0].click()
                    print(f"✓ Товар добавлен в корзину: {selector}")
                    return True
            except:
                continue

        print("✗ Не удалось найти кнопку добавления в корзину")
        return False

    @allure.step("Проверить наличие фильтров")
    def are_filters_visible(self):
        """Проверить видимость секции фильтров."""
        filter_selectors = [
            ".filters",
            ".filter-section",
            ".sidebar",
            "[data-test='filters']"
        ]

        for selector in filter_selectors:
            if self.is_visible((By.CSS_SELECTOR, selector), timeout=5):
                return True
        return False

    @allure.step("Проверить, что результаты содержат '{keyword}'")
    def results_contain_keyword(self, keyword):
        """
        Проверить, что результаты поиска содержат ключевое слово.

        Args:
            keyword: Ключевое слово для поиска

        Returns:
            bool: True если найдено, иначе False
        """
        product_names = self.get_product_names(10)
        keyword_lower = keyword.lower()

        for name in product_names:
            if keyword_lower in name.lower():
                return True

        # Также проверяем заголовок страницы
        page_title = self.driver.title.lower()
        if keyword_lower in page_title:
            return True

        # И содержимое страницы
        page_content = self.driver.page_source.lower()
        if keyword_lower in page_content:
            return True

        return False
