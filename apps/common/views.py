from .serializers import SponsorSerializer, StudentSerializer, SponsorDetailSerializer, StudentDetailSerializer, \
    StudentSponsorCreateSerializer, StudentSponsorUpdateSerializer, StudentCreateSerializer, StudentUpdateSerializer
from rest_framework import generics
from .models import Sponsor, Student, StudentSponsor
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class SponsorAPIView(generics.CreateAPIView):
    serializer_class = SponsorSerializer


class SponsorFilterSearchAPIView(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['sponsor_perform_type', 'created_at']
    search_fields = ['full_name', 'phone', 'amount', 'created_at']


class StudentFilterSearchAPIView(generics.ListAPIView):
    queryset = Student.objects.all().select_related('university')
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['contract_amount', 'student_type', 'university']
    search_fields = ['university', 'student_type']


class SponsorDetailAPIView(generics.RetrieveAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorDetailSerializer
    lookup_field = 'pk'


class StudentDetailAPIView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer
    lookup_field = 'pk'


class StudentSponsorCreateAPIView(generics.CreateAPIView):
    serializer_class = StudentSponsorCreateSerializer


class StudentSponsorUpdateAPIView(generics.UpdateAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorUpdateSerializer
    lookup_field = 'pk'


class StudentDeleteAPIView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer
    lookup_field = 'pk'


class StudentCreateAPIView(generics.CreateAPIView):
    serializer_class = StudentCreateSerializer


class StudentUpdateAPIView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    lookup_field = 'pk'


class SponsorUpdateAPIView(generics.UpdateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    lookup_field = 'pk'
