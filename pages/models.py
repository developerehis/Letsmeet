from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, blank=True,null=True,on_delete=models.CASCADE)
    first = models.CharField(max_length=200,blank=True,null=True,)
    last = models.CharField(max_length=200,blank=True,null=True,)
    photo = models.ImageField(default='user.png', upload_to='photos/%y/%m', blank=True,null=True)
    friends = models.ManyToManyField('self',blank=True)
    speaks = models.CharField(max_length=200,blank=True,null=True)
    is_learning =  models.CharField(max_length=200, blank=True,null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("pages:profile", kwargs={"profile_id": self.pk})
    

    class Meta:
        ordering = ['-id']

def create_profile(sender,instance,created,**kwargs):

    if created:
        Profile.objects.create(user=instance)
        print('Profile created successfully')

post_save.connect(create_profile,sender=User)