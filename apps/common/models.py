from apps.common.validators import phone_number_validator
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class University(BaseModel):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Student(BaseModel):
    BACHELOR = 1
    MASTER = 2
    STUDENT_TYPE_CHOICES = [
        (BACHELOR, 'bachelor'),
        (MASTER, 'master')
    ]
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14, validators=[phone_number_validator()])
    contract_amount = models.DecimalField(max_digits=60, decimal_places=6, default=0)
    student_type = models.PositiveIntegerField(choices=STUDENT_TYPE_CHOICES, default=BACHELOR)
    university = models.ForeignKey(University, related_name='students', on_delete=models.PROTECT)

    def __str__(self):
        return self.full_name


class Sponsor(BaseModel):
    NATURAL_PERSON = 1
    LEGAL_ENTITY = 2
    SPONSOR_TYPE_CHOICES = [
        (NATURAL_PERSON, 'Jismoniy shaxs'),
        (LEGAL_ENTITY, 'Yuridik shaxs')
    ]
    NEW = 1
    PENDING = 2
    APPROVED = 3
    CANCELLED = 4
    SPONSOR_PERFORM_CHOICES = [
        (NEW, 'Yangi'),
        (PENDING, 'Kutulmoqda'),
        (APPROVED, 'Tasdiqlangan'),
        (CANCELLED, 'Bekor qilindi'),
    ]
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14, validators=[phone_number_validator()])
    amount = models.DecimalField(max_digits=60, decimal_places=6, default=0)
    organization = models.CharField(max_length=250, null=True, blank=True)
    sponsor_perform_type = models.PositiveIntegerField(choices=SPONSOR_PERFORM_CHOICES, default=NEW)
    sponsor_type = models.PositiveIntegerField(choices=SPONSOR_TYPE_CHOICES, default=NATURAL_PERSON)

    def __str__(self):
        return self.full_name


class StudentSponsor(BaseModel):
    amount = models.DecimalField(max_digits=60, decimal_places=6, default=0)
    student = models.ForeignKey(Student, related_name='student_sponsors', on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, related_name='student_sponsors', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"
