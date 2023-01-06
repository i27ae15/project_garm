from django.contrib import admin

from .models import CustomUser, Specie, Race, FriendRequest

admin.site.register(CustomUser)
admin.site.register(Specie)
admin.site.register(Race)
admin.site.register(FriendRequest)
