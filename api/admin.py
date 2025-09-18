from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Event, Announcement
from .forms import CustomUserCreationForm

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    model = User

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("role", "neighborhood")}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'neighborhood'),
        }),
    )

    list_display = ("username", "email", "role", "is_staff", "is_superuser")
    list_filter = ("role", "is_staff")

admin.site.register(User, UserAdmin)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", )
    search_fields = ("title", "description")
    list_filter = ("date", )




#Announcement
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")   
    search_fields = ("title", "message")     
    ordering = ("-created_at",)


# help-exchange
from django.contrib import admin
from .models import HelpPost, Reply

@admin.register(HelpPost)
class HelpPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'user', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('title', 'description', 'user__username')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('message', 'user__username', 'post__title')
