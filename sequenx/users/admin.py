from django.contrib import admin
from .models import UserProfile
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture']

admin.site.register(UserProfile, UserProfileAdmin)
