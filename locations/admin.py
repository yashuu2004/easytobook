from django.contrib import admin
from .models import State, City


class CityInline(admin.TabularInline):
    model = City
    extra = 1


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    inlines = [CityInline]
    list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state',)
    search_fields = ('name', 'state__name')
