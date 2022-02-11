from django.contrib import admin

from .models import User, UserOnline, UserRegistration
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserOnline)
admin.site.register(UserRegistration)
