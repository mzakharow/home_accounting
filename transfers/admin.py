from django.contrib import admin

from transfers.models import Transfer, CategoryTransfer

# class MovieAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'url': ('title', )}


admin.site.register(Transfer)
admin.site.register(CategoryTransfer)
