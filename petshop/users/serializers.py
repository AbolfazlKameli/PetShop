from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Address
from .services import check_otp_code
from .validators import validate_iranian_phone_number


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user, lifetime=None):
        token = super().get_token(user)
        if lifetime:
            token.set_exp(claim='exp', lifetime=lifetime)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data.update({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': self.user.id,
                'email': self.user.email
            }
        })
        return data


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('owner',)


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions')
        read_only_fields = ('last_login', 'role', 'is_active')


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Passwords must be match.'})
        try:
            validate_password(confirm_password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return attrs


class UserVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, required=False)
    phone_number = serializers.CharField(max_length=11, required=False, validators=[validate_iranian_phone_number])
    code = serializers.CharField(max_length=5)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        email = attrs.get('email')
        code = attrs.get('code')

        if email:
            if not check_otp_code(otp_code=code, email=email, action='verify'):
                raise serializers.ValidationError({'code': 'Code is invalid.'})
        elif phone_number:
            if not check_otp_code(otp_code=code, phone_number=phone_number, action='verify'):
                raise serializers.ValidationError({'code': 'Code is invalid.'})
        else:
            raise serializers.ValidationError('Entering an email address or phone number is required.')
        return attrs


class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, required=True)


class ResendVerificationSMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, required=True, validators=[validate_iranian_phone_number])


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, required=True, write_only=True)
    new_password = serializers.CharField(min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(min_length=8, required=True, write_only=True)

    def validate_old_password(self, data):
        user: User = self.context.get('user')
        if not user.check_password(data):
            raise serializers.ValidationError('Password is incorrect.')
        return data

    def validate(self, attrs):
        password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Passwords must be match.'})
        try:
            validate_password(confirm_password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return attrs


class SetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, required=True)
    code = serializers.CharField(max_length=5, required=True)
    new_password = serializers.CharField(min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(min_length=8, required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Passwords must be match.'})
        try:
            validate_password(confirm_password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        email = attrs.get('email')
        code = attrs.get('code')
        if not check_otp_code(otp_code=code, email=email, action='reset_password'):
            raise serializers.ValidationError({'code': 'Code is invalid.'})
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, required=True)
