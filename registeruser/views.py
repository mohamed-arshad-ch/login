from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth.models import User
from rest_framework import filters
from .serializers import UserSerializer, RegisterSerializer,ProfileSerializer
from .models import Profile
from django.contrib.auth import login
from django.contrib.auth import authenticate

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        


        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "user": UserSerializer(user, context=self.get_serializer_context()).data,
                    "token": AuthToken.objects.create(user)[1],
                    "status":"success"
                }
            )
        else:
            return Response(
                {
                    "message":serializer.errors,
                    
                    "status":"error"
                }
            )


class GetDetails(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = Profile.objects.all()

    def get(self,*args, **kwargs):
        try:
            profile = Profile.objects.get(slug=kwargs['slug'])

            return Response(
                {
                    "user":{
                        
                        "email":profile.user.email,
                        "phone":profile.phone_number,
                        "address":profile.address
                    },
                    "status":"success"
                }
            )
        except Profile.DoesNotExist:
            return Response(
                {
                    "message":"user not found",
                    "status":"error"
                }
            )


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    

    def post(self, request, format=None):
        
        user = authenticate(username=request.data['email'], password=request.data['password'])
        print(user)
        if user is not None:
            login(request,user)
            new_data = super(LoginAPI, self).post(request, format=None)
            new_data['status'] = "success"
            
            return new_data
        else:
            return Response(
                {
                    "data":"Invalid UserName And Password",
                    "status":"Error"
                    }
                )


class GetAllDetails(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    
    filter_backends = [filters.OrderingFilter]

    def filter_queryset(self, queryset):
        queryset = super(GetAllDetails, self).filter_queryset(queryset)
        return queryset.order_by('user__email')