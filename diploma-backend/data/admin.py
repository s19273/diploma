from django.contrib import admin

from data.models.image import ImageModel
from data.models.log_item import LogItem

admin.site.register(LogItem)
admin.site.register(ImageModel)
