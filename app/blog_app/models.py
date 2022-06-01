import datetime
from django.db import models


def blog_img_directory_img_path(instance, filename):
    today = datetime.datetime.today()
    filename = "{}.{}".format(instance.title, filename.split('.')[-1])
    
    return "blog/{}/{}/{}/{}".format(
        today.year,
        today.month,
        today.day,
        filename
    )
    

class Category(models.Model):
    title = models.CharField(verbose_name="Blog Post Category", max_length=30)
    
    class Meta:
        verbose_name = "Blog Post Category"
        verbose_name_plural = "Blog Post Categories"
        
    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    title = models.CharField(verbose_name="Tag", max_length=50)
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        
    def __str__(self) -> str:
        return self.title


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published")
    )
    
    title = models.CharField(verbose_name="Title", max_length=300)
    category = models.ForeignKey(
        Category, 
        verbose_name="Category", 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="posts_by_category"  # related_name - могу получить все посты по категории
    )
    img = models.ImageField(upload_to=blog_img_directory_img_path)
    content = models.TextField(verbose_name="Post content")
    tag = models.ManyToManyField(Tag, verbose_name="Tag", blank=True)
    created_at = models.DateTimeField(verbose_name="Date of create", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date of Updated", auto_now=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default="draft",
        max_length=50
    )
    
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Post`s"
        
    def __str__(self):
        return self.title
