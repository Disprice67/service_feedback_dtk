from .views import CustomTokenObtainPairView, UploadActivitiesView, UploadCasesView, UserCreateView, ResetUserFeedbackView, ExportActivesToExcelView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path


urlpatterns = [
    path('upload-actives/', UploadActivitiesView.as_view(), name='upload-actives'),
    path('upload-cases/', UploadCasesView.as_view(), name='upload-cases'),
    path('token/create/', CustomTokenObtainPairView.as_view(), name='custom_token-create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('export-actives/', ExportActivesToExcelView.as_view(), name='export_actives'),
    path('reset-user-form/', ResetUserFeedbackView.as_view(), name='reset-user-form'),
    path('create-user/', UserCreateView.as_view(), name='create-user'),
]
