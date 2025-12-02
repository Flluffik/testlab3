from playwright.sync_api import Page, expect
import re

def test_checkout_validation_empty_cart(page: Page):
    """6. Тест: Валидация - попытка оформить пустую корзину."""
    # Открываем корзину и нажимаем "Оформить заказ"
    page.locator("#cartButton").click()
    page.locator("#checkoutButton").click()
    
    # Проверяем, что появилось alert-сообщение (Playwright может его перехватить)
    # Для простоты проверим, что модальное окно НЕ открылось
    modal = page.locator(".modal-overlay")
    expect(modal).not_to_have_class(re.compile(r".*active.*"))
    
    # Также можно проверить, что текст алерта содержит "Корзина пуста"
    # Но это требует специальной настройки для перехвата алертов
    
    print("✅ Попытка оформить пустую корзину корректно отклонена.")

def test_complete_order_flow(page: Page):
    """7. Тест: Полный сценарий оформления заказа."""
    # 1. Добавляем товар
    page.locator("button.add-to-cart").first.click()
    page.wait_for_timeout(300)
    
    # 2. Открываем корзину и переходим к оформлению
    page.locator("#cartButton").click()
    page.locator("#checkoutButton").click()
    
    # 3. Проверяем, что модальное окно открылось
    modal = page.locator(".modal-overlay")
    expect(modal).to_have_class(re.compile(r".*active.*"))
    
    # 4. Заполняем форму корректными данными
    page.locator("#firstName").fill("Иван")
    page.locator("#lastName").fill("Петров")
    page.locator("#address").fill("ул. Ленина, д. 1, кв. 10")
    page.locator("#phone").fill("+79991234567")
    
    # 5. Отправляем форму
    page.locator("button.submit-order").click()
    
    # 6. Проверяем, что появилось сообщение об успехе (alert)
    # В вашем коде после отправки формы вызывается alert('Заказ создан!')
    # Playwright может перехватить этот диалог
    # Для демонстрации просто проверим, что модальное окно закрылось
    expect(modal).not_to_have_class(re.compile(r".*active.*"), timeout=5000)
    
    # 7. Проверяем, что корзина очистилась
    expect(page.locator("#cartCount")).to_have_text("0")
    
    print("✅ Полный сценарий оформления заказа выполнен успешно.")