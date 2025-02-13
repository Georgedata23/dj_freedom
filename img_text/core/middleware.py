import requests

from django.http import JsonResponse

from img_text import settings


class KeycloakMiddleware:
    """ Middleware для проверки JWT-токена в каждом запросе """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """ Проверяем токен перед обработкой запроса """
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            is_valid, user_info = self.verify_token(token)

            if is_valid:
                request.user = user_info  # Передаем user в request
            else:
                return JsonResponse({"error": "Invalid token"}, status=401)
        else:
            request.user = None  # Неавторизованный пользователь

        return self.get_response(request)

    def verify_token(self, token):
        """ Проверяем валидность токена через Keycloak """
        keycloak_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.REALM_NAME}/protocol/openid-connect/userinfo"

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(keycloak_url, headers=headers)

        if response.status_code == 200:
            return True, response.json()
        return False, None