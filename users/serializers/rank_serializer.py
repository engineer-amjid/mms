from rest_framework import serializers
from users.models.user_rank_model import UserRank


class UserRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRank
        fields = ['id', 'name']
    def create(self, validated_data):
        rank = UserRank.objects.create(**validated_data)
        return rank