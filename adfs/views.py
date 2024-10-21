from onelogin.saml2.auth import OneLogin_Saml2_Auth
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from .saml_config_loader import load_saml_config
from django.views.decorators.csrf import csrf_exempt
from onelogin.saml2.utils import OneLogin_Saml2_Utils
import xml.etree.ElementTree as ET
from base64 import b64decode
from feedback import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
from onelogin.saml2.logout_request import OneLogin_Saml2_Logout_Request
from urllib.parse import urlencode


def prepare_django_request(request):
    if settings.USE_X_FORWARDED_PORT:
        port = '443'
    else:
        port = request.META['SERVER_PORT']

    return {
        'http_host': request.get_host(),
        'script_name': request.META['PATH_INFO'],
        'server_port': port,
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy(),
        'https': 'on',
        'session': request.session
    }


def is_compressed(saml_response):
    try:
        decoded_data = b64decode(saml_response)
        ET.fromstring(decoded_data.decode('utf-8'))
        return False
    except:
        return True


def sso_login(request):
    req = prepare_django_request(request)
    auth = OneLogin_Saml2_Auth(req, load_saml_config())
    return redirect(auth.login())


@csrf_exempt
def acs(request):
    decoded_data = ''
    req = prepare_django_request(request)
    saml_response = req['post_data'].get('SAMLResponse', None)

    if not saml_response:
        return HttpResponse("SAMLResponse is missing.")

    if is_compressed(saml_response):
        try:
            decoded_data = OneLogin_Saml2_Utils.decode_base64_and_inflate(saml_response)
        except Exception as e:
            return HttpResponse(f"Error during decompression: {str(e)}")
    else:
        try:
            decoded_data = OneLogin_Saml2_Utils.b64decode(saml_response)
        except Exception as e:
            return HttpResponse(f"Base64 decoding error: {str(e)}")

    if decoded_data:

        auth = OneLogin_Saml2_Auth(req, load_saml_config())

        auth.process_response()
        errors = auth.get_errors()

        if not errors:
            if auth.is_authenticated():

                attributes = auth.get_attributes()
                email = attributes.get('http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress', [None])[0]

                if email:
                    try:
                        user = User.objects.get(username='ISurin@croc.ru')
                        login(request, user)

                        request.session['samlNameId'] = auth.get_nameid()
                        request.session['samlSessionIndex'] = auth.get_session_index()
                        return redirect('/')

                    except User.DoesNotExist:
                        return HttpResponse("Ooops вас нет в базе!")
                else:
                    return HttpResponse("Не удалось получить email из SAML ответа.", status=400)
        else:
            error_reason = auth.get_last_error_reason()
            return HttpResponse(f"Error during authentication: {str(errors)}. Reason: {error_reason}")


# def sso_logout(request):
#     # Получаем URL для завершения сессии, если пользователь аутентифицирован
#     name_id = request.session.get('samlNameId', None)
#     session_index = request.session.get('samlSessionIndex', None)

#     req = prepare_django_request(request)

#     # Создание экземпляра SAML-аутентификации
#     auth = OneLogin_Saml2_Auth(req, load_saml_config())
#     saml_settings = auth.get_settings()
#     slo_service_url = saml_settings.get_idp_data()['singleLogoutService']['url']

#     # Создаем SAML LogoutRequest с NameID и SessionIndex
#     logout_request = OneLogin_Saml2_Logout_Request(
#         saml_settings,
#         name_id=name_id,
#         session_index=session_index
#     )

#     logout_request_xml = logout_request.get_xml()

#     signed_logout_request = OneLogin_Saml2_Utils.add_sign(
#         logout_request_xml,
#         saml_settings.get_sp_key(),   # Приватный ключ SP
#         saml_settings.get_sp_cert(),  # X.509 сертификат SP
#     ).decode('utf-8')

#     # Проверка, что запрос был успешно подписан
#     if not signed_logout_request:
#         raise Exception("Ошибка: не удалось подписать SAML LogoutRequest.")

#     encoded_logout_request = OneLogin_Saml2_Utils.b64encode(signed_logout_request.encode('utf-8'))

#     # Формируем параметры для URL
#     params = {
#         'SAMLRequest': encoded_logout_request,
#         'RelayState': 'http://service-dtk.croc.ru'
#     }

#     # Формируем полный URL для редиректа с подписанным запросом
#     redirect_url = f"{slo_service_url}?{urlencode(params)}"

#     return HttpResponseRedirect(redirect_url)

def saml_metadata(request):
    saml_settings = load_saml_config()

    metadata = saml_settings.get_sp_metadata()

    errors = saml_settings.validate_metadata(metadata)

    if len(errors) == 0:
        return HttpResponse(content=metadata, content_type='text/xml')
    else:
        return HttpResponse(content='Метаданные содержат ошибки: ' + ', '.join(errors), status=500)
