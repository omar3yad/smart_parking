# administration/serializers.py
from rest_framework import serializers
from parking.models import VehicleLog, ParkingSlot, Reservation
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Shift


class AdminVehicleLogSerializer(serializers.ModelSerializer):
    duration_hours = serializers.SerializerMethodField()
    entry_image_url = serializers.SerializerMethodField()
    exit_image_url = serializers.SerializerMethodField()
    slot_number = serializers.CharField(source='slot.slot_number', read_only=True, default=None)
    collected_by_username = serializers.CharField(source='collected_by.username', read_only=True, default=None)
    entry_shift_id = serializers.IntegerField(source='entry_shift.id', read_only=True, default=None)
    exit_shift_id = serializers.IntegerField(source='exit_shift.id', read_only=True, default=None)

    class Meta:
        model = VehicleLog
        fields = [
            'id', 'license_plate', 'car_color', 'status', 'is_inside',
            'slot_number', 'entry_time', 'exit_time', 'duration_hours',
            'total_fee',        # ← القيمة الحقيقية المخزنة، مش معادة الحساب
            'is_paid',
            'entry_image_url', 'exit_image_url',
            'collected_by_username', 'entry_shift_id', 'exit_shift_id',
        ]

    def get_duration_hours(self, obj):
        if not obj.exit_time or not obj.entry_time:
            return None
        entry, exit_ = obj.entry_time, obj.exit_time
        if timezone.is_aware(entry) and timezone.is_naive(exit_):
            exit_ = timezone.make_aware(exit_)
        elif timezone.is_naive(entry) and timezone.is_aware(exit_):
            entry = timezone.make_aware(entry)
        delta_seconds = (exit_ - entry).total_seconds()
        return round(delta_seconds / 3600, 2) if delta_seconds > 0 else None

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
        fields = ['id', 'slot_number', 'status', 'slot_type', 'floor', 'row', 'col', 'latitude', 'longitude']


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
            raise serializers.ValidationError({"password": "كلمتا المرور غير متطابقتين."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class AdminShiftSerializer(serializers.ModelSerializer):
    """سجل الشفتات - يعرض بيانات كل شفت مع الفرق المالي"""
    employee_username = serializers.CharField(source='employee.username', read_only=True)
    difference = serializers.SerializerMethodField()
    difference_status = serializers.SerializerMethodField()
    cars_entered_count = serializers.SerializerMethodField()
    cars_exited_count = serializers.SerializerMethodField()

    class Meta:
        model = Shift
        fields = [
            'id', 'employee_username', 'start_time', 'end_time', 'is_closed',
            'starting_cash', 'expected_collected_cash', 'actual_collected_cash',
            'difference', 'difference_status',
            'cars_entered_count', 'cars_exited_count',
        ]

    def get_difference(self, obj):
        if obj.actual_collected_cash is None:
            return None
        
        starting = float(obj.starting_cash or 0)
        expected = float(obj.expected_collected_cash or 0)
        actual = float(obj.actual_collected_cash or 0)
        
        # الفرق الصحيح = الفعلي - (العهدة + التحصيل المتوقع)
        total_expected_in_drawer = starting + expected
        return actual - total_expected_in_drawer

    def get_difference_status(self, obj):
        diff = self.get_difference(obj)
        if diff is None:
            return None
        if diff > 0:
            return "زيادة"
        elif diff < 0:
            return "عجز"
        return "متطابق"

    def get_cars_entered_count(self, obj):
        return obj.entries_recorded.count()

    def get_cars_exited_count(self, obj):
        return obj.exits_recorded.count()

        
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
 