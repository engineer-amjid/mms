from rest_framework import serializers

class ApproveMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)