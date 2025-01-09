from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Tag(models.Model):    
    caption = models.CharField(max_length=15, unique=True)  
     
    def __str__(self):
        return f"{self.caption}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return f"{self.name}"   


class Project(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="projects")
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to="images")
    slug = models.SlugField(default="", null=False)
    tags = models.ManyToManyField(Tag, related_name="projects")
    gh_link = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
     user_name = models.CharField(max_length=120) 
     user_email = models.EmailField() 
     text = RichTextField()
     date = models.DateField(auto_now=True)
     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comments")

     def __str__(self):
        return f"{self.text}"
    

class CV(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="images") 
    uploaded_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.title}"
    

class Course(models.Model):
    title = models.CharField(max_length=100)    
    start = models.DateField()
    finish = models.DateField()

    def __str__(self):
        return f"{self.title}"
    
    
class Education(models.Model):
    title = models.CharField(max_length=100)    
    start = models.DateField()
    finish = models.DateField()
    specializaion = models.CharField(max_length=100)  