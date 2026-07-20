from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Shift
class RegisterSerializer(serializers.ModelSerializer):
    # نطلب تأكيد كلمة المرور لزيادة الأمان
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "كلمات المرور غير متطابقة."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    """ لعرض بيانات المستخدم بعد تسجيل الدخول """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class ShiftSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.username')

    class Meta:
        model = Shift
        fields = ['id', 'employee_name', 'start_time', 'end_time', 'starting_cash', 'expected_collected_cash', 'actual_collected_cash', 'is_closed']
        read_only_fields = ['id', 'start_time', 'end_time', 'expected_collected_cash', 'is_closed']

class CloseShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ['actual_collected_cash']
        extra_kwargs = {
            'actual_collected_cash': {'required': True}
        }