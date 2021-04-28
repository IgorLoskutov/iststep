from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length = 128)
    tagline = models.TextField()

    def __str__(self):
        return self.name



class Author(models.Model):
    name = models.CharField(max_length = 64)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.title
