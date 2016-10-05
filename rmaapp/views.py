from django.views.decorators.csrf import csrf_exempt
import django.contrib.auth

from serializers import UserSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64


def configure_basic_authentication(swagger_client, username, password):
    authentication_string = "%s:%s" % (username, password)
    base64_authentication_string = base64.b64encode(bytes(authentication_string))
    header_key = "Authorization"
    header_value = "Basic %s" % (base64_authentication_string, )
    swagger_client.api_client.default_headers[header_key] = header_value


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

    users_client = UsersApi()
    configure_basic_authentication(users_client, "admin", "pass")  # TODO: Change to a user that is not a superuser (created in User Data)

    users_client .users_post(data=user_data)

    return Response(user_data, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@csrf_exempt
def add_to_host_file(request):

    print(request.POST)
    if "hostname" not in request.POST:
        return Response({"response": "KO", "msg": "missing 'hostname' parameter"}, status=status.HTTP_202_ACCEPTED)

    if "ip" not in request.POST:
        return Response({"response": "KO", "msg": "missing 'ip' parameter"}, status=status.HTTP_202_ACCEPTED)

    ip = request.POST["ip"]
    hostname = request.POST["hostname"]

    with open("/etc/hosts", "a") as hostfile:
        hostfile.write("%s %s\n" % (ip, hostname))

    return Response({"response": "OK"}, status=status.HTTP_202_ACCEPTED)
