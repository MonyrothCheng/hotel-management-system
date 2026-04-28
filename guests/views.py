from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Guest
from .serializers import GuestSerializer

@api_view(['GET', 'POST'])
def guest_list(request):
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)