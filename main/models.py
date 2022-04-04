from django.db import models
from account.models import User
from django.urls import reverse

class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories', blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return self.name

    @property
    def get_children(self):
        if self.children:
            return self.children.all()
        return False

class Apartment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='apartments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apartments')
    created = models.DateTimeField()

    def __str__(self):
        return self.title

    @property
    def get_image(self):
        return self.images.first()

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

class Image(models.Model):
    image = models.ImageField(upload_to='apartments')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url



