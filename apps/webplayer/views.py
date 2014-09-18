from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.conf import settings

from .models import WebPlayer
from ..clickjogosauth.views import CLICKJOGOS_AUTH_URL


def webplayer(request):
    version = request.GET.get("version", "")
    if version:
        request.session["webplayer_version"] = version

    #if uid is in querystring, authenticate the user
    clickjogos_id = request.GET.get("uid")
    if clickjogos_id:
        user = authenticate(clickjogos_id=clickjogos_id)
        #if authentication failed (e.g. the user was not authenticated with clickjogos), show
        #auth page
        if not user:
            render(request, "webplayer/not_logged_in.html", dict(
                webplayer=WebPlayer.objects.get_active(),
                google_analytics_property=settings.GOOGLE_ANALYTICS_PROPERTY,
                clickjogos_auth_url=CLICKJOGOS_AUTH_URL,
            ))
        login(request, user)

    #if not authenticated, show authentication page
    if not request.user.is_authenticated():
        return render(request, "webplayer/not_logged_in.html", dict(
            google_analytics_property=settings.GOOGLE_ANALYTICS_PROPERTY,
            clickjogos_auth_url=CLICKJOGOS_AUTH_URL,
        ))

    #try to find the named webplayer
    webplayer = None
    version = request.session.get("webplayer_version", "")
    if version:
        try:
            webplayer = WebPlayer.objects.get(name=version)
        except WebPlayer.DoesNotExist:
            pass

    #otherwise get the active webplayer
    if not webplayer:
        webplayer = WebPlayer.objects.get_active()

    return render(request, "webplayer/webplayer.html", dict(
        version=webplayer.name,
        webplayer=webplayer,
        google_analytics_property=settings.GOOGLE_ANALYTICS_PROPERTY,
    ))


def cjapitest(request):
    return render(request, "webplayer/cjapitest.html", dict(

    ))