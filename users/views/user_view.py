from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import UserProfile
from users.serializers.profile_serializer import UserProfileCreateSerializer, UserProfileUpdateSerializer
from users.utils.custom_permissions import IsAdminOrStaff, IsAdmin
from users.utils.custom_response import custom_response


class UserLoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            tokens = serializer.validated_data

            # Serialize user data
            user = serializer.user
            user_serializer = UserProfileCreateSerializer(user)
            # Custom response format
            data = {
                "tokens": tokens,
                "user": user_serializer.data,
            }
            return custom_response("Login successful", status.HTTP_200_OK, data=data)

        except AuthenticationFailed as e:
            return custom_response("Invalid credentials", status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return custom_response("An error occurred", status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
class RegisterUserView(APIView):
    permission_classes = [AllowAny,]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileCreateSerializer

    def post(self, request, *args, **kwargs):
        if UserProfile.objects.filter(email=request.data.get('email')).exists():
            return custom_response('Email already registered', status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate JWT tokens for the registered user
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)

            # Include the tokens in the custom response
            data = {
                'user': serializer.data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(access),
                }
            }
            return custom_response('User registered successfully', status.HTTP_201_CREATED, data=data)
        return custom_response('Failed to register user', status.HTTP_400_BAD_REQUEST, data=serializer.errors)

class AdminCreateUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileCreateSerializer
    def post(self, request):
        role = request.data.get('role')
        if role not in ['admin', 'staff']:
            return custom_response('Invalid role', status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return custom_response(f'{role.capitalize()} created successfully', status.HTTP_201_CREATED, data=serializer.data)

        return custom_response('Failed to create user', status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class AllMembersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):
        print(request.user.role)
        members = UserProfile.objects.all()
        serializer = UserProfileCreateSerializer(members, many=True)
        return custom_response('All members fetched successfully', status.HTTP_200_OK, data=serializer.data)

class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user.role)
        serializer = UserProfileCreateSerializer(request.user)
        return custom_response('Profile fetched successfully', status.HTTP_200_OK, data=serializer.data)

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    serializer_class = UserProfileUpdateSerializer
    def put(self, request):
        # Get the logged-in user
        user = request.user

        # Serialize the request data and update the user instance
        serializer = UserProfileCreateSerializer(user, data=request.data, partial=True)  # Use `partial=True` for partial updates
        if serializer.is_valid():
            serializer.save()
            return custom_response('Profile updated successfully', status.HTTP_200_OK, data=serializer.data)
        return custom_response('Failed to update profile', status.HTTP_400_BAD_REQUEST, data=serializer.errors)