from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.exceptions import AuthenticationFailed

from users.models import UserProfile
from users.serializers.profile_serializer import UserProfileSerializer, UserProfileUpdateSerializer
from users.serializers.approve_member_serializer import ApproveMemberSerializer
from users.utils.custom_response import custom_response
from users.utils.custom_permissions import IsAdminOrStaff, IsAdmin

def handle_serializer_errors(serializer, error_msg, status_code):
    return custom_response(error_msg, status_code, data=serializer.errors)

def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(access),
    }

class UserViewSet(viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    http_method_names = ['post', 'get', 'put']
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
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

    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = UserProfileSerializer(request.user)
        return custom_response('Profile fetched successfully', status.HTTP_200_OK, data=serializer.data)

    @extend_schema(
        request=UserProfileUpdateSerializer,
    )
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response('Profile updated successfully', status.HTTP_200_OK, data=serializer.data)

        return handle_serializer_errors(serializer, 'Failed to update profile', status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAdmin])
    def create_user(self, request):
        role = request.data.get('role')
        if role not in ['admin', 'staff']:
            return custom_response('Invalid role', status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(f'{role.capitalize()} created successfully', status.HTTP_201_CREATED, data=serializer.data)

        return handle_serializer_errors(serializer, 'Failed to create user', status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=ApproveMemberSerializer,
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAdminOrStaff])
    def approve_member(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return custom_response('user_id is required', status.HTTP_400_BAD_REQUEST)
        try:
            user = UserProfile.objects.get(id=request.data.get('user_id'))

            if user.is_approved:
                return custom_response('User is already approved', status.HTTP_400_BAD_REQUEST)

            user.is_approved = True
            user.save()
            return custom_response('User profile approved successfully', status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return custom_response('User not found', status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def all_members(self, request):
        members = UserProfile.objects.all()
        serializer = UserProfileSerializer(members, many=True)
        return custom_response('All members fetched successfully', status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def approved_members(self, request):
        members = UserProfile.objects.filter(is_approved=True)
        serializer = UserProfileSerializer(members, many=True)
        return custom_response('Approved members fetched successfully', status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def new_members(self, request):
        members = UserProfile.objects.filter(is_approved=True)
        serializer = UserProfileSerializer(members, many=True)
        return custom_response('New members fetched successfully', status.HTTP_200_OK, data=serializer.data)

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