from django.shortcuts import render
from django.http import JsonResponse
from .models import Guest,Movie,Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer,MovieSerializer,ReservationSerializer
from rest_framework.response import Response
from rest_framework import status,filters
# Create your views here.

#1 without Rest and no model query FBV
def no_rest_no_model(request):
    guests = [
        {   'id':1,
            'Name':'Ahmed',
            'mobile':48767
        },
        {
            'id':2,
            'Name':'Sara',
            'mobile':556487
        },
    ] 

    return JsonResponse(guests,safe=False)

#model data default django without rest
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'Guests':list(data.values('name','mobile'))
        }
    return JsonResponse(response)

#list==GET
#Create==POST
#pk query == GET
#update == PUT
#DELETE Destroy == DELETE
#Function Based View
#3.1 GET POST
@api_view(['GET','POST'])
def FBV_List(request):
    #GET
    if request.method =='GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests,many=True)
        return Response(serializer.data)
    #POST
    elif request.method == 'POST':
        data = request.data
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data,status=status.HTTP_201_CREATED)
        return Response(request.data,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    #PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    #DELETE
    elif  request.method =='DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)