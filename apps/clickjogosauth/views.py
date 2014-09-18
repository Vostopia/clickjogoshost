from django.contrib.auth import authenticate, login
from django.http import HttpResponseNotAllowed
from django.conf import settings
from django.shortcuts import render

CLICKJOGOS_AUTH_URL = "%s/%s/" % (settings.CLICKJOGOS_URL, settings.CLICKJOGOS_KEY)


def success(request):
    clickjogos_id = request.GET["uid"]
    user = authenticate(clickjogos_id=clickjogos_id)
    if not user:
        return HttpResponseNotAllowed("Not authenticated with clickjogos")
    login(request, user)
    return render(request, "clickjogosauth/login_completed.html")


def failure(request):
    return HttpResponseNotAllowed("Must authenticate with clickjogos")

