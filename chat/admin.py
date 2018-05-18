from django.contrib import admin

from .models import User, Response, Input

admin.site.register(User)
admin.site.register(Input)
admin.site.register(Response)