from django.contrib import admin
from .models import ValetKey

# class ValetKeyAdmin(admin.ModelAdmin):
#     list_display = ('key', 'user', 'expires_at', 'is_active', 'can_upload', 'can_edit', 'can_delete')
#     list_filter = ('is_active', 'can_upload', 'can_edit', 'can_delete')
#     search_fields = ('key', 'user__username')

# admin.site.register(ValetKey, ValetKeyAdmin)
