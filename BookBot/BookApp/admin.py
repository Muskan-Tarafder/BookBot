from django.contrib import admin
from BookApp.models import *
# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display = ['role','short_content','source','timestamp','session_key']
    list_filter = ['role','source','timestamp']
    search_fields = ['content','session_key']
    readonly_fields = ['timestamp']

    def short_content(self,obj):
        return obj.content[:50]
    short_content.short_description = 'Content'

admin.site.register(Message)
admin.site.register(Suggestions)