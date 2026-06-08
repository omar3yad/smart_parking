from rest_framework import serializers
from parking.models import VehicleLog, ParkingSlot, Reservation
from django.contrib.auth.models import User
import math
from django.utils import timezone


class AdminVehicleLogSerializer(serializers.ModelSerializer):
    duration_hours = serializers.SerializerMethodField()
    total_fee = serializers.SerializerMethodField()
    billed_hours = serializers.SerializerMethodField()
    entry_image_url = serializers.SerializerMethodField()
    exit_image_url = serializers.SerializerMethodField()
    slot_number = serializers.CharField(source='slot.slot_number', read_only=True)

    class Meta:
        model = VehicleLog
        fields = [
            'id',
            'license_plate',
            'slot_number',
            'entry_time',
            'exit_time',
            'duration_hours',
            'total_fee',
            'billed_hours',
            'is_paid',
            'entry_image_url',
            'exit_image_url',
        ]

    # def get_duration_hours(self, obj):
    #     if obj.exit_time:
    #         delta = obj.exit_time - obj.entry_time
    #         return round(delta.total_seconds() / 3600, 2)
    #     return None  # Still inside

    def get_duration_hours(self, obj):
        if not obj.exit_time or not obj.entry_time:
           return None
        
        entry = obj.entry_time
        exit_ = obj.exit_time

        if timezone.is_aware(entry) and timezone.is_naive(exit_):
            exit_ = timezone.make_aware(exit_)
        elif timezone.is_naive(entry) and timezone.is_aware(exit_):
            entry = timezone.make_aware(entry)

        delta = exit_ - entry
        total_seconds = delta.total_seconds()

        if total_seconds <= 0:
            return None
        
        return round(total_seconds / 3600, 2)
    
    def get_billed_hours(self, obj):
        if not obj.exit_time:
           return None

        delta = obj.exit_time - obj.entry_time

        hours = math.ceil(delta.total_seconds() / 3600)

        return max(hours, 0)
    
    def get_total_fee(self, obj):
        billed_hours = self.get_billed_hours(obj)
        if billed_hours is None:
            return 0
        return billed_hours * 30  # Assuming $30 per hour

    def get_entry_image_url(self, obj):
        request = self.context.get('request')
        if obj.entry_image and request:
            return request.build_absolute_uri(obj.entry_image.url)
        return None

    def get_exit_image_url(self, obj):
        request = self.context.get('request')
        if obj.exit_image and request:
            return request.build_absolute_uri(obj.exit_image.url)
        return None


class AdminSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = ['id', 'slot_number', 'status', 'slot_type', 'latitude', 'longitude']


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']


class CreateAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        user.is_staff = True      # Can access Django admin panel
        user.is_superuser = True  # Full permissions
        user.save()
        return user


class AdminReservationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    slot_number = serializers.CharField(source='slot.slot_number', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'username', 'slot_number',
            'reservation_code', 'start_time', 'end_time',
            'created_at', 'is_active'
        ]
