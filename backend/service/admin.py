from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from .models import Service, FieldConfiguration, Submission

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "service_id",
        "name",
    )
    search_fields = (
        "service_id",
        "name",
    )

@admin.register(FieldConfiguration)
class FieldConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "name",
        "placeholder",
        "field_type",
    )
    search_fields = (
        "service__name",
        "name",
    )

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "data",
        "submitted_at",
    )
    search_fields = (
        "service__name",        
    )
    list_filter = (
        ("submitted_at", DateRangeFilter),
    )