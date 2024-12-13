from rest_framework import serializers
from users.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'username', 'password', 'role', 'phone', 'full_name', 'rank']  # Include necessary fields

    # Mark fields as required
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user