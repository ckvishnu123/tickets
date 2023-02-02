from rest_framework import serializers
from api.models import CustomUser, Department, Tickets


class UserSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ["phone_number", "username", "password",
        "is_superuser", "role", "email", "created_at", "last_updated_at"]

    """ def create(self, validated_data):
        # calling create user in manager.py
        return CustomUser.objects.create_user(**validated_data) """

class DepartmentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Department
        fields = "__all__"

class TicketSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Tickets
        fields = "__all__"

    