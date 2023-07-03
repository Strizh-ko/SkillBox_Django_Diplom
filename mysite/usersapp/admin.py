from django.contrib import admin
from .models import ProfileUser, AvatarUser


class ProfileUserInline(admin.StackedInline):
    model = AvatarUser


@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    inlines = [ProfileUserInline]
    list_display = ("pk", "fullName", "email", "phone", "user")
    list_display_links = ("pk", "fullName")
    ordering = ("pk",)


@admin.register(AvatarUser)
class AvatarUserAdmin(admin.ModelAdmin):
    list_display = ("pk", "avatar", "profile")
    ordering = ("pk",)
