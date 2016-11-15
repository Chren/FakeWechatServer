from django.contrib import admin
from .models import IMUser, FriendShip

class IMUserAdmin(admin.ModelAdmin):
	filter_horizontal = ('friends',)
	list_display = ("userid", "name", "phone", "image_tag")
    
admin.site.register(IMUser, IMUserAdmin)
admin.site.register(FriendShip)
