from django.contrib import admin
from .models import Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "status",
        "location_name",
        "date",
        "time",
        "max_participants",
        "current_participants",
        "is_active",
        "created_at",
    ]
    list_filter = ["status", "category", "is_active", "date"]
    search_fields = ["title", "description", "location_name"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at"]
