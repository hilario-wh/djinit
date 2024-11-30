from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UserAdmin_


User = get_user_model()


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin_):
    pass
