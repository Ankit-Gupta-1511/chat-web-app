from django.db import models

class User(models.Model):
    username = models.CharField(max_length = 20)
    pub_date = models.DateTimeField(auto_now_add=True)

class Input(models.Model):
    msg = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    

class Response(models.Model):
    input_msg = models.ForeignKey(Input, on_delete=models.CASCADE)
    response = models.CharField(max_length=200)

class Query(models.Model):
    email = models.EmailField()
    query = models.CharField(max_length = 400)
