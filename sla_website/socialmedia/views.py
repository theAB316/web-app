from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm

from .models import Acts, Post, CustomUser

#from .models import CustomUser


from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
import base64
import binascii
from django.core.files import File
import cv2
import os
from django.core.files.base import ContentFile



class IndexView(generic.ListView):
	model = Acts
	template_name = 'socialmedia/index.html'
	context_object_name = 'allActs'


#index view for the news feed of each ActType
class DetailView(generic.DetailView):
	model = Acts
	template_name = 'socialmedia/detail.html'
	context_object_name = 'act'
	
class PostCreate(CreateView):
	model = Post
	#template_name = 'socialmedia/detail.html'
	#context_object_name = 'posts'

	#fields for the user to fill out in the form
	fields = ['user', 'act', 'caption', 'image', 'timestamp']

'''class PostUpdate(UpdateView):
	model = Post
	#template_name = 'socialmedia/detail.html'
	#context_object_name = 'posts'

	#fields for the user to fill out in the form
	fields = ['act', 'name', 'caption', 'image']


class PostDelete(DeleteView):
	model = Post
	success_url = reverse_lazy('socialmedia:index')
'''


class UserFormView(View):
	form_class = UserForm
	template_name = 'socialmedia/registration_form.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user.set_password(password)
			user.save()

			user = authenticate(username = username, password = password)

			if user is not None:
				if user.is_active:
					login(request, user)
					#return redirect('socialmedia:index')
					return render(request, 'socialmedia/index.html', {})
					#return Response(status=status.HTTP_201_CREATED)



			#return render(request, self.template_name, {'form': form})
			#return Response (status=status.HTTP_400_BAD_REQUEST)
			return render(request, 'socialmedia/index.html', {})



#	REST API 
#
#
#

#1 - Add user -  /api/v1/users

def check_sha1(password):
	n = len(password)
	if n != 40:
		return 0

	valid_chars = []
	for i in range(0, 10):
		valid_chars.append(str(i))
	
	string = 'abcdefABCDEF'
	for char in string:
		valid_chars.append(char)
	

	for char in password:
		if char not in valid_chars:
			return 0

	#valid password
	return 1

class UserCreate(APIView):
	def post(self, request, username=''):
		
		data = request.data
		username = data.get('username')
		password = data.get('password')

		if(not check_sha1(password)):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		try:
			user = CustomUser.objects.get(username = username)
			return Response(status=status.HTTP_400_BAD_REQUEST)

		except:
			new_user = CustomUser()
			new_user.username = username
			new_user.password = password
			new_user.save()

			return Response(status=status.HTTP_201_CREATED)

#2. Remove user - /api/v1/users/{username}
class UserDelete(APIView):
	def delete(self, request, username):
		username = self.kwargs.get('username', None)
		
		try:
			user = CustomUser.objects.get(username = username)
			user.delete()
			return Response(status=status.HTTP_200_OK)

		except CustomUser.DoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)


#3. List categories - api/v1/categories
#4. Add categories - api/v1/categories
class ListAddActsCategories(APIView):

	def get(self, request, actType=''):

		acts = Acts.objects.all()

		if(acts.count() == 0):
			return Response(status=status.HTTP_204_NO_CONTENT)

		count = dict()

		for act in acts:
			count[act.actType] = act.post_set.all().count()

		return Response(count, status=status.HTTP_200_OK)


	def post(self, request, actType=''):
		
		data = request.data
		data = data[0]


		try:
			Acts.objects.get(actType = str(data))
			
		except Acts.DoesNotExist:
			new_act = Acts()
			new_act.actType = str(data)
			new_act.save()

			return Response(status=status.HTTP_201_CREATED)

		return Response(status=status.HTTP_400_BAD_REQUEST)
		

#5. Remove category - /api/v1/categories/{categoryName}
class DeleteActsCategories(APIView):
	def delete(self, request, actType):
		data = self.kwargs.get('actType', None)

		try:
			act = Acts.objects.get(actType = str(data))

		except Acts.DoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		act.delete()
		return Response(status=status.HTTP_200_OK)
					

		


#6. List acts for a given category - /api/v1/categories/{categoryName}/acts

class ListPostAct(APIView):
	def get(self, request, actType):
		data = self.kwargs.get('actType', None)
		
		act = Acts.objects.get(actType = data)
		count = act.post_set.all().count()

		
		if(count >= 500):
			return Response(status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
		elif(count == 0):
			return Response(status=status.HTTP_204_NO_CONTENT)	
		
		response_dict= dict()
		response_data = []

		for post in act.post_set.all():
			print("usernmae", post.user)
			response_dict = {
				'username': str(post.user),
				'timestamp': post.timestamp,
				'actID': post.id,
				'caption': post.caption,
				#'imgB64': base64.b64encode((post.image).file.read())
				'imgB64': post.image
			}
			'''response_dict['actID'] = post.id
			response_dict['caption'] = post.caption
			response_dict['imgB64'] = base64.b64encode((post.image).file.read())'''
			response_data.append(response_dict)

		return Response(response_data, status=status.HTTP_200_OK)


#7. List number of acts for a given category - /api/v1/categories/{categoryName}/acts/size
class ListPostsSize(APIView):
	def get(self, request, actType):
		data = self.kwargs.get('actType', None)
		
		acts = Acts.objects.all()

		try:
			act = Acts.objects.get(actType = str(data))

		except Acts.DoesNotExist:
			return Response(status=status.HTTP_204_NO_CONTENT)

		count = act.post_set.all().count()
		return Response(count, status=status.HTTP_200_OK)


		


#8. Return number of acts for a given category in a given range (inclusive) - /api/v1/categories/{categoryName}/acts?start={startRange}&end={endRange}

class ListPostRange(APIView):
	def get(self, request, actType, startRange, endRange):
		Type = self.kwargs.get('actType', None)
		startRange = self.kwargs.get('startRange', None)
		EndRange = self.kwargs.get('endRange', None)

		try:
			acts = Acts.objects.get(actType = Type)
		except Acts.DoesNotExist:
			return Response(status= status.HTTP_204_NO_CONTENT)


		no_of_posts = Acts.objects.all().count()
		if(startRange < 1 or endRange > no_of_posts):
			return Response(status= status.HTTP_400_BAD_REQUEST)

		count = endRange-startRange+1
		if(count > 100 or count < 1):
			return Response(status = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
		
		count2 = 0
		response_data = []
		for post in acts.post_set.all.reversed():
			if(count2 == count or count2 == no_of_posts):
				break;

			response_dict = dict()
			response_dict = {
				'username': str(post.user),
				'timestamp': post.timestamp,
				'actID': post.id,
				'caption': post.caption,
				#'imgB64': base64.b64encode((post.image).file.read())
				'imgB64': post.image
			}
			response_data.append(response_dict)
			count2 += 1

		return Response(response_data, status = status.HTTP_200_OK)


#9. Upvote an act - Route: /api/v1/acts/upvote

class UpvotePost(APIView):
	def post(self, request):
		postID = request.data[0]
		print('\n\n\n\n lol')
		try:
			post = Post.objects.get(id = postID)

		
		except Post.DoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		post.upvotes += 1
		post.save()
		return Response(status = status.HTTP_200_OK)



#10. Remove an act - /api/v1/acts/{actId}

class RemovePost(APIView):
	#/api/v1/acts/{actId}
	def delete(self, request, actID):
		#actID is post.id here!!!

		data = self.kwargs.get('actID', None)
		#data = request.data
		try:
			post_del = Post.objects.get(pk = data)
			post_del.delete()
			return Response(status=status.HTTP_200_OK)

		except Post.DoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)


#11. Upload an act - /api/v1/acts
class AddPost(APIView):	
	def post(self, request):
		
		data = request.data
		

		actID = data.get('actID')

		username = str(data.get('username'))
		actType = str(data.get('actType'))
		timestamp = data.get('timestamp')
		caption = data.get('caption')
		imgB64 = data.get('imgB64')
		
		

		posts = Post.objects.all()

		if actID in posts.values_list('id', flat=True):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		try:
			image_binary = base64.b64decode(imgB64)
		except binascii.Error:
			return Response(status=status.HTTP_400_BAD_REQUEST)


		new_post = Post()

		new_post.act = Acts.objects.get(actType = str(actType))
		new_post.user = CustomUser.objects.get(username = str(username))

		new_post.id = actID
		new_post.caption = caption
		new_post.image = imgB64
		
		#timestamp read is in the format of “DD-MM-YYYY:SS-MM-HH”,
		dd = timestamp[0:2]
		mm = timestamp[3:5]
		yy = timestamp[6:10]
		ss = timestamp[11:13]
		minm = timestamp[14:16]
		hh = timestamp[17:19]

		#2019-02-09 11:17:13
		new_timestamp = yy+"-"+mm+"-"+dd+" "+hh+":"+minm+":"+ss
		print("\n\n\n\n\n", new_timestamp)

		try:
			new_post.timestamp = new_timestamp
			new_post.save()

		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)	

		return Response(status=status.HTTP_201_CREATED)

	
				

				

