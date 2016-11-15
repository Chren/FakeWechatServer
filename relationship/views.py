#!/usr/bin/python
#-*-coding:utf-8-*-

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from relationship.models import IMUser
from django.views.decorators.csrf import csrf_exempt
from relationship.serializers import IMUserSerializer,LoginUserSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from django.db.models import Q
import uuid
import json

from rongcloud import RongCloud

app_key = '6tnym1brnsfy7'
app_secret = 'L4HtbD4coIXzo'
rcloud = RongCloud(app_key, app_secret)

# Create your views here.

def authorise(deviceid, token):
	if not token:
		return False
	try:
		user = IMUser.objects.get(token=token)
	except IMUser.DoesNotExist:
		return False
	return user

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, errorcode=200, errormsg="success", **kwargs):
    	print(kwargs)
    	composite = {}
    	if isinstance(data, list):
    		composite = {"errorcode":errorcode, "errormsg":errormsg, "data":{"result":data}}
    	else:
    		composite = {"errorcode":errorcode, "errormsg":errormsg, "data":data}
    	
        content = JSONRenderer().render(composite)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class UserList(APIView):
    """
    List all users, or create a new user.
    """
    def get(self, request, format=None):
    	try:
    		token = request.META['HTTP_TOKEN']
    	except KeyError:
    		return JSONResponse('', errorcode=417, errormsg="token empty")
    	if not authorise('', token):
    		return JSONResponse('', errorcode=418, errormsg="invalid token")
        users = IMUser.objects.all()
        serializer = IMUserSerializer(users, many=True)
        return JSONResponse(serializer.data, errorcode=200, errormsg="success")

class FriendList(APIView):
    def get(self, request, format=None):
    	try:
    		token = request.META['HTTP_TOKEN']
    	except KeyError:
    		return JSONResponse('', errorcode=417, errormsg="token empty")

    	if not authorise('', token):
    		return JSONResponse('', errorcode=418, errormsg="invalid token")

    	try:
    		tempuser = IMUser.objects.get(token=token)
    	except IMUser.DoesNotExist:
    		return JSONResponse('', errorcode=419, errormsg="invalid token")
    	
    	friends = tempuser.friendlist
    	serializer = IMUserSerializer(friends, many=True)
    	return JSONResponse(serializer.data, errorcode=200, errormsg="success")

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	def get_object(self, pk):
		try:
			return IMUser.objects.get(pk=pk)
		except IMUser.DoesNotExist:
			return JSONResponse('', errorcode=511, errormsg="user not exist")
	def get(self, request, pk, format=None):
		user = self.get_object(pk)
		serializer = IMUserSerializer(user)
		return JSONResponse(serializer.data)
	def put(self, request, pk, format=None):
		user = self.get_object(pk)
		serializer = IMUserSerializer(user, data=request.data)
		if serializer.is_valid():
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, errorcode=400, errormsg="bad request")
	def delete(self, request, pk, format=None):
		user = self.get_object(pk)
		user.delete()
		return JSONResponse(status=status.HTTP_204_NO_CONTENT, errorcode=400, errormsg="no content")

@api_view(['POST'],)
def login(request):
    try:
        phone = request.POST['phone']
        password = request.POST['password']
    except KeyError:
		return JSONResponse('', errorcode=419, errormsg="invalid param")
    try:
        imuser = IMUser.objects.get(Q(phone=phone), Q(password=password))
        imuser.token = str(uuid.uuid4())
        if not imuser.rctoken:
            r = rcloud.User.getToken(userId=imuser.userid, name=imuser.name, portraitUri=imuser.photo)
            imuser.rctoken = r.result['token']
        imuser.save()
        serializer = LoginUserSerializer(imuser)
        return JSONResponse(serializer.data)
    except IMUser.DoesNotExist:
        return JSONResponse(password, errorcode=511, errormsg="incorrect param")

@api_view(['POST'],['GET'])
def logout(request):
    try:
        token = request.META['HTTP_TOKEN']
    except KeyError:
        return JSONResponse('', errorcode=417, errormsg="token empty")

    if not authorise('', token):
        return JSONResponse('', errorcode=418, errormsg="invalid token")

    try:
        tempuser = IMUser.objects.get(token=token)
    except IMUser.DoesNotExist:
        return JSONResponse('', errorcode=418, errormsg="invalid token")

    tempuser.token = ''
    tempuser.save()
    return JSONResponse('')

@api_view(['POST'],['GET'])
def magic(request):
    try:
        token = request.META['HTTP_TOKEN']
    except KeyError:
        return JSONResponse('', errorcode=417, errormsg="token empty")

    if not authorise('', token):
        return JSONResponse('', errorcode=418, errormsg="invalid token")
    try:
        tempuser = IMUser.objects.get(userid=2)
    except IMUser.DoesNotExist:
        return JSONResponse('', errorcode=419, errormsg="invalid token")

    friends = tempuser.friendlist
    for friend in friends:
        fromUserId = str(friend.userid)
        toUserId = "2"
        r=rcloud.Message.publishPrivate(
            fromUserId = fromUserId,
            toUserId = toUserId,
            content = '{"content":"祝福你们！","extra":"helloExtra"}',
            objectName = 'RC:TxtMsg',
            pushContent = "new message",
            pushData='{"pushData":"new message"}')
    return JSONResponse('')

@api_view(['POST'],['GET'])
def msgrouter(request):
    try:
        token = request.META['HTTP_TOKEN']
    except KeyError:
        return JSONResponse('', errorcode=417, errormsg="token empty")
    if not authorise('', token):
        return JSONResponse('', errorcode=418, errormsg="invalid token")

    try:
        fromUserId = request.POST['fromUserId']
        toUserId = request.POST['toUserId']
        content = request.POST['content']
        objectName = request.POST['objectName']
        extra = request.POST['extra']
    except KeyError:
        return JSONResponse('', errorcode=419, errormsg="invalid param")
    contentDict = json.loads(content)
    contentDict['extra'] = extra
    rcloud.Message.publishPrivate(
        fromUserId = fromUserId,
        toUserId = toUserId,
        content = json.dumps(contentDict),
        objectName = objectName,
        pushContent = "new message",
        pushData='{"pushData":"new message"}')
    return JSONResponse('')

@api_view(['POST'],['GET'])
def sendmsg(request):
    try:
        token = request.META['HTTP_TOKEN']
    except KeyError:
        return JSONResponse('', errorcode=417, errormsg="token empty")
    if not authorise('', token):
        return JSONResponse('', errorcode=418, errormsg="invalid token")

    try:
        fromUserId = request.GET['fromUserId']
        toUserId = request.GET['toUserId']
        content = request.GET['content']
        objectName = request.GET['objectName']
        extra = request.GET['extra']
    except KeyError:
        return JSONResponse('', errorcode=419, errormsg="invalid param")
    contentDict = json.loads(content)
    contentDict['extra'] = extra
    rcloud.Message.publishPrivate(
        fromUserId = fromUserId,
        toUserId = toUserId,
        content = json.dumps(contentDict),
        objectName = objectName,
        pushContent = "new message",
        pushData='{"pushData":"new message"}')
    return JSONResponse('')
