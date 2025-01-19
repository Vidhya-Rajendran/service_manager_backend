from rest_framework import serializers
from .models import Service, FieldConfiguration, Submission


class FieldConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldConfiguration
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    fields = FieldConfigurationSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'service_id', 'fields']


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'service', 'submission_date', 'data']