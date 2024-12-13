from users.models.user_rank_model import UserRank


class UserRankSerializer:
    class Meta:
        model = UserRank
        fields = '__all__'
    def create(self, validated_data):
        rank = UserRank.objects.create(**validated_data)
        return rank