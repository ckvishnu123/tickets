from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, authentication

from api.serializers import UserSerializers, DepartmentSerializer, TicketSerializer
from api.models import CustomUser, Department, Tickets

# Create your views here.

class UsersView(ModelViewSet):
    # permission class is set bcoz only admin can create new users
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    # here http method is set to post as we need user creation only
    serializer_class = UserSerializers
    queryset = CustomUser.objects.all()
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            if request.query_params.get("department"):
                name = request.query_params.get("department")
                dep = Department.objects.get(name=name)
                CustomUser.objects.create_user(**serializer.validated_data, department=dep)
            else:
                CustomUser.objects.create_user(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class DepartmentView(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    # admin only can manage CRUD of department
    permission_classes = [permissions.IsAdminUser]

    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    # we need get here to list all departments
    # all admin users can perform updation, delete etc
    http_method_names = ["post", "get", "put", "delete"]


class TicketView(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = TicketSerializer
    queryset = Tickets.objects.all()
    http_method_names = ["get", "post"]

    # here we need to override get_queryset because we need to list tickets -
    # of loginned user only

    def get_queryset(self):
        return Tickets.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class TicketAdminview(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    # here permission class is set to IsAdminUser bcoz admin has only access to-
    # manage all tickets, delte etc.
    permission_classes = [permissions.IsAdminUser]

    serializer_class = TicketSerializer
    queryset = Tickets.objects.all()
    http_method_names = ["get", "put", "delete"]
    # here no need to override listing bcoz all admin users must be
    # able to perform CRUD
    # admin also can use normal user create

    