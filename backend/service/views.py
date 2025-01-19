from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
import re
from django.db.models import Count
from datetime import datetime, timedelta
from .models import Service, FieldConfiguration, Submission
from .serializers import ServiceSerializer, FieldConfigurationSerializer


class ServiceListView(generics.ListAPIView):
    """
    API to list all services with their field configurations.
    """
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.prefetch_related('field_configurations').all()
    serializer_class = ServiceSerializer


class FieldConfigurationView(generics.ListAPIView):
    """
    API to list all field configurations for a specific service.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FieldConfigurationSerializer

    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        queryset = FieldConfiguration.objects.filter(service__service_id=service_id)
    
        return queryset


class SubmissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, service_id):
        """
        Retrieve submissions for a specific service with filtering, sorting, and pagination.
        """
        try:
            service = Service.objects.get(service_id=service_id)
        except Service.DoesNotExist:
            return Response({"error": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

        requested_language = request.headers.get('Accept-Language', 'en')

        filter_field = request.query_params.get('filter_field') 
        filter_value = request.query_params.get('filter_value') 
        sort_by = request.query_params.get('sort_by', 'id')  
        sort_order = request.query_params.get('sort_order', 'asc')  

        page = int(request.query_params.get('page', 1)) 
        page_size = int(request.query_params.get('page_size', 10))  

        submissions = Submission.objects.filter(service=service)
        if filter_field and filter_value:
            filter_criteria = {f"data__{filter_field}__value__icontains": filter_value}
            submissions = submissions.filter(**filter_criteria)

        if sort_order == "desc":
            sort_by = f"-{sort_by}"
        submissions = submissions.order_by(sort_by)

        paginator = Paginator(submissions, page_size)
        try:
            paginated_submissions = paginator.page(page)
        except Exception:
            return Response({"error": "Invalid page number."}, status=status.HTTP_400_BAD_REQUEST)

        response_data = []
        for submission in paginated_submissions:
            formatted_submission = {
                "id": submission.id,
                "data": {
                    field: {
                        "label": value.get("label", ""),
                        "value": value.get("value", ""),
                    }
                    if isinstance(value, dict) else value
                    for field, value in submission.data.items()
                },
                "submitted_at": submission.submitted_at,
            }
            response_data.append(formatted_submission)

        return Response({
            "total": paginator.count,
            "pages": paginator.num_pages,
            "current_page": paginated_submissions.number,
            "results": response_data,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        service_id = kwargs.get('service_id')
        try:
            service = Service.objects.get(service_id=service_id)
        except Service.DoesNotExist:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

        requested_language = request.headers.get('Accept-Language', 'en')

        data = request.data
        errors = {}
        transformed_data = {}
        for field in service.field_configurations.all():
            field_name = field.name
            field_value = data.get(field_name)
            if not field_value:
                validation_error_message = (
                    field.validation_error_message.get(requested_language, field.validation_error_message.get("en"))
                )
                errors[field_name] = validation_error_message
            elif field.validation_regex and not re.match(field.validation_regex, str(field_value)) and len(field_value) <= field.max_length:
                validation_error_message = (
                    field.validation_error_message.get(requested_language, field.validation_error_message.get("en"))
                )
                errors[field_name] = validation_error_message
            else:
                field_label = field.label.get(requested_language, field.label.get("en"))
                transformed_data[field_name] = {
                    "label": field_label,
                    "value": field_value,
                }

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        submission = Submission.objects.create(
            service=service,
            data=transformed_data,  
        )

        return Response(
            {"message": "Submission successful", "submission_id": submission.id},
            status=status.HTTP_200_OK,
        )


class SubmissionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, submission_id):
        """
        Retrieve the details of a specific submission by ID.
        """
        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return Response({"error": "Submission not found."}, status=status.HTTP_404_NOT_FOUND)

        requested_language = request.headers.get('Accept-Language', 'en')

        submission_data = {
            "id": submission.id,
            "service": submission.service.name,
            "data": {
                field: {
                    "label": value.get("label", ""),
                    "value": value.get("value", ""),
                }
                if isinstance(value, dict) else value
                for field, value in submission.data.items()
            },
            "submitted_at": submission.submitted_at,
        }

        return Response(submission_data, status=status.HTTP_200_OK)
    
class DashboardReportingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, filter_type='day'):
        """
        Retrieve reporting data for the dashboard.
        """
        now = datetime.now()

        if filter_type == 'day':
            start_date = now - timedelta(days=1)  
        elif filter_type == 'week':
            start_date = now - timedelta(days=7)  
        elif filter_type == 'month':
            start_date = now - timedelta(days=30)  
        else:
            return Response(
                {"error": "Invalid filter type. Use 'day', 'week', or 'month'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_submissions_per_service = Submission.objects.values('service__name').annotate(total_submissions=Count('id'))

        submission_trends = (
            Submission.objects.filter(submitted_at__gte=start_date)
            .values('submitted_at__date')
            .annotate(total_submissions=Count('id'))
            .order_by('submitted_at__date')
        )

        most_frequent_services = (
            Submission.objects.filter(submitted_at__gte=start_date)
            .values('service__name')
            .annotate(total_submissions=Count('id'))
            .order_by('-total_submissions')[:5]
        )

        response_data = {
            "total_submissions_per_service": [
                {
                    "service_name": entry['service__name'],
                    "total_submissions": entry['total_submissions']
                }
                for entry in total_submissions_per_service
            ],
            "submission_trends": [
                {
                    "date": entry['submitted_at__date'],
                    "total_submissions": entry['total_submissions']
                }
                for entry in submission_trends
            ],
            "most_frequent_services": [
                {
                    "service_name": entry['service__name'],
                    "total_submissions": entry['total_submissions']
                }
                for entry in most_frequent_services
            ]
        }

        return Response(response_data, status=status.HTTP_200_OK)