from django.urls import path
from blog_app.api.view import(
    BlogPostCreateAPIView,
    BlogPostListAPIView,
    BlogPostDetailAPIView
)

urlpatterns = [
    path("create-post/", BlogPostCreateAPIView.as_view()),
    path("", BlogPostListAPIView.as_view()),
    path("detail/<int:pk>/", BlogPostDetailAPIView.as_view()),
]