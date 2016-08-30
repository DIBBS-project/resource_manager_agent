from django.views.decorators.csrf import csrf_exempt
import django.contrib.auth

from serializers import UserSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = django.contrib.auth.get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])
@csrf_exempt
def create_account(request):
    from oma_client.apis.users_api import UsersApi
    from oma_client.configure import configure_auth_basic
    import string
    import random
    import sys

    def generate_random_string(size, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    username = "user_%s" % (generate_random_string(25))

    user_data = {
        "username": username,
        "password": generate_random_string(20)
    }

    configure_auth_basic("admin", "pass")  # TODO: Change to a user that is not a superuser (created in User Data)

    UsersApi().users_post(data=user_data)

    return Response(user_data, status=status.HTTP_202_ACCEPTED)
