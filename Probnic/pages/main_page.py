"""Page Object Model для главной страницы."""

from selenium.webdriver.common.by import By
import allure
from pages.base_page import BasePage


class MainPage(BasePage):
    """Класс для работы с главной страницей."""

    # Обновленные локаторы для сайта Читай-Город
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='text'], input[type='search'], .search-input, #search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .search-btn, .btn-search")
    COOKIE_ACCEPT = (By.CSS_SELECTOR, "button.cookie-notice__agree, .cookie-accept, [data-test='cookies-accept']")
    CATEGORY_MENU = (By.CSS_SELECTOR, ".header-menu, .menu, nav, .categories")
    CART_BUTTON = (By.CSS_SELECTOR, ".header-cart, .cart-icon, .basket, [href*='cart']")
    USER_ICON = (By.CSS_SELECTOR, ".header-user, .user-icon, .login-btn")
    LOGO = (By.CSS_SELECTOR, ".logo, [href='/'], .header-logo")

    @allure.step("Принять cookies")
    def accept_cookies(self):
        """Принять cookies, если кнопка доступна."""
        cookie_selectors = [
            "button.cookie-notice__agree",
            ".cookie-accept",
            "[data-test='cookies-accept']",
            "button[onclick*='cookie']",
            ".btn-cookie"
        ]

        for selector in cookie_selectors:
            try:
                if self.is_visible((By.CSS_SELECTOR, selector), timeout=3):
                    self.click((By.CSS_SELECTOR, selector))
                    print(f"✓ Cookies приняты с селектором: {selector}")
                    return self
            except:
                continue
        print("✓ Кнопка cookies не найдена или не требуется")
        return self

    @allure.step("Выполнить поиск по запросу: {query}")
    def search_for(self, query):
        """
        Выполнить поиск по указанному запросу.

        Args:
            query: Строка поискового запроса

        Returns:
            SearchPage: Страница результатов поиска
        """
        from pages.search_page import SearchPage

        # Пробуем разные селекторы для поисковой строки
        search_selectors = [
            "input[type='text']",
            "input[type='search']",
            ".search-input",
            "#search",
            "[name='q']",
            "[placeholder*='поиск']",
            "[placeholder*='найти']"
        ]

        search_input = None
        for selector in search_selectors:
            try:
                search_input = self.find_element((By.CSS_SELECTOR, selector), timeout=5)
                print(f"✓ Поисковая строка найдена: {selector}")
                break
            except:
                continue

        if search_input is None:
            raise Exception("Не удалось найти поисковую строку")

        # Очищаем и вводим текст
        search_input.clear()
        search_input.send_keys(query)

        # Пробуем найти и нажать кнопку поиска
        search_button_selectors = [
            "button[type='submit']",
            ".search-btn",
            ".btn-search",
            "[aria-label*='поиск']",
            "[aria-label*='найти']"
        ]

        for selector in search_button_selectors:
            try:
                search_button = self.find_element((By.CSS_SELECTOR, selector), timeout=3)
                search_button.click()
                print(f"✓ Кнопка поиска найдена: {selector}")
                break
            except:
                # Если кнопка не найдена, пробуем отправить через Enter
                search_input.send_keys("\n")
                print("✓ Поиск выполнен через Enter")
                break

        return SearchPage(self.driver, self.wait)

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """Перейти на страницу корзины."""
        from pages.cart_page import CartPage

        cart_selectors = [
            ".header-cart",
            ".cart-icon",
            ".basket",
            "[href*='cart']",
            "[href*='basket']"
        ]

        for selector in cart_selectors:
            try:
                self.click((By.CSS_SELECTOR, selector), timeout=5)
                print(f"✓ Переход в корзину по селектору: {selector}")
                return CartPage(self.driver, self.wait)
            except:
                continue

        raise Exception("Не удалось найти кнопку корзины")

    @allure.step("Проверить наличие поисковой строки")
    def is_search_visible(self):
        """Проверить видимость поисковой строки."""
        search_selectors = [
            "input[type='text']",
            "input[type='search']",
            ".search-input",
            "#search"
        ]

        for selector in search_selectors:
            if self.is_visible((By.CSS_SELECTOR, selector), timeout=5):
                return True
        return False

    @allure.step("Проверить наличие меню категорий")
    def is_category_menu_visible(self):
        """Проверить видимость меню категорий."""
        menu_selectors = [
            ".header-menu",
            ".menu",
            "nav",
            ".categories",
            "[data-test='main-menu']"
        ]

        for selector in menu_selectors:
            if self.is_visible((By.CSS_SELECTOR, selector), timeout=5):
                return True
        return False

    @allure.step("Кликнуть по логотипу")
    def click_logo(self):
        """Кликнуть по логотипу для возврата на главную."""
        logo_selectors = [
            ".logo",
            "[href='/']",
            ".header-logo",
            "[data-test='logo']"
        ]

        for selector in logo_selectors:
            try:
                self.click((By.CSS_SELECTOR, selector), timeout=5)
                print(f"✓ Клик по логотипу: {selector}")
                return self
            except:
                continue

        raise Exception("Не удалось найти логотип")
