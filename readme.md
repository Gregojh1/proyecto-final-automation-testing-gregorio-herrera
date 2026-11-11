# Proyecto Final - Automatización de Pruebas (QA Automation)

Framework integral de pruebas automatizadas end-to-end desarrollado con **Python**, **Selenium WebDriver**, **Pytest** y **Requests**, implementando el patrón de diseño **Page Object Model (POM)** para la capa de UI y cobertura de servicios REST para la capa de API.

---

## Propósito del Proyecto

Asegurar la calidad y estabilidad de los flujos críticos de negocio mediante pruebas automatizadas repetibles y consistentes:
- **UI:** Validación de escenarios de autenticación (positivos y negativos parametrizados), ordenamiento y catálogo de inventario, reactividad del carrito de compras y checkout completo en la plataforma [SauceDemo](https://www.saucedemo.com/).
- **API:** Verificación de métodos HTTP (`GET`, `POST`, `DELETE`), consistencia de esquemas JSON, códigos de respuesta y flujos de encadenamiento de recursos utilizando [ReqRes API](https://reqres.in/).

---

## Tecnologías Utilizadas

- **Lenguaje:** Python 3.10+
- **Test Runner:** Pytest 8.x
- **Automatización Web:** Selenium WebDriver 4.x
- **Gestión de Drivers:** WebDriver Manager
- **Pruebas de API:** Requests
- **Reportes:** Pytest-HTML
- **CI/CD:** GitHub Actions

---

## Estructura del Proyecto

```text
├── .github/workflows/
│   └── run-tests.yml        # Pipeline de Integración Continua (CI/CD)
├── data/
│   ├── login_data.json      # Dataset externo para parametrización de login
│   └── checkout_data.json   # Datos para formulario de checkout
├── logs/
│   └── automation.log       # Registro cronológico detallado de ejecución
├── pages/                   # Page Object Model (POM)
│   ├── base_page.py         # Métodos base y esperas explícitas (WebDriverWait)
│   ├── login_page.py        # Mapeo y acciones de autenticación
│   ├── inventory_page.py    # Catálogo, filtros y manipulación de productos
│   ├── cart_page.py         # Validación del carrito
│   └── checkout_page.py     # Pasos de finalización de orden
├── reports/
│   ├── report.html          # Reporte generado por pytest-html
│   └── screenshots/         # Capturas automáticas capturadas en fallos
├── tests/
│   ├── api/
│   │   ├── conftest.py      # Fixtures de cliente HTTP y base URL
│   │   └── test_api_reqres.py
│   ├── ui/
│   │   └── test_saucedemo_ui.py
│   └── conftest.py          # Fixture del WebDriver y hooks de screenshots
├── utils/
│   ├── data_loader.py       # Utilidad para ingesta de archivos JSON
│   └── logger.py            # Configuración de logs en consola y archivo
├── pytest.ini               # Configuración centralizada de Pytest
├── requirements.txt         # Dependencias del proyecto
└── README.md