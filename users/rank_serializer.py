from users.models import UserRank


class UserRankSerializer:
    class Meta:
        model = UserRank
        fields = '__all__'
    def create(self, validated_data):
        rank = UserRank.objects.create(**validated_data)
        return rank