from django.contrib import admin

from .models import Property


class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'pid', 'lotarea', 'overallqual', 'overallcond', 'centralair', 'fullbath', 'bedroomabvgr', 'garagecars',
        'saleprice', 'data_source', 'dataset'
    )
    list_filter = ('data_source', 'dataset')


admin.site.register(Property, PropertyAdmin)
