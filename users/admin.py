from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, User, Privilege, Logging, UserPrivilege,UserType

class CustomUserAdmin(UserAdmin):

    model = User
    list_display = ('id', 'email','username' ,'is_staff', 'is_active',
                    'first_name', 'last_name', 'branch','is_delete_requested')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password', 'staff_id',
         'first_name', 'middle_name', 'last_name', 'user_type', 'branch','role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_branch_user', 'is_head_office_user'
                                    )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'staff_id', 'first_name', 'middle_name', 'last_name','branch', 'user_type')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)


@admin.register(Privilege)
class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ("slug","privilege", "created_at",)
    prepopulated_fields = {"slug":("privilege",)}


@admin.register(UserPrivilege)
class UserPrivilegeAdmin(admin.ModelAdmin):
    list_display = ('user', "privilege","is_delete_requested",)


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', "title")
    prepopulated_fields = {"slug":("title",)}

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id","user")
    





