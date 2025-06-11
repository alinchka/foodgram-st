from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import User, Subscription

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')

admin.site.register(Subscription) 