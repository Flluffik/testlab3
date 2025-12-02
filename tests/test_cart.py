from playwright.sync_api import Page, expect
import re

def test_catalog_loading(page: Page):
    """1. Тест: Проверка загрузки каталога товаров."""
    # Проверяем, что заголовок секции виден
    expect(page.locator("h2:has-text('Каталог товаров')")).to_be_visible()
    
    # Проверяем, что список товаров загрузился (минимум 8 карточек)
    product_cards = page.locator(".product-card")
    expect(product_cards).to_have_count(8)
    
    # Проверяем, что у первой карточки есть название, цена и кнопка
    first_card = product_cards.first
    expect(first_card.locator(".product-title")).not_to_be_empty()
    expect(first_card.locator(".product-price")).not_to_be_empty()
    expect(first_card.locator("button.add-to-cart")).to_be_visible()
    
    print("✅ Каталог товаров успешно загружен.")

def test_add_item_to_cart_and_update_counter(page: Page):
    """2. Тест: Добавление товара в корзину и проверка счетчика."""
    initial_count = page.locator("#cartCount").inner_text()
    assert initial_count == "0", f"Счетчик корзины должен быть 0, но он {initial_count}"
    
    # Нажимаем кнопку "Добавить в корзину" у первого товара
    first_add_button = page.locator("button.add-to-cart").first
    first_add_button.click()
    
    # Ждем обновления счетчика через Assertion (проверка с таймаутом)
    expect(page.locator("#cartCount")).to_have_text("1")
    
    # Проверяем, что появилось уведомление
    notification = page.locator("div").filter(has_text="Товар добавлен в корзину!")
    expect(notification).to_be_visible()
    # Ждем, когда уведомление исчезнет
    expect(notification).to_be_hidden(timeout=3000)
    
    print("✅ Товар добавлен в корзину, счетчик обновлен.")

def test_cart_sidebar_functionality(page: Page):
    """3. Тест: Работа боковой панели корзины."""
    # Добавляем товар, чтобы корзина не была пустой
    page.locator("button.add-to-cart").first.click()
    page.wait_for_timeout(500) # Небольшая задержка для стабильности
    
    # Открываем корзину
    cart_button = page.locator("#cartButton")
    cart_button.click()
    
    sidebar = page.locator(".cart-sidebar")
    expect(sidebar).to_have_class(re.compile(r".*active.*"))
    
    # Проверяем содержимое корзины
    expect(sidebar.locator(".cart-item")).to_have_count(1)
    expect(sidebar.locator("#cartTotal")).not_to_have_text("0")
    
    # Закрываем корзину
    close_button = page.locator("#closeCart")
    close_button.click()
    expect(sidebar).not_to_have_class(re.compile(r".*active.*"))
    
    print("✅ Боковая панель корзины работает корректно.")

def test_update_item_quantity_in_cart(page: Page):
    """4. Тест: Изменение количества товара в корзине."""
    # Добавляем товар и открываем корзину
    page.locator("button.add-to-cart").first.click()
    page.locator("#cartButton").click()
    
    # Находим элемент управления количеством
    quantity_span = page.locator(".quantity-controls span").first
    increase_button = page.locator(".quantity-btn:has-text('+')").first
    
    # Проверяем начальное количество
    expect(quantity_span).to_have_text("1")
    
    # Увеличиваем количество
    increase_button.click()
    expect(quantity_span).to_have_text("2")
    
    # Проверяем, что итоговая сумма обновилась
    total_text = page.locator("#cartTotal").inner_text()
    total_value = int(total_text)
    # Цена первого товара 179 руб * 2 = 358 руб
    assert total_value == 358, f"Итоговая сумма должна быть 358, но она {total_value}"
    
    print("✅ Количество товара и итоговая сумма обновлены корректно.")

def test_remove_item_from_cart(page: Page):
    """5. Тест: Удаление товара из корзины."""
    # Добавляем товар и открываем корзину
    page.locator("button.add-to-cart").first.click()
    page.locator("#cartButton").click()
    
    # Проверяем, что товар есть
    expect(page.locator(".cart-item")).to_have_count(1)
    
    # Удаляем товар
    remove_button = page.locator("button.remove-item").first
    remove_button.click()
    
    # Проверяем, что корзина пуста
    expect(page.locator(".empty-cart")).to_be_visible()
    expect(page.locator(".cart-item")).to_have_count(0)
    expect(page.locator("#cartTotal")).to_have_text("0")
    
    # Проверяем, что счетчик в шапке тоже обновился
    expect(page.locator("#cartCount")).to_have_text("0")
    
    print("✅ Товар успешно удален из корзины.")
