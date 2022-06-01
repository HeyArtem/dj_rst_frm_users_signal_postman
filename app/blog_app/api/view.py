from blog_app.models import BlogPost
from blog_app.api.serializers import(
    BlogPostListSerializer,
    BlogPostSerializer,
    BlogPostDetailSerializer
)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


# создание поста
class BlogPostCreateAPIView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


# просмотр всех постов
class BlogPostListAPIView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(status="published")
    serializer_class = BlogPostListSerializer
    
    
# детальный вывод поста
class BlogPostDetailAPIView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostDetailSerializer
    permission_classes = [IsAuthenticated]
    

# class BlogPostDetailAPIView(generics.DestroyAPIView):
#     queryset = BlogPost.objects.all()
#     serializer_class = BlogPostDetailSerializer
    