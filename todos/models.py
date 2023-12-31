from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Todo(models.Model):
    title = models.CharField(validators=[MinLengthValidator(4)], max_length=64)
    description = models.TextField(max_length=256)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name="todos", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created']


