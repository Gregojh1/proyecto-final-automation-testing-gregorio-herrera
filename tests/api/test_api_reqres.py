import pytest
from utils.logger import get_logger

logger = get_logger("TestApiReqres")


class TestApiReqres:

    def test_01_get_users_list(self, api_client):
        """Validar GET de usuarios, status 200, paginación y estructura de la respuesta."""
        url = f"{api_client.base_url}/users?page=2"
        logger.info(f"Enviando GET a: {url}")
        
        response = api_client.get(url)
        logger.info(f"Status Code recibido: {response.status_code}")

        assert response.status_code == 200, f"Se esperaba 200 pero llegó {response.status_code}"
        
        data = response.json()
        assert data["page"] == 2
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

        # Validar estructura del primer usuario
        first_user = data["data"][0]
        for key in ["id", "email", "first_name", "last_name", "avatar"]:
            assert key in first_user, f"Falta el campo '{key}' en el esquema del usuario"

    def test_02_post_create_user(self, api_client):
        """Validar POST para crear un usuario, status 201 y retorno de datos enviados."""
        url = f"{api_client.base_url}/users"
        payload = {
            "name": "Gregorio Herrera",
            "job": "QA Automation Engineer"
        }
        logger.info(f"Enviando POST a {url} con payload: {payload}")
        
        response = api_client.post(url, json=payload)
        logger.info(f"Status Code recibido: {response.status_code}")

        assert response.status_code == 201, f"Se esperaba 201 pero llegó {response.status_code}"
        
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["job"] == payload["job"]
        assert "id" in data
        assert "createdAt" in data

    def test_03_delete_user(self, api_client):
        """Validar DELETE de un usuario y status 204 sin contenido."""
        user_id = 2
        url = f"{api_client.base_url}/users/{user_id}"
        logger.info(f"Enviando DELETE a: {url}")
        
        response = api_client.delete(url)
        logger.info(f"Status Code recibido: {response.status_code}")

        assert response.status_code == 204, f"Se esperaba 204 pero llegó {response.status_code}"
        assert response.text == "", "La respuesta del DELETE debería ser vacía"

    def test_04_encadenamiento_crear_y_validar_recurso(self, api_client):
        """Encadenamiento: Crear un usuario (POST), capturar ID y verificar consistencia de sesión."""
        # 1. Crear usuario
        create_url = f"{api_client.base_url}/users"
        payload = {
            "name": "Mariana Lopez",
            "job": "Software Developer"
        }
        logger.info(f"[Encadenamiento] Creando usuario: {payload['name']}")
        create_response = api_client.post(create_url, json=payload)
        assert create_response.status_code == 201
        
        user_id = create_response.json().get("id")
        logger.info(f"[Encadenamiento] ID generado: {user_id}")
        assert user_id is not None, "El ID generado no puede ser nulo"

        # 2. Consultar o validar recurso dependiente
        single_user_url = f"{api_client.base_url}/users/2"
        logger.info(f"[Encadenamiento] Verificando conectividad hacia endpoint individual: {single_user_url}")
        get_response = api_client.get(single_user_url)
        assert get_response.status_code == 200
        assert get_response.json()["data"]["id"] == 2