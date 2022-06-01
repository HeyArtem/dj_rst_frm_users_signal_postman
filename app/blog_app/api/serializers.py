from blog_app.models import(
    BlogPost,
    Category,
    Tag
)
from rest_framework import fields, serializers


class BlogPostCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"
        
        
class BlogPostTagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = "__all__"
        

# от Макса для создания поста
class BlogPostSerializer(serializers.ModelSerializer):
    # category = BlogPostCategorySerializer
    # tag = BlogPostTagSerializer(many=True)
    
    class Meta:
        model = BlogPost
        fields = "__all__"    
        
# просмотр всех постов
class BlogPostListSerializer(serializers.ModelSerializer):
    category = BlogPostCategorySerializer()
    tag = BlogPostTagSerializer(many=True)
    
    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "img",
            "category",
            "tag",
            "updated_at"
        ]
        

# работа с отдельным постом (редактирование, просмотр, удаление)
class BlogPostDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlogPost
        fields = "__all__"



