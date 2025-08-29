from django.contrib import admin

from django.contrib.admin.models import LogEntry

READ_ONLY_FIELDS = (
    "deleted_at",
    "restored_at",
    "transaction_id",
)


class SoftDeleteAdmin(admin.ModelAdmin):
    exclude = ["deleted_at", "restored_at", "transaction_id"]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "action_time",
        "user",
        "content_type",
        "object_id",
        "object_repr",
        "action_flag",
        "change_message",
    )

    list_display = (
        "id",
        "action_time",
        "user",
        "content_type",
        "object_repr",
        "action_flag",
        "change_message",
    )

    list_filter = ("action_time", "user", "content_type")

    search_fields = ("object_repr", "change_message")

    list_per_page = 50

    ordering = ["action_time"]
