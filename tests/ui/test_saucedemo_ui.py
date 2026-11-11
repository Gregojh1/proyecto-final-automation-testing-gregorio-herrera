import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data_loader import load_json_data
from utils.logger import get_logger

logger = get_logger("TestSauceDemoUI")

# Cargar datasets externos
login_test_cases = load_json_data("data/login_data.json")
checkout_data = load_json_data("data/checkout_data.json")


class TestSauceDemoUI:

    @pytest.mark.parametrize(
        "test_case",
        login_test_cases,
        ids=[tc["case_id"] for tc in login_test_cases]
    )
    def test_01_login_fallido_parametrizado(self, driver, test_case):
        """Caso 1: Escenarios negativos parametrizados con datos externos JSON."""
        logger.info(f"Ejecutando: {test_case['case_id']} - {test_case['description']}")
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(test_case["username"], test_case["password"])

        error_msg = login_page.get_error_message()
        assert error_msg == test_case["expected_error"], (
            f"Se esperaba '{test_case['expected_error']}' pero se obtuvo '{error_msg}'"
        )

    def test_02_login_exitoso(self, driver):
        """Caso 2: Login con credenciales válidas y verificación de catálogo."""
        logger.info("Ejecutando login exitoso con standard_user")
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded(), "La página de inventario no cargó correctamente"
        assert inventory_page.get_title_text() == "Products"

    def test_03_ordenar_productos_por_precio(self, driver):
        """Caso 3: Ordenar productos por precio low-to-high y verificar el orden."""
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        logger.info("Ordenando productos de menor a mayor precio ('lohi')")
        inventory_page.sort_by("lohi")

        prices = inventory_page.get_all_prices()
        logger.info(f"Precios obtenidos: {prices}")
        assert prices == sorted(prices), "La lista de productos no quedó ordenada ascendentemente"

    def test_04_agregar_y_remover_carrito(self, driver):
        """Caso 4: Manejo dinámico del carrito (añadir y quitar producto)."""
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        
        logger.info("Agregando producto 'Backpack' al carrito")
        inventory_page.add_backpack_to_cart()
        assert inventory_page.get_cart_badge_count() == 1, "El badge del carrito debería marcar 1"

        logger.info("Removiendo producto del carrito")
        inventory_page.remove_backpack_from_cart()
        assert inventory_page.get_cart_badge_count() == 0, "El badge del carrito debería desaparecer o estar en 0"

    def test_05_flujo_checkout_completo(self, driver):
        """Caso 5: Flujo completo End-to-End hasta finalizar compra."""
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        inventory_page.add_backpack_to_cart()
        inventory_page.go_to_cart()

        cart_page = CartPage(driver)
        assert cart_page.get_items_count() > 0, "El carrito no contiene productos"
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(driver)
        logger.info("Completando formulario con datos de checkout_data.json")
        checkout_page.fill_information(
            first_name=checkout_data["first_name"],
            last_name=checkout_data["last_name"],
            postal_code=checkout_data["postal_code"]
        )

        logger.info("Finalizando la orden de compra")
        checkout_page.finish_order()

        confirmation = checkout_page.get_confirmation_message()
        assert "Thank you for your order!" in confirmation, (
            f"Mensaje inesperado al finalizar la orden: '{confirmation}'"
        )