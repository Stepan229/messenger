from django.contrib import admin

from .models import Chat, Message, UserChat


class ChatAdmin(admin.ModelAdmin):
    # Какие поля отображаются в списке записей
    list_display = ('title', 'time_create')

    # Фильтры справа
    list_filter = ('title', 'time_create')

    # Поиск по полям
    search_fields = ('title',)
    #
    # # Автозаполнение slug на основе title
    # prepopulated_fields = {'slug': ('title',)}

    # Группировка полей при редактировании
    # fieldsets = (
    #     ('Основное', {
    #         'fields': ('title', 'slug', 'author', 'content'),
    #     }),
    #     ('Дополнительно', {
    #         'fields': ('is_published', 'tags'),
    #         'classes': ('collapse',),  # Сворачиваемый блок
    #     }),
    # )

class MessageAdmin(admin.ModelAdmin):
    # Какие поля отображаются в списке записей
    list_display = ('creator_id', 'chat_id', 'text',
                    'time_create', 'time_update', 'is_read')

    # Фильтры справа
    list_filter = ('creator_id', 'time_create', 'is_read')

    # Поиск по полям
    search_fields = ('title',)

class UserChatAdmin(admin.ModelAdmin):
    # Какие поля отображаются в списке записей
    list_display = ('chat_id', 'user_id', 'is_read', 'is_creator')

    # Фильтры справа
    list_filter = ('chat_id', 'chat_id',)

    # Поиск по полям
    search_fields = ('chat_id', 'user_id',)

# Регистрируем модель с кастомным админ-классом
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserChat, UserChatAdmin)
# Register your models here.
