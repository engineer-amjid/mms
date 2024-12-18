from rest_framework import serializers
from users.models import UserProfile
from users.models.user_rank_model import UserRank
from users.serializers.rank_serializer import UserRankSerializer


# Serializer for retrieving UserProfile data
# class UserProfileSerializer(serializers.ModelSerializer):
#     rank = UserRankSerializer(read_only=True)  # Display rank as a nested object
#
#     class Meta:
#         model = UserProfile
#         fields = ['id', 'email', 'username', 'role', 'phone', 'full_name', 'rank', 'is_approved']


# Serializer for creating a new UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    rank_id = serializers.PrimaryKeyRelatedField(
        queryset=UserRank.objects.all(), source='rank', write_only=True
    )
    rank = UserRankSerializer(read_only=True)  # Display rank details after creation

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'username', 'password', 'role', 'phone', 'full_name', 'rank', 'rank_id', 'is_approved']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
        }

    def create(self, validated_data):
        rank = validated_data.pop('rank', None)  # Extract rank if provided
        user = UserProfile.objects.create_user(**validated_data)
        if rank:
            user.rank = rank  # Assign rank to the user
            user.save()
        return user


# Serializer for updating UserProfile data
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    rank_id = serializers.PrimaryKeyRelatedField(
        queryset=UserRank.objects.all(), source='rank', write_only=True
    )
    rank = UserRankSerializer(read_only=True)  # Display rank details after update

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'phone', 'full_name', 'rank', 'rank_id']
        read_only_fields = ['email', 'role', 'is_approved']

    def update(self, instance, validated_data):
        # Update user fields
        rank = validated_data.pop('rank', None)  # Handle rank assignment separately
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if rank:
            instance.rank = rank
        instance.save()
        return instance