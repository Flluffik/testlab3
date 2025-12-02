import pytest
from playwright.sync_api import Page, BrowserContext

@pytest.fixture(scope="function")
def context(browser):
    # Создаем новый контекст с разрешением на доступ к геолокации, камере и т.д., если нужно
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        # Можем эмулировать мобильное устройство, если нужно тестировать responsive.css
        # device_scale_factor=2, is_mobile=True, has_touch=True
    )
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function", autouse=True)
def go_to_home_page(page: Page):
    """Фикстура, которая перед каждым тестом открывает главную страницу."""
    # Playwright может открывать файлы напрямую с диска
    page.goto("file://" + "D:/Downloads/projects vsc/TEST/Online_shop-main/index.html")
    # ИЛИ, если вы запускаете через локальный сервер (рекомендуется):
    # page.goto("http://localhost:8000") 
    yield