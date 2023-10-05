#from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from testapp.models import Person
from testapp.serializers import PersonSerializer, LoginSerializer, RegisterSerializer

from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated

from django.core.paginator import Paginator

from rest_framework.decorators import action

# Create your views here.

class loginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer= LoginSerializer(data = data)

        if not serializer.is_valid():
            return Response({'status':False, 'message':serializer.errors}, status.HTTP_400_BAD_REQUEST)
        user =authenticate(username = serializer.data['username'], password =serializer.data['password'])
        print(user)
        if not user:
            return Response({'status':False, 'message':'invalid credentials'}, status.HTTP_400_BAD_REQUEST)



        token, _ = Token.objects.get_or_create(user=user)
        return Response({'status':True, 'message':'successfull login', 'token':str(token)} ,status.HTTP_201_CREATED)



class RegisterAPI(APIView):
    def post(self , request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({'status':False, 'message':serializer.errors}, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'status':True, 'message':'user created'},status.HTTP_201_CREATED)








@api_view(['GET','POST','PUT'])
def index(request):

    #if request.method == 'GET':
    courses = {
            'course_name': 'Python',
            'learn':['flask','django','tornado','fastapi'],
            'course_provider': 'scaler'

    }
    
    if request.method == 'GET':
        print(request.GET.get('search'))
        print('you hit a get response ')
        return Response(courses)
    elif request.method == 'POST':
        data = request.data # Accept data from frontend 
        print(data['age']) # console , post 

        print('you hit a POSt response ')
        return Response(courses)
    elif request.method == 'PUT':
        print('you hit a PUT response ')
        return Response(courses)







#login

@api_view(['POST'])
def login(request):
    data = request.data
    serializer= LoginSerializer(data = data)

    if serializer.is_valid():
        data = serializer.validated_data
        #data = serializer.data   # taking the data n printing in conlsole 
        #print(data)
        return Response({'message':'success'})

    return Response(serializer.errors)


# class helps in encapsulationss it reduceses the code 
#no need to write extra logic  
class PersonAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        #print(request.user)
        objs = Person.objects.all()
        page= request.GET.get('page',1)
        page_size=3
        try:
            paginator = Paginator(objs , page_size)
            print(paginator.page(page))
        except Exception as e:
            return Response({'status':False, 'message':'invalid page'})
        #print(paginator.page(page))
        serializer= PersonSerializer(paginator.page(page),many=True)

        #serializer = PersonSerializer(objs, many= True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer= PersonSerializer(data = data) # check if serializer is valid, all fields r required 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    
    def put(self, request):
        data = request.data
        serializer= PersonSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer= PersonSerializer(obj,data = data, partial = True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'data is deleted '})






# Person 
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.all()
        serializer = PersonSerializer(objs, many= True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer= PersonSerializer(data = data) # check if serializer is valid, all fields r required 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'PUT':
        data = request.data
        serializer= PersonSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


    elif request.method == 'PATCH':  #partial update
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer= PersonSerializer(obj,data = data, partial = True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    else:
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'data is deleted '})


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer   
    queryset = Person.objects.all()  #all crued r done 
    #http_method_names = ['get','post']
    def list(self , request):
        search = request.GET.get('search')
        queryset =self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
        
        serializer= PersonSerializer(queryset, many=True)

        return Response({'status':200, 'data':serializer.data},status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['POST'])
    def send_mail_to_person(self,request,pk):
        print(pk)
        obj = Person.objects.get(pk=pk)
        serializer = PersonSerializer(obj)
        return Response({'status':True, 'message':'email sent successfully', 'data': serializer.data
    })


