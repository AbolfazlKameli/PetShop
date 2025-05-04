from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User
from .services import check_otp_code
from .validators import validate_iranian_phone_number


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions')


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def validate_confirm_password(self, data):
        password1 = self.initial_data.get('password', False)
        if password1 and data and password1 != data:
            raise serializers.ValidationError('Passwords must be match.')
        try:
            validate_password(data)
        except serializers.ValidationError:
            raise serializers.ValidationError()
        return data


class UserVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, required=False)
    phone_number = serializers.CharField(max_length=11, required=False, validators=[validate_iranian_phone_number])
    code = serializers.CharField(max_length=5)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        email = attrs.get('email')
        code = attrs.get('code')

        if email:
            if not check_otp_code(otp_code=code, email=email):
                raise serializers.ValidationError({'code': 'Code is invalid.'})
        elif phone_number:
            if not check_otp_code(otp_code=code, phone_number=phone_number):
                raise serializers.ValidationError({'code': 'Code is invalid.'})
        else:
            raise serializers.ValidationError('Entering an email address or phone number is required.')
        return attrs


class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, required=True)
