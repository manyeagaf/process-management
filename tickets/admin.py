from django.contrib import admin
from .models import Request, Comment, Attachment, RequestType, Status

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id','request_id','title', 'created_at', 'request_type', 'initiator',
                    'assignee', "status", "is_assigned",'is_archieved')
    list_editable = ("status", "is_assigned","assignee",'is_archieved')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'owner', 'created_at')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'request',)

@admin.register(RequestType)
class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ("request_type", "created_at")
    prepopulated_fields = {"slug": ("request_type",)}

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id","status", "slug",)
    prepopulated_fields = {'slug': ('status',)}
