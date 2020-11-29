from django.contrib.auth.models import User
from rest_framework import serializers


class ReadOnlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_active',
                  'last_login', 'is_superuser')
        read_only_fields = ('last_login', 'is_superuser')

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class WriteOnlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'password', 'is_active')

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()
        return instance
