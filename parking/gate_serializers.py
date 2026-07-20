from rest_framework import serializers
from .models import VehicleLog


class GateEntrySerializer(serializers.ModelSerializer):
    entry_image_url = serializers.SerializerMethodField()

    class Meta:
        model = VehicleLog
        fields = ['id', 'license_plate', 'entry_time', 'car_color', 'entry_image_url', 'status']

    def get_entry_image_url(self, obj):
        request = self.context.get('request')
        if obj.entry_image:
            return request.build_absolute_uri(obj.entry_image.url) if request else obj.entry_image.url
        return None


class GateExitSerializer(serializers.ModelSerializer):
    exit_image_url = serializers.SerializerMethodField()
    entry_image_url = serializers.SerializerMethodField()
    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = VehicleLog
        fields = ['id', 'license_plate', 'entry_time', 'exit_time', 'total_fee',
                  'is_paid', 'car_color', 'entry_image_url', 'exit_image_url', 'duration_minutes']

    def get_exit_image_url(self, obj):
        request = self.context.get('request')
        if obj.exit_image:
            return request.build_absolute_uri(obj.exit_image.url) if request else obj.exit_image.url
        return None

    def get_entry_image_url(self, obj):
        request = self.context.get('request')
        if obj.entry_image:
            return request.build_absolute_uri(obj.entry_image.url) if request else obj.entry_image.url
        return None

    def get_duration_minutes(self, obj):
        if obj.exit_time and obj.entry_time:
            return round((obj.exit_time - obj.entry_time).total_seconds() / 60, 1)
        return None

# ضيف ده تحت السيريالايزرز الموجودة في نفس الملف

class VehicleLogFullSerializer(serializers.ModelSerializer):
    """يعرض كل المعلومات الممكنة عن السيارة - يستخدم في جداول السجل الكامل"""
    entry_image_url = serializers.SerializerMethodField()
    exit_image_url = serializers.SerializerMethodField()
    duration_minutes = serializers.SerializerMethodField()
    slot_number = serializers.CharField(source='slot.slot_number', default=None, read_only=True)
    collected_by_username = serializers.CharField(source='collected_by.username', default=None, read_only=True)

    class Meta:
        model = VehicleLog
        fields = [
            'id', 'license_plate', 'car_color', 'status', 'is_inside',
            'entry_time', 'exit_time', 'duration_minutes',
            'entry_image_url', 'exit_image_url',
            'total_fee', 'is_paid', 'slot_number', 'collected_by_username',
        ]

    def get_entry_image_url(self, obj):
        request = self.context.get('request')
        if obj.entry_image:
            return request.build_absolute_uri(obj.entry_image.url) if request else obj.entry_image.url
        return None

    def get_exit_image_url(self, obj):
        request = self.context.get('request')
        if obj.exit_image:
            return request.build_absolute_uri(obj.exit_image.url) if request else obj.exit_image.url
        return None

    def get_duration_minutes(self, obj):
        if obj.exit_time and obj.entry_time:
            return round((obj.exit_time - obj.entry_time).total_seconds() / 60, 1)
        return None
        