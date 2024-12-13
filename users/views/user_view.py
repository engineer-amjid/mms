from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from users.models import UserProfile
from users.serializers.profile_serializer import UserProfileSerializer
from users.utils.custom_response import custom_response


class RegisterUserView(APIView):
    permission_classes = [AllowAny,]

    parser_classes = [JSONParser, MultiPartParser, FormParser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        # Check if email is already in use
        if UserProfile.objects.filter(email=request.data.get('email')).exists():
            return custom_response('Email already registered', status.HTTP_400_BAD_REQUEST)

        # Serialize the data
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response('User registered successfully', status.HTTP_201_CREATED, data=serializer.data)

        return custom_response('Failed to register user', status.HTTP_400_BAD_REQUEST, data=serializer.errors)

class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, many=False)
        return custom_response('User profile fetched successfully', status.HTTP_200_OK, data=serializer.data)

    def put(self, request):
        user = request.user
        # Update other fields
        user.full_name = request.data.get('full_name', user.full_name)
        user.phone = request.data.get('phone', user.phone)
        user.rank = request.data.get('rank', user.rank)
        user.save()
        return custom_response('Profile updated successfully', status.HTTP_200_OK)


class AllUsersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return custom_response('All users fetched successfully', status.HTTP_200_OK, data=serializer.data)
