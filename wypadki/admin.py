from django.contrib import admin
from .models import Lokomotywa, Zdarzenie, Material

@admin.register(Lokomotywa)
class LokomotywaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'zrodlo_zdjecia')
    search_fields = ('nazwa', 'opis')

class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1

@admin.register(Zdarzenie)
class ZdarzenieAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'data', 'miejscowosc', 'liczba_ofiar')
    list_filter = ('data', 'lokomotywa')
    search_fields = ('tytul', 'miejscowosc', 'linia_kolejowa')
    inlines = [MaterialInline]

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'typ', 'zdarzenie')
    list_filter = ('typ',)
    search_fields = ('tytul', 'url')
