from django.contrib import admin
from accounts.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group




class UserAuthAdmin(UserAdmin):
    search_fields = ('username',)
admin.site.register(UserAuth,UserAuthAdmin)
admin.site.unregister(Group)
admin.site.register(Wallet)