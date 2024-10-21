from django.shortcuts import redirect


class RedirectToLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = ['/sso/login/', '/acs/', '/sso/logout/', '/metadata/', '/djadmin/', '/djadmin/login/']
        print(request.path)
        if not request.user.is_authenticated and request.path not in allowed_paths and '/api/' not in request.path:
            return redirect('/sso/login/')
        return self.get_response(request)
