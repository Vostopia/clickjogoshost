from django.contrib import admin

from .models import ActiveWebPlayer, WebPlayer


class ActiveWebPlayerAdmin(admin.ModelAdmin):
    pass


class WebPlayerAdmin(admin.ModelAdmin):
    pass


admin.site.register(ActiveWebPlayer, ActiveWebPlayerAdmin)
admin.site.register(WebPlayer, WebPlayerAdmin)
