from django.contrib import admin

from .models import Property


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('pid', 'neighborhood', 'lotarea', 'yrsold', 'mosold', 'salecondition', 'saletype', 'saleprice')
    list_filter = ('neighborhood', 'salecondition', 'saletype', 'yrsold')


admin.site.register(Property, PropertyAdmin)
