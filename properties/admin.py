from django.contrib import admin

from .models import Property, Listing


class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'pid', 'lotarea', 'overallqual', 'overallcond', 'centralair', 'fullbath', 'bedroomabvgr', 'garagecars',
        'saleprice', 'data_source', 'dataset'
    )
    list_filter = ('data_source', 'dataset')


class ListingAdmin(admin.ModelAdmin):
    list_display = ('property', 'description', 'created_at')


admin.site.register(Property, PropertyAdmin)
admin.site.register(Listing, ListingAdmin)
