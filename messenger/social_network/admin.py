from django.contrib import admin
from messanger.models import *

@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Message, MessagesAdmin)
# admin.site.register(UserChat, MessagesAdmin)
# admin.site.register(Chat, MessagesAdmin)
