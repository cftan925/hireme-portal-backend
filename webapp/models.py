from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# https://github.com/veryacademy/YT-Django-Theory-Create-Custom-User-Models-Admin-Testing/blob/master/users/models.py
# class CustomAccountManager(BaseUserManager):

#     def create_superuser(self, name, contact, email, password, is_freelancer, created_date, updated_date, **other_fields):

#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_active', True)

#         if other_fields.get('is_staff') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_staff=True.')
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_superuser=True.')

#         return self.create_user(name=name, contact=contact, email=email, is_freelancer=is_freelancer, created_date=created_date, updated_date=updated_date, **other_fields)


#     def create_user(self, name, contact, email, password, is_freelancer, created_date, updated_date, **other_fields):

#         if not email:
#             raise ValueError(_('You must provide an email address'))

#         user = self.model(name=name, contact=contact, email=self.normalize_email(email), is_freelancer=is_freelancer, created_date=created_date, updated_date=updated_date, **other_fields)
#         user.set_password(password)
#         user.save()
#         return user


# class User(AbstractBaseUser, PermissionsMixin):

#     name = models.CharField(max_length=200)
#     contact = models.CharField(max_length=200)
#     email = models.EmailField(max_length=200, unique=True)
#     password = models.CharField(max_length=200)
#     is_freelancer = models.BooleanField()
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)

#     #about = models.TextField(_(
#     #    'about'), max_length=500, blank=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)

#     objects = CustomAccountManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name', 'contact', 'password', 'is_freelancer', 'created_date']

#     def __str__(self):
#         return self.name
 
def upload_path_profile(instance, filename):
  return '/'.join(['profileImages', filename])
# >>> u = User.objects.get(username='fsmith')
# >>> freds_department = u.employee.department

def profile_upload_path(instance, filename):
  return '/'.join(['profileImages', filename])

# When creating a new user, need to create User object and Profile object
class Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  #name = models.CharField(max_length=200)
  contact = models.CharField(max_length=200, null=True)
  #email = models.EmailField(max_length=200)
  #password = models.CharField(max_length=200)
  is_freelancer = models.BooleanField(null=True)
  profile_image = models.ImageField(upload_to=profile_upload_path, null=True)
  #created_date = models.DateTimeField(auto_now_add=True)
  #updated_date = models.DateTimeField(auto_now=True)
  
  class Meta:
    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'

  def __str__(self):
    return self.user.username

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       #profile, created = Profile.objects.get_or_create(user=instance)
       Profile.objects.create(user=instance)
       Profile.is_freelancer = False  

post_save.connect(create_user_profile, sender=User) 

class Freelancer(models.Model): 
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  skillset = models.CharField(max_length=300, default='')
  introduction = models.CharField(max_length=500, null=True, default='')
  linkedin_url = models.CharField(max_length=200, null=True, default='')
  facebook_url = models.CharField(max_length=200, null=True, default='')
  github_url = models.CharField(max_length=200, null=True, default='')
  
  class Meta:
    verbose_name = 'Freelancer'
    verbose_name_plural = 'Freelancers'

  def __str__(self):
    return self.profile.user.username

class Chat(models.Model):
  from_userID = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_userID')
  to_userID = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='to_userID')
  message = models.CharField(max_length=200)
  created_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name = 'Chat'
    verbose_name_plural = 'Chats'
  
  def __str__(self):
    return self.message

def upload_path(instance, filename):
  return '/'.join(['serviceImages', filename])

class Service(models.Model):
  freelancerID = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  description = models.TextField()
  image = models.ImageField(upload_to=upload_path)
  price = models.FloatField()
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = 'Service'
    verbose_name_plural = 'Services'
  
  def __str__(self):
    return self.title

class Booking(models.Model):
  # (actual value to be set on the model, the human-readable name)
  #STATUS = (('Example','Example'))
  userID = models.ForeignKey(Profile, on_delete=models.CASCADE)
  serviceID = models.ForeignKey(Service, on_delete=models.CASCADE)
  rating = models.IntegerField(null=True)
  review = models.CharField(max_length=200, null=True)
  #status = models.CharField(max_length=200, choices=STATUS)
  remark = models.TextField()
  status = models.CharField(max_length=200)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = 'Booking'
    verbose_name_plural = 'Bookings'
  
  def __str__(self):
    return f'{self.pk} { self.serviceID.freelancerID.pk } {self.remark}'

class Notification(models.Model):
  #(actual value to be set on the model, the human-readable name) 
  #STATUS = (('Example','Example'))
  booking_ID = models.ForeignKey(Booking, on_delete=models.CASCADE)
  to_userID = models.ForeignKey(Profile, on_delete=models.CASCADE)
  message = models.CharField(max_length=200)
  created_date = models.DateTimeField(auto_now_add=True)
  #status = models.CharField(max_length=200, choices=STATUS)
  status = models.CharField(max_length=200)
  class Meta:
    verbose_name = 'Notification'
    verbose_name_plural = 'Notifications'
  
  def __str__(self):
    return self.message

