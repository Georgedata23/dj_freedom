import requests
from django.contrib.auth.models import AnonymousUser

from django.http import JsonResponse, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from img_text import settings
from img_text.settings import DRF_URL

User = get_user_model()


class DRFMiddleware(MiddlewareMixin):
    """ Middleware для проверки JWT-токена """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """ Проверяем токен из куки """
        token_status = False
        token = request.COOKIES.get("access_token")
        print(f"Token from cookies: {token}")

        if token:

            token_status = self._introspect_token(token)
            print(f"token_data_after_introspect: {token_status}")

            if token_status == False:
                new_tokens = self._refresh_token(request)
                print(new_tokens)

                if new_tokens:
                    token = new_tokens["access"]
                    token_status = self._introspect_token(token)


        if token_status == True:
            request.user = self._get_user(token)
        else:
            request.user = AnonymousUser()

        response = self.get_response(request)

        return response

 # Неавторизованный пользователь


    def _introspect_token(self, token):
        """ Проверяем валидность токена через Keycloak """
        DRF_INTROSPECT_URL = f"{DRF_URL}/api/token/verify/"
        response = requests.post(
            DRF_INTROSPECT_URL,
            data={"token": token}
        )
        return True if response.status_code == 200 else False

    def _refresh_token(self, request):
        """ Обновляем токены, если access_token истек """
        refresh_token = request.COOKIES.get("refresh_token")
        DRF_REFRESH_URL = f"{DRF_URL}/api/token/refresh/"
        if not refresh_token:
            return redirect("login/")

        response = requests.post(DRF_REFRESH_URL,
            data={"refresh": refresh_token})

        if response.status_code == 200:
            return response.json()
        return redirect("login/")

    def _get_user(self, token):
        """ Получаем или создаем пользователя """
        USER_INFO_URL = f"{DRF_URL}/api/user/"
        user_response = requests.get(USER_INFO_URL, headers={"Authorization": f"Bearer {token}"})
        if user_response.status_code == 200:
            user_data = user_response.json()
            user_id = user_data.get("id")
            username = user_data.get("username")
            user = User.objects.get(username=username)
            return user
        return AnonymousUser()

