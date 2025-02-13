import requests
from django.contrib.auth.models import AnonymousUser

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

from img_text import settings

User = get_user_model()

class KeycloakMiddleware(MiddlewareMixin):
    """ Middleware для проверки JWT-токена """

    def __call__(self, request):
        """ Проверяем токен из куки """
        token = request.COOKIES.get("access_token")
        print(f"Token from cookies: {token}")

        if token:
            token_data = self._introspect_token(token)

            if not token_data or token_data.get("active") == False:
                new_tokens = self._refresh_token(request)

                if new_tokens:
                    token = new_tokens["access_token"]
                    token_data = self._introspect_token(token)
                else:
                    request.user = AnonymousUser()

        request.user = self._get_user(token_data)

        response = self.get_response(request)
        return response

 # Неавторизованный пользователь


    def _introspect_token(self, token):
        """ Проверяем валидность токена через Keycloak """
        KEYCLOAK_INTROSPECT_URL = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.REALM_NAME}/protocol/openid-connect/token/introspect"
        response = requests.post(
            KEYCLOAK_INTROSPECT_URL,
            data={"token": token, "client_id": settings.CLIENT_ID,
                  "client_secret": settings.CLIENT_SECRET},
        )
        return response.json() if response.status_code == 200 else None

    def _refresh_token(self, request):
        """ Обновляем токены, если access_token истек """
        refresh_token = request.COOKIES.get("refresh_token")
        KEYCLOAK_REFRESH_URL = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.REALM_NAME}/protocol/openid-connect/token"
        if not refresh_token:
            return None

        response = requests.post(
            KEYCLOAK_REFRESH_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            },
        )

        if response.status_code == 200:
            return response.json()
        return None

    def _get_user(self, token_data):
        """ Получаем или создаем пользователя """
        user_id = token_data.get("sub")
        email = token_data.get("email", "")
        username = token_data.get("preferred_username", f"user_{user_id}")  # 👈 Даем fallback-username

        user, created = User.objects.get_or_create(username=username, defaults={"email": email})

        return user
        # username = token_data.get("username")
        # user = User.objects.get(username=username)
        # return user

