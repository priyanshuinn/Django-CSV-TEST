from django.http import HttpResponse
from rest_framework import viewsets
from django.contrib.auth.models import User,Group
from task.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .exceptions import NoPermission,WrongAuthorization

# Create your views here.

def home(request):
    return HttpResponse('<h1> Credicxo Django Task</h1>')

class UserViewSet(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer
    
    @action(detail = False,methods =["GET"])
    def me(self,request): # /me/ endpoint for showing user details
        user = User.objects.filter(pk=request.user.id).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(None)
    @action(detail = False,methods =["POST"])
    def reset_password(self,request): # /reset_password/ enpoint for creating new password
        user = User.objects.filter(pk=request.user.id).first()
        print(user.username)
        if user:
            if not request.data.get("new_password",None): # checking if new_password field is provided or not
                return Response('''{'new_password': 'This field is required.'}''',status=404)
            user.set_password(str(request.data["new_password"]))
            user.save()
            return Response("!!! Password Updated Successfully !!!")
        else:
            return Response("Wrong Authorization Token Passed !!!") # if user does not exist in database
    
    def get_queryset(self): # return the default queryset according to user's access
        user = User.objects.filter(pk=self.request.user.id).first()
        serializer = UserSerializer(user)
        print(serializer.data)
        l=[g.name for g in self.request.user.groups.all()]
        print(l)
        if serializer.data["username"]=="":
            raise WrongAuthorization()
        elif serializer.data.get('is_superuser',None):
            return User.objects.all()
        elif len(l)!=0 and 'Teachers' in l:
            return User.objects.filter(groups__name='Students') # all teacher able to list student details
        elif len(l)!=0 and 'Students' in l:
            user = User.objects.filter(pk=self.request.user.id)
            return user
        raise NoPermission()
    
    def create(self, request, *args, **kwargs): # overwriting the existinf create() according to our need
        l=[g.name for g in request.user.groups.all()]
        print(l)
        if not request.data.get("password",None):
                return Response('''{'password': 'this is a required field.'}''',status=405)
        if request.user.is_superuser:
            if not request.data.get("group",None):
                return Response('''{'group': 'This field is required.'}''',status=401)
            elif not (("Teachers" in request.data.get("group",None)) or ("Students" in request.data.get("group",None))):
                return Response('''{'group': 'group can take either value 'Teachers' or 'Students'.]'}''',status=402)
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception = True)
            user = serializer.save()
            group = Group.objects.get(name=request.data.get("group",None))
            user.groups.add(group)
            user.set_password(str(request.data["password"]))
            user.save()
            return Response(serializer.data)
        elif len(l)!=0 and 'Teachers' in l: 
            if request.data.get("group",None):
                return Response("You don't have access to assign group !!",status=403)
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception = True)
            user = serializer.save()
            group = Group.objects.get(name='Students')
            user.groups.add(group)
            user.set_password(str(request.data["password"]))
            user.save()
            return Response(serializer.data)
        return Response("You don't have any access to create an user.")

