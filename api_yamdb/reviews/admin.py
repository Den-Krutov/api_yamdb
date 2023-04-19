from django.contrib import admin

from .models import User, Review, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


admin.site.register(Review)
admin.site.register(Comment)
