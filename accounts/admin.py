from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Skill, Profile, Booking

admin.site.register(Skill)
admin.site.register(Profile)
admin.site.register(Booking)
