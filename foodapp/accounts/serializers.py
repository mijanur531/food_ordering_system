from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'age', 'address']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            age=validated_data.get('age'),
            address=validated_data.get('address', ''),
            user_type=User.CUSTOMER,
        )
        return user


class ClientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    business_name = serializers.CharField(write_only=True)
    business_type = serializers.ChoiceField(write_only=True, choices=('hotel', 'restaurant', 'partner'))
    mode = serializers.ChoiceField(write_only=True, choices=('online', 'offline'), default='online')
    business_address = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone',
                  'business_name', 'business_type', 'mode', 'business_address']

    def create(self, validated_data):
        from restaurants.models import ClientProfile
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            user_type=User.CLIENT,
        )
        ClientProfile.objects.create(
            user=user,
            business_name=validated_data['business_name'],
            business_type=validated_data['business_type'],
            mode=validated_data.get('mode', 'online'),
            address=validated_data['business_address'],
        )
        return user


class DeliveryRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    vehicle_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
    id_proof_number = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'age', 'vehicle_number', 'id_proof_number']

    def create(self, validated_data):
        from delivery.models import DeliveryBoyProfile
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            age=validated_data.get('age'),
            user_type=User.DELIVERY,
        )
        DeliveryBoyProfile.objects.create(
            user=user,
            vehicle_number=validated_data.get('vehicle_number', ''),
            id_proof_number=validated_data.get('id_proof_number', ''),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account has been disabled.')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'phone', 'age',
                  'is_age_verified', 'address', 'latitude', 'longitude']
        read_only_fields = ['id', 'user_type']
