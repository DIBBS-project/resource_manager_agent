

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
