from django.urls import path
from . import views


app_name = 'socialmedia'

    
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
	#homepage

    path('<pk>/', views.DetailView.as_view(), name = 'detail'),

    path('post/add/', views.PostCreate.as_view(), name = 'add-post'),

    path('user/register/', views.UserFormView.as_view(), name = 'register'),

    #path('post//', views.PostCreate.as_view(), name = 'add-post'),

    #path('post/add/', views.PostCreate.as_view(), name = 'add-post'),

    #1. add users
    path('api/v1/users/', views.UserCreate.as_view(), name = 'add-user'),
    path('api/v1/users/<username>/', views.UserDelete.as_view(), name = 'remove-user'),


    path('api/v1/categories/', views.ListAddActsCategories.as_view(), name = 'list-add-acts'),
    path('api/v1/categories/<actType>/', views.DeleteActsCategories.as_view(), name = 'delete-acts'),

    path('api/v1/categories/<actType>/acts/', views.ListPostAct.as_view(), name = 'list-posts-for-act'),
    path('api/v1/categories/<actType>/acts/size/', views.ListPostsSize.as_view(), name = 'list-posts-size'),
    path('api/v1/categories/<actType>/acts?start=<startRange>&end=<endRange>/', views.ListPostRange.as_view(), name = 'list-posts-in-range'),

    path('api/v1/acts/upvote/', views.UpvotePost.as_view(), name = 'upvote-post'),

	path('api/v1/acts/<actID>/', views.RemovePost.as_view(), name = 'delete-post'),

    path('api/v1/acts/', views.AddPost.as_view(), name = 'upload-post'),    

	#6. List acts for a given category (when total #acts is less than 500)
	

	

	
]	