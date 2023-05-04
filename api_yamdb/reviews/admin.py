from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
