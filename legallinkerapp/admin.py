from django.contrib import admin

# Register your models here.
from .models import Advocate, Location

admin.site.register(Advocate)
admin.site.register(Location)