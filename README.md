-Создал проект app с возможностью создавать посты и загружать картинки из html формы
-так же приложение users_app и скрипт сигнала от от пользователя, который создает профайл
-создавал полльователей через postman

***********************************
Тестирование через Postman:
оПрежде чем начать работать с Postman, нужно прописать настройки в settings.py, пути в urls.py

настройки в settings.py:
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users_app.User'

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework.authentication.TokenAuthentication',
		# 'rest_framework.authentication.BasicAuthentication',
		# 'rest_framework_simplejwt.authentication.JWTAuthentication', # работы с jwt
	),
}

SIMPLE_JWT = {
	# 'AUTH_HEADER_TYPES': ('JWT',),
	'AUTH_HEADER_TYPES': ('Bearer',),
	# 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
	# 'REFRESH_TOKEN_LIFETIME': timedelta(days=1)
}


настройки в urls.py:
urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include("blog_app.api.urls")),
	path('api/auth/', include('djoser.urls')),
	path('api/auth/', include('djoser.urls.authtoken')), # для аутентификации
	# path('api/auth/', include('djoser.urls.jwt')), # для работы с jwt 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


djoser-позволяет использовать токены для авторизации пользователя

открываю postman и документацию с эндпоинтами
https://djoser.readthedocs.io/en/latest/base_endpoints.html

создаю пользователя:
	http://127.0.0.1:8000/api/auth/users/
в postman сoздаю новую вкладку:
	POST — Body - form-data
	username — user1 (имя пользователя user1)
	email - user1@gmail.com (email пользователя user1@gmail.com)
	password = user1USER1  (пароль пользователя)
		→Send

	создался пользователь
	{
		"email": "user1@gmail.com",
		"username": "user1",
		"id": 2
	}

сгенерирую обычный токен ( с помощью токена идет аутонтификация на сайте):
https://djoser.readthedocs.io/en/latest/token_endpoints.html
в postman сoздаю новую вкладку:
	POST
	http://127.0.0.1:8000/api/auth/token/login/
	Body - form-data
	username — user1
	email - user1@gmail.com #можно без мыла
	password - user1USER1
		→Send

создаю несколько постов в админке, буду тестировать аутентификацию, поэтому на вьюхе на детльный просмотр у меня стоит
	# детальный вывод поста
	class GirlsDetailView(generics.RetrieveAPIView):
		queryset = Girls.objects.all() 
		serializer_class = GirlsDetailSerializer
		permission_classes = (IsAuthenticated, )

в postman сoздаю новую вкладку (т. к. я прописал пермишены на детальный пост, то здесь я должен вписать token):
в postman сoздаю новую вкладку:
	GET 
	http://127.0.0.1:8000/api/detail/1/

Headers
Postman-Token  <calculated when request is sent>
Host  <calculated when request is sent>
User-Agent  PostmanRuntime/7.29.0
Accept   */*
Accept-Encoding  gzip, deflate, br
Connection  keep-alive
Authorization  token 8d47891b401e9e57d430937131b5c3549396cf1c
	
		→Send
Ответ:
{
"id": 1,
"title": "Post 1",
"img": "http://127.0.0.1:8000/media/blog/2022/5/26/Post_1.jpg",
"content": "Post content Post 1",
"created_at": "2022-05-26T11:25:53.455012Z",
"updated_at": "2022-05-26T11:25:53.455038Z",
"status": "published",
"category": 1,
"tag": [
1
]
}

!!! если бы у меня не были прописаны (permission_classes = [IsAuthenticated]
), то token не нужен!!!
	

что бы разлогинится:
в postman сoздаю новую вкладку:
	POST
	http://127.0.0.1:8000/api/auth/token/logout/
	headers
Postman-Token  <calculated when request is sent>
Content-Length  0
Host  <calculated when request is sent>
User-Agent  PostmanRuntime/7.29.0
Accept  */*
Accept-Encoding  gzip, deflate, br
Connection  keep-alive
Authorization  Token 8d47891b401e9e57d430937131b5c3549396cf1c
		
		→Send


кто я (токен получил новый, т. к. старый разлогигил):
	GET
	http://127.0.0.1:8000/api/auth/users/me/
	headers
	Autorization — token 8c3998e467dc35b89d69b7c95c2ab57ff661de42				→Send

J

WT
JWT это более продвинутый уровень, в нем есть две пары access & refresh (
  access — используется для доступа к информации на сайте
  refresh — используется для обновления access token)

*Для этого, во view.py моих постов, должны должны быть прописаны permissions:
from rest_framework.permissions import IsAuthenticated

# детальный вывод поста
class BlogPostDetailAPIView(generics.RetrieveAPIView):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostDetailSerializer
	permission_classes = [IsAuthenticated]


*а в url должен быть прописан путь:
urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include("blog_app.api.urls")),
	path('api/auth/', include('djoser.urls')),
	# path('api/auth/', include('djoser.urls.authtoken')), # для аутентификации joser
	path('api/auth/', include('djoser.urls.jwt')), # для работы с jwt 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

*в settings:
REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		# 'rest_framework.authentication.TokenAuthentication', # для работы joser обычные токены которые будут записываться в базу данных
		# 'rest_framework.authentication.BasicAuthentication',
		'rest_framework_simplejwt.authentication.JWTAuthentication', # работы с jwt
	),
}

SIMPLE_JWT = {
	# 'AUTH_HEADER_TYPES': ('JWT',), # это по дефолту
	'AUTH_HEADER_TYPES': ('Bearer',), # за место 'Bearer'может быть и другое слово, я его буду прописывать при работе с JWT, в строке Authorization, прописываю за место слова token 
	# 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1), #время жизни ACCESS token
	# 'REFRESH_TOKEN_LIFETIME': timedelta(days=1) #время жизни REFRESH token
}

получаю refresh & access:
POST
	http://127.0.0.1:8000/api/auth/jwt/create/

	body
	username  user_fr_pst_2
	password  123_User_2
		→Send

Ответ:
{
"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1Mzk0NjY5OCwianRpIjoiOGUwOTI2Y2VkOGY0NDFiMjg1ZWUzYjA2NTIxMDAxMDEiLCJ1c2VyX2lkIjo3fQ.k7JJvM9Fd_CkRPYqf32Dy9mcYAgPBjjewg8uAjgEprc",
"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzODYwNTk4LCJqdGkiOiI4ZWMzODc1NWU5NjY0YWNkYmY5ZDIxYWJiMTE5MTczNSIsInVzZXJfaWQiOjd9.p2B1WUBBz2vNAB5NqgzeAhV5Dq9KAtEL0-D1zj8EzEk"
}


детальный просмотр с JWT token:
GET
	http://127.0.0.1:8000/api/detail/1/

	headers
	Postman-Token   <calculated when request is sent>
	Host   <calculated when request is sent>
	User-Agent   PostmanRuntime/7.29.0
	Accept   */*
	Accept-Encoding   gzip, deflate, br
	Connection   keep-alive
	Authorization  Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzODYyNjA0LCJqdGkiOiI1NjhlMTBmODExMDI0ZmM0YWU2Y2Y4M2JhYzM3NWQzZCIsInVzZXJfaWQiOjd9.0izSl9WTE6bfuyLU2c7yS-FohM1qMen96CIpBNNBH5c
		→Send

Ответ:
{
"id": 1,
"title": "Post 1",
"img": "http://127.0.0.1:8000/media/blog/2022/5/26/Post_1.jpg",
"content": "Post content Post 1",
"created_at": "2022-05-26T11:25:53.455012Z",
"updated_at": "2022-05-26T11:25:53.455038Z",
"status": "published",
"category": 1,
"tag": [
1
]
}


обновление access JWT token = Refresh (в body прописываю код из refresh):
POST
	http://127.0.0.1:8000/api/auth/jwt/refresh/
body
refresh  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1Mzk0ODcwNCwianRpIjoiMWJjY2M4OTM2ZDYzNDNmNWFhZTU0ZDQ5OTNlNjhjZGUiLCJ1c2VyX2lkIjo3fQ.x5tTiPxMe-MZxtw6WZm34DxkkbnflzGHcfJCUUHYAeA

Ответ (на выходе получаем новый access token):
{
"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzODY1ODA1LCJqdGkiOiJkNDJiZTM3ZDg3MjM0YTNiYWI4NWFjOTliMWMyNGNiMyIsInVzZXJfaWQiOjd9.iUB1ucZ_iGyuDP0aDC7iK9HuvVcXMgTJZcmjBP5MH1o"
}

