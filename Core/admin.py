from django.contrib import admin
from .models import Reply, Reports

# admin.model admin for showing data in the admin panel
class ReportsAdmin(admin.ModelAdmin):
    list_display = ['name','email','image_tag']
    search_fields = ['name','email']
    list_filter = ['time']

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['reporter_name','reporter_email']
    search_fields = ['reporter_name','reporter_email']
    list_filter = ['reply_time']


# site register for considering the site as belongs to the admin
admin.site.register(Reports,ReportsAdmin)
admin.site.register(Reply,ReplyAdmin)
