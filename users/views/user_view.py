from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import UserProfile
from users.serializers.approve_member_serializer import ApproveMemberSerializer
from users.serializers.profile_serializer import  UserProfileUpdateSerializer, UserProfileSerializer
from users.utils.custom_permissions import IsAdminOrStaff, IsAdmin
from users.utils.custom_response import custom_response


def handle_serializer_errors(serializer, error_msg, status_code):
    """Utility function to handle serializer errors."""
    return custom_response(error_msg, status_code, data=serializer.errors)


def generate_tokens_for_user(user):
    """Utility function to generate JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(access),
    }


class UserLoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            tokens = serializer.validated_data
            user = serializer.user
            user_serializer = UserProfileSerializer(user)
            data = {
                "tokens": tokens,
                "user": user_serializer.data,
            }
            return custom_response("Login successful", status.HTTP_200_OK, data=data)
        except AuthenticationFailed:
            return custom_response("Invalid credentials", status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return custom_response("An error occurred", status.HTTP_400_BAD_REQUEST, data={"error": str(e)})


class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            return custom_response('Email already registered', status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = generate_tokens_for_user(user)
            data = {
                'user': serializer.data,
                'tokens': tokens,
            }
            return custom_response('User registered successfully', status.HTTP_201_CREATED, data=data)

        return handle_serializer_errors(serializer, 'Failed to register user', status.HTTP_400_BAD_REQUEST)


class AdminCreateUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    def post(self, request):
        role = request.data.get('role')
        if role not in ['admin', 'staff']:
            return custom_response('Invalid role', status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(f'{role.capitalize()} created successfully', status.HTTP_201_CREATED,
                                   data=serializer.data)

        return handle_serializer_errors(serializer, 'Failed to create user', status.HTTP_400_BAD_REQUEST)

class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return custom_response('Profile fetched successfully', status.HTTP_200_OK, data=serializer.data)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    serializer_class = UserProfileUpdateSerializer
    def put(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response('Profile updated successfully', status.HTTP_200_OK, data=serializer.data)

        return handle_serializer_errors(serializer, 'Failed to update profile', status.HTTP_400_BAD_REQUEST)


class MemberApproveView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    serializer_class = ApproveMemberSerializer
    def post(self, request):
        try:
            user = UserProfile.objects.get(id=request.data.get('user_id'))

            if user.is_approved:
                return custom_response('User is already approved', status.HTTP_400_BAD_REQUEST)

            user.is_approved = True
            user.save()
            return custom_response('User profile approved successfully', status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return custom_response('User not found', status.HTTP_404_NOT_FOUND)

class AllMembersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):
        members = UserProfile.objects.all()
        serializer = UserProfileSerializer(members, many=True)
        return custom_response('All members fetched successfully', status.HTTP_200_OK, data=serializer.data)

class AllApprovedMembersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):
        members = UserProfile.objects.filter(is_approved=True)
        serializer = UserProfileSerializer(members, many=True)
        return custom_response('Approved members fetched successfully', status.HTTP_200_OK, data=serializer.data)

class NewMembersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):
        members = UserProfile.objects.filter(is_approved=True)
        serializer = UserProfileSerializer(members, many=True)
        return custom_response('New members fetched successfully', status.HTTP_200_OK, data=serializer.data)