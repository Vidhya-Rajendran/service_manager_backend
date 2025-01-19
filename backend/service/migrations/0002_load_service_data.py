from django.db import migrations
import json
import os

def load_services_data(apps, schema_editor):
    Service = apps.get_model('service', 'Service')
    FieldConfiguration = apps.get_model('service', 'FieldConfiguration')

    current_directory = os.path.dirname(os.path.abspath(__file__))
    services_file_path = os.path.join(current_directory, '..', 'services.json')
    
    with open(services_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for service_data in data['services']:
        service = Service.objects.create(
            name=service_data['name'],
            service_id=service_data['id']
        )

        for field_data in service_data['required_fields']:
            FieldConfiguration.objects.create(
                service=service,
                name=field_data['name'],
                label=field_data['label'],
                placeholder=field_data['placeholder'],
                field_type=field_data['type'],
                validation_regex=field_data['validation'],
                validation_error_message=field_data['validation_error_message'],
                max_length=field_data.get('max_length', None),
                options=field_data.get('options', None)
            )

def unload_services(apps, schema_editor):
    Service = apps.get_model('service', 'Service')
    FieldConfiguration = apps.get_model('service', 'FieldConfiguration')
    Service.objects.all().delete()
    FieldConfiguration.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(load_services_data, reverse_code=unload_services),
    ]
