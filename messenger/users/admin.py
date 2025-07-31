from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    # Какие поля отображаются в списке записей
    list_display = ('id', 'username', 'email', 'is_staff')

    # Фильтры справа
    list_filter = ('id', 'username', 'email')

    # Поиск по полям
    search_fields = ('title',)


# Register your models here.
admin.site.register(User, UserAdmin)