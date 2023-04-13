from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
