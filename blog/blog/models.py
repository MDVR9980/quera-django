from django.db import models
from django.utils import timezone
from copy import deepcopy

class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def copy(self):
        """
        Create a full copy of this BlogPost including all related Comment objects.
        The copy will have:
        - new id
        - date_created set to now
        - same title, body, and author
        - all related comments copied as new Comment instances linked to the new post
        Returns the id of the newly created BlogPost.
        """
        
        post_copy = BlogPost(
            title=self.title,
            body=self.body,
            author=self.author,
            date_created=timezone.now()
        )
        post_copy.save()  

        for comment in self.comments.all():
            Comment.objects.create(
                blog_post=post_copy,
                text=comment.text
            )

        return post_copy.id

class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text[:50]