from django.contrib import admin
from .models import Categoria, Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_name', 'phone', 'email', 'creation_date', 'categoria', 'show')
    list_display_links = ('id', 'name', 'last_name')
    list_filter = ('categoria',)
    list_per_page = 10
    search_fields = ('name', 'last_name', 'phone')
    list_editable = ('phone', 'show')


admin.site.register(Categoria)
admin.site.register(Contact, ContactAdmin)
