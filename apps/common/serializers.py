from decimal import Decimal

from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Sponsor, Student, StudentSponsor
from django.db.models import Sum


class SponsorSerializer(serializers.ModelSerializer):
    def validate(self, value):
        if value <= 0 or None:
            raise serializers.ValidationError('Amount must be greater than 0.')
        return round(Decimal(value), 6)

        sponsor_type = self.initial_data.get('sponsor_type')
        if sponsor_type == str(Sponsor.NATURAL_PERSON) and value:
            raise serializers.ValidationError('Organization field must be empty for natural persons.')
        return value

    class Meta:
        model = Sponsor
        fields = ['id', 'full_name', 'phone', 'amount', 'organization', 'sponsor_perform_type', 'sponsor_type']


class StudentSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source='university.title')
    total_student_amount = serializers.SerializerMethodField()

    def validate(self, value):
        if value <= 0 or None:
            raise serializers.ValidationError('Contract_amount must be greater than 0.')
        return round(Decimal(value), 6)

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'phone', 'contract_amount', 'student_type', 'university', 'total_student_amount']

    def get_total_student_amount(self, obj):
        total_amount = StudentSponsor.objects.filter(student=obj).aggregate(total_amount=Sum('amount'))[
                           'total_amount'] or Decimal(0)
        return total_amount


class SponsorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['amount', 'full_name', 'phone']


class StudentSponsorShortSerializer(serializers.ModelSerializer):
    sponsor = serializers.CharField(source='sponsor.full_name')

    class Meta:
        model = StudentSponsor
        fields = ['amount', 'sponsor']


class StudentSponsorSerializer(serializers.ModelSerializer):
    sponsor = serializers.CharField(source='sponsor.full_name')
    student = serializers.CharField(source='student.full_name')

    class Meta:
        model = StudentSponsor
        fields = ['amount', 'student', 'sponsor']


class StudentDetailSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source='university.title')
    student_sponsors = StudentSponsorShortSerializer(many=True, read_only=True)
    total_sponsor_amount = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'phone', 'contract_amount', 'student_type', 'university', 'student_sponsors',
                  'total_sponsor_amount']

    def get_total_sponsor_amount(self, obj):
        total_amount = StudentSponsor.objects.filter(student=obj).aggregate(total_amount=Sum('amount'))[
                           'total_amount'] or Decimal(0)
        return total_amount


class StudentSponsorCreateSerializer(serializers.ModelSerializer):

    def validate(self, data):
        amount = data.get('amount')
        sponsor = data.get('sponsor')
        student = data.get('student')

        total_transfer_amount = StudentSponsor.objects.filter(sponsor=sponsor).aggregate(total_amount=Sum('amount'))[
                                    'total_amount'] or Decimal(0)
        available_amount = sponsor.amount - total_transfer_amount

        if amount > available_amount:
            raise ValidationError("The amount entered must not exceed the sponsor's available amount")
        existing_amount = StudentSponsor.objects.filter(student=student).aggregate(total_amount=Sum('amount'))[
                              'total_amount'] or Decimal(0)
        if amount + existing_amount > student.contract_amount:
            raise ValidationError(
                """The sum of the entered amount and the available amounts 
                should not be greater than the student's contract amount.
                """)
        return data

    def create(self, validate_data):
        sponsor = validate_data['sponsor']
        amount = validate_data['amount']
        sponsor.amount -= amount
        sponsor.save()
        return super().create(validate_data)

    class Meta:
        model = StudentSponsor
        fields = ['amount', 'student', 'sponsor']


class StudentSponsorUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data):
        amount = data.get('amount')
        sponsor = data.get('sponsor')
        student = data.get('student')

        if sponsor and sponsor != self.instance.sponsor:
            total_transfer_amount = \
                StudentSponsor.objects.filter(sponsor=sponsor).aggregate(total_amount=Sum('amount'))[
                    'total_amount'] or Decimal(0)
            available_amount = sponsor.amount - total_transfer_amount
            if amount > available_amount:
                raise ValidationError(
                    "Don't transfer the amount entered into the sponsor's available amount")

        existing_amount = StudentSponsor.objects.filter(student=student).exclude(pk=self.instance.pk).aggregate(
            total_amount=Sum('amount'))['total_amount'] or Decimal(0)
        if amount + existing_amount > student.contract_amount:
            raise ValidationError(
                "The amount entered and the amount available cannot be greater than the student's contract amount")

        return data

    def update(self, instance, validated_data):
        sponsor = validated_data.get('sponsor', instance.sponsor)
        amount = validated_data.get('amount', instance.amount)
        student = validated_data.get('student', instance.student)

        instance.sponsor.amount += instance.amount
        instance.sponsor.save()

        total_transfer_amount = StudentSponsor.objects.filter(sponsor=sponsor).exclude(pk=instance.pk).aggregate(
            total_amount=Sum('amount'))['total_amount'] or Decimal(0)

        available_amount = sponsor.amount - total_transfer_amount
        if amount > available_amount:
            raise ValidationError("Don't transfer the amount entered into the sponsor's available amount")
        existing_amount = StudentSponsor.objects.filter(student=student).exclude(pk=instance.pk).aggregate(
            total_amount=Sum('amount'))['total_amount'] or Decimal(0)
        if amount + existing_amount > sponsor.contract_amount:
            raise ValidationError(
                """The sum of the entered amount and the available amounts 
                should not be greater than the student's contract amount.
                """)
        sponsor.amount -= amount
        sponsor.save()

        instance.sponsor = sponsor
        instance.amount = amount
        instance.student = student
        instance.save()

        return instance

    class Meta:
        model = StudentSponsor
        fields = ['amount', 'student', 'sponsor']


class StudentCreateSerializer(serializers.ModelSerializer):
    def validate(self, value):
        if value <= 0 or None:
            raise serializers.ValidationError('Contract amount must be greater than 0.')
        return round(Decimal(value), 6)

    class Meta:
        model = Student
        fields = ['full_name', 'phone', 'contract_amount', 'university', 'student_type']


class StudentUpdateSerializer(serializers.ModelSerializer):
    def validate(self, value):
        if value <= 0 or None:
            raise serializers.ValidationError('Contract amount must be greater than 0.')
        return round(Decimal(value), 6)

    class Meta:
        model = Student
        fields = ['full_name', 'phone', 'contract_amount', 'university']
