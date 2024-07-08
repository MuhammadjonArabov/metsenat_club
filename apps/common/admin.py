from django.contrib import admin
from .models import University, Student, Sponsor, StudentSponsor


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'contract_amount']
    search_fields = ['full_name', 'phone', 'university']


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'amount',]
    search_fields = ['full_name', 'phone', 'organization']


@admin.register(StudentSponsor)
class StudentSponsorAdmin(admin.ModelAdmin):
    list_display = ['amount', 'student', 'sponsor']
    search_fields = ['student', 'sponsor']
