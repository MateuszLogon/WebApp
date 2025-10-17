from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Displays Item objects in Django admin with key fields.
    """
    list_display = ('id', 'user', 'name', 'quantity', 'created_at')
    list_filter = ('user',)
    search_fields = ('name', 'user__username')
