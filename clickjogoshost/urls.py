from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', 'apps.webplayer.views.webplayer', name="index"),
    url(r'^cjapitest$', 'apps.webplayer.views.cjapitest', name="cjapitest"),

    # Authentication callbacks from click jogos
    url(r'^auth/callback/?$', 'apps.clickjogosauth.views.success'),
    url(r'^auth/failure/?$', 'apps.clickjogosauth.views.failure'),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #s3direct
    url(r'^s3direct/', include('apps.s3direct.urls')),
)

#serve static files
urlpatterns += staticfiles_urlpatterns()

#serve uploaded files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)