from rest_framework.views import APIView
from users.models.user_rank_model import UserRank


class RankView(APIView):

    def get(self, request):
        ranks = UserRank.objects.all()