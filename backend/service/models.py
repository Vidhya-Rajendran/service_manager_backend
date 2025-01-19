from django.db import models
from django.db.models import JSONField


class Service(models.Model):
    """
    Model representing a service, such as 'ABC Bank' or 'XYZ Bank'.
    """
    name = models.CharField(max_length=255, unique=True)
    service_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class FieldConfiguration(models.Model):
    """
    Model representing a field configuration for a specific service.
    """
    FIELD_TYPES = [
        ('number', 'Number'),
        ('text', 'Text'),
        ('option', 'Option (Dropdown)'),
        ('date', 'Date'),
    ]
    
    service = models.ForeignKey(Service, related_name='field_configurations', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    label = models.JSONField()
    placeholder = models.JSONField(blank=True, null=True)  
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    validation_regex = models.CharField(max_length=255, blank=True, null=True)
    validation_error_message = models.JSONField(blank=True, null=True) 
    max_length = models.IntegerField(blank=True, null=True)
    options = models.JSONField(blank=True, null=True) 
    
    def __str__(self):
        return f"{self.name.get('en', 'Field')} ({self.service.name})"


class Submission(models.Model):
    """
    Model representing a service submission
    """
    service = models.ForeignKey(Service, related_name='submissions', on_delete=models.CASCADE)
    data = JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.service.name}"