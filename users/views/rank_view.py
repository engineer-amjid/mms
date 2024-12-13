from rest_framework.views import APIView
from users.models import UserRank


class RankView(APIView):

    def get(self, request):
        ranks = UserRank.objects.all()