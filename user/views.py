from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated


from django.contrib.auth.models import User
from .serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(User.objects.all(), pk=pk)
            serializer = ReadOnlyUserSerializer(user)
            return Response({"user": serializer.data})
        users = User.objects.all()
        serializer = ReadOnlyUserSerializer(users, many=True)
        return Response({"users": serializer.data})

    def post(self, request):
        user = request.data.get('user')
        serializer = WriteOnlyUserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
            return Response({"success": "User '{}' created successfully"
                            .format(user_saved.username)})

    def put(self, request, pk):
        saved_user = get_object_or_404(User.objects.all(), pk=pk)
        data = request.data.get('user')
        serialized = WriteOnlyUserSerializer(instance=saved_user,
                                             data=data, partial=True)
        if serialized.is_valid(raise_exception=True):
            user_saved = serialized.save()
            return Response({"success": "User '{}' updated successfully"
                            .format(user_saved.username)})

    def delete(self, request, pk):
        user = get_object_or_404(User.objects.all(), pk=pk)
        data = {"is_active": False}
        serialized = WriteOnlyUserSerializer(instance=user,
                                             data=data, partial=True)
        if serialized.is_valid(raise_exception=True):
            user = serialized.save()
            return Response({"success": "User '{}' delete successfully"
                            .format(user.username)})
