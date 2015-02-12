from django.contrib import admin
from cartoview2.core.models import *


class AppInstanceAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_installed'

admin.site.register(App)
admin.site.register(HomePage)

admin.site.register(AppInstance,AppInstanceAdmin)
admin.site.register(KeyValueGroup)
admin.site.register(KeyValue)
admin.site.register(AppTag)