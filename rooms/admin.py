from django.contrib import admin
from .models import Room, City, Ward, RoomImage

class RoomImageInline(admin.TabularInline):

    model = RoomImage

    extra = 3

@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'code',
    )

    search_fields = (
        'name',
        'code',
    )


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'city',
        'code',
        'ward_type',
    )

    list_filter = (
        'city',
        'ward_type',
    )

    search_fields = (
        'name',
        'code',
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'city',
        'ward',
        'address',
        'price',
        'area',
        'status',
    )

    list_filter = (
        'city',
        'ward',
        'status',
    )

    search_fields = (
        'name',
        'address',
    )

    inlines = [
        RoomImageInline
    ]

