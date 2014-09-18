import random
from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()


@register.filter()
def cdn(original_url):
    """
    Tries to find a CDN server for the original_url. CDN servers
    are defined in settings.CDN_SERVERS as a dict, where the key is
    the url prefix the cdn hosts and the value is a list of urls that
    are chosen randomly
    """
    if settings.CDN_SERVERS:
        for prefix, cdn_servers in settings.CDN_SERVERS.items():
            if original_url.startswith(prefix):
                server = random.choice(cdn_servers)
                return original_url.replace(prefix, server)

    return original_url


@register.filter()
def cdn_static(path):
    original_url = staticfiles_storage.url(path)
    return cdn(original_url)

