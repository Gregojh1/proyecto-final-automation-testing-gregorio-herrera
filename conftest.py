import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import get_logger

logger = get_logger("conftest")

@pytest.fixture(scope="function")
def driver(request):
    logger.info("Iniciando navegador...")
    options = Options()
    
    # Asignar la ruta explícita del binario de Brave
    options.binary_location = "/usr/bin/brave-browser"

    # Argumentos para estabilidad
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Modo headless opcional (útil para CI/CD)
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")

    # En Selenium 4.25+ se puede instanciar directamente con options
    # Selenium Manager resolverá el driver compatible de forma automática
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    request.node.driver = driver

    yield driver

    logger.info("Cerrando navegador...")
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura de pantalla automática al fallar para adjuntarla al reporte HTML."""
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.name.replace("/", "_")
            screenshot_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            
            screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            logger.error(f"Test falló. Captura guardada en: {screenshot_path}")

            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                relative_path = os.path.join("screenshots", f"{test_name}_{timestamp}.png")
                extra.append(pytest_html.extras.image(relative_path))
                report.extra = extra