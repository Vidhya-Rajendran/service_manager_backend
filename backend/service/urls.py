
from django.urls import path
from .views import  ServiceListView, FieldConfigurationView, SubmissionView, SubmissionDetailView, DashboardReportingView


urlpatterns = [    
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:service_id>/fields/', FieldConfigurationView.as_view(), name='field-configuration'),
    path('services/<int:service_id>/submit/', SubmissionView.as_view(), name='submit-data'),
    path('services/<int:service_id>/submissions/', SubmissionView.as_view(), name='submission-list'),
    path('submissions/<int:submission_id>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('dashboard/<str:filter_type>/', DashboardReportingView.as_view(), name='dashboard-reporting')
]
