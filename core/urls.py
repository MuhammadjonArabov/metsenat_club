from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from apps.common.views import SponsorAPIView, SponsorFilterSearchAPIView, StudentFilterSearchAPIView, \
    SponsorDetailAPIView, StudentDetailAPIView, StudentSponsorCreateAPIView, StudentSponsorUpdateAPIView, \
    StudentDeleteAPIView, StudentCreateAPIView, StudentUpdateAPIView, SponsorUpdateAPIView
from .schema import swagger_urlpatterns  # Assuming you have swagger_urlpatterns defined in schema.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/sponsor/', SponsorAPIView.as_view(), name='sponsor-create'),
    path('api/sponsor-search-filter/', SponsorFilterSearchAPIView.as_view(), name='sponsor-search-filter'),
    path('api/student-search-filter/', StudentFilterSearchAPIView.as_view(), name='student-search-filter'),
    path('api/sponsor-detail/<int:pk>/', SponsorDetailAPIView.as_view(), name='sponsor-detail'),
    path('api/student-detail/<int:pk>/', StudentDetailAPIView.as_view(), name='student-detail'),
    path('api/student-sponsor-create/', StudentSponsorCreateAPIView.as_view(), name='student-sponsor-create'),
    path('api/student-sponsor-update/<int:pk>/', StudentSponsorUpdateAPIView.as_view(), name='student-sponsor-update'),
    path('api/student-delete/<int:pk>/', StudentDeleteAPIView.as_view(), name='student-delete'),
    path('api/student-update/<int:pk>/', StudentUpdateAPIView.as_view(), name='student-update'),
    path('api/student-create', StudentCreateAPIView.as_view(), name='student-create'),
    path('api/sponsor-update/<int:pk>/', SponsorUpdateAPIView.as_view(), name='sponsor-update'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += swagger_urlpatterns  # Include swagger URLs if defined

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
