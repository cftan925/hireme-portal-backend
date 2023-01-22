import json
from django.http import HttpResponse
from django.shortcuts import render
from config import settings 
from rest_framework.generics import ListAPIView
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from .models import Service, Freelancer, Booking, Notification, Profile
from .serializers import FreelancerSerializer, ProfileSerializer, ServiceSerializer, UserSerializer

from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

class WebAppListView(ListAPIView):
  permission_classes = (permissions.AllowAny, )
  queryset = Service.objects.all()
  serializer_class = ServiceSerializer
  pagination_class = None

class ServiceDetailListView(ListAPIView):
  def get(self, request):
    
    service = Service.objects.get(title=request.GET['title'])
    freelancerUser = User.objects.get(pk=service.freelancerID.profile.user.pk)
        
    serviceDetail={
     "service_id":service.pk,
     "service_title":service.title,
      "service_description":service.description,
      "service_price": service.price,
      "service_image": settings.API_URL + service.image.url,
      "freelancer_username": service.freelancerID.profile.user.username,
      "freelancer_firstname": service.freelancerID.profile.user.first_name,
      "freelancer_lastname": service.freelancerID.profile.user.last_name,
    }
    
    return HttpResponse(json.dumps(serviceDetail)) 
  
class BookServiceListView(ListAPIView):
  permission_classes = (IsAuthenticated, )
  authentication_classes = (TokenAuthentication,)
  def post(self, request, *args, **kwargs):
    #booking = booking.objects.get(pk=request.data[''])
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = user_id
    serviceID = request.data["serviceID"]
    serviceRemark = request.data['serviceRemark']
    serviceStatus = "Pending"
    ServiceCreatedDate = datetime.now()
    serviceRating = 5

    Booking.objects.create(
        serviceID_id=serviceID,
        remark=serviceRemark, 
        status=serviceStatus,
        created_date=ServiceCreatedDate,
        userID_id = user, #######################user login ID
        rating = serviceRating ##############nullable
    )
    return HttpResponse({"status": 'Success'}) 


class ProfileListView(ListAPIView):
  permission_classes = (permissions.AllowAny, )
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer
  pagination_class = None

  def put(self, request, *args, **kwargs):
    print(request.data)

    user_id = User.objects.get(username=(request.GET["username"]))
    profile = Profile.objects.get(user_id = user_id)
    profile.contact = (request.data["contact"])
    profile.profile_image = (request.data["profile_image"])
    profile.is_freelancer = (request.data["is_freelancer"])
    # Profile.objects.aupdate(profile_image = profile.profile_image)

    profile.save()

    return HttpResponse({"status": 'Success'}) 

class FreelancerListView(ListAPIView):
  permission_classes = (IsAuthenticated, )
  authentication_classes = (TokenAuthentication,)
  serializer_class = FreelancerSerializer
  pagination_class = None

  # def get(self, request):
  #   # queryset = Freelancer.objects.all().filter(id=request.GET["id"])
  #   username = [Freelancer.profile.user.id for Freelancer.profile.user in Freelancer.objects.all().filter(pk=request.GET["id"])]
  #   return Response(username)
    
  def get(self, request):
    # user = User.objects.get(pk=request.GET["id"])
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = User.objects.get(id=user_id)
    freelancers = Freelancer.objects.all().filter(profile__user=user) 
    freelancer_list = [ 
      {"username": freelancer.profile.user.username,
      "first_name": freelancer.profile.user.first_name,
      "last_name": freelancer.profile.user.last_name,
      "email": freelancer.profile.user.email, 
      "contact": freelancer.profile.contact,
      "is_freelancer": freelancer.profile.is_freelancer,
      "profile_image": settings.API_URL + freelancer.profile.profile_image.url,
      "linkedin_url": freelancer.linkedin_url,
      "facebook_url": freelancer.facebook_url,
      "github_url": freelancer.github_url,
      "skillset": freelancer.skillset,
      "introduction": freelancer.introduction,
      "user_id": freelancer.profile.user.id,} 
      for freelancer in freelancers
    ]
    return HttpResponse(json.dumps(freelancer_list))

  @csrf_exempt 
  def post(self, request, *args, **kwargs):
    
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user_id = user)

    Freelancer.objects.create(
        profile=profile,
        skillset=request.data['skillset'],
        linkedin_url=request.data['linkedin_url'],
        facebook_url=request.data['facebook_url'],
        github_url=request.data['github_url'],
    )
    return HttpResponse({"status": 'Success'})

  def put(self, request, *args, **kwargs):
    print(request.data)

    user_id = Token.objects.get(key=request.auth.key).user_id
    user = User.objects.get(id=user_id)
    freelancer = Freelancer.objects.get(profile__user=user) 
    freelancer.skillset = (request.data["skillset"])
    freelancer.linkedin_url = (request.data["linkedin_url"])
    freelancer.facebook_url = (request.data["facebook_url"])
    freelancer.github_url = (request.data["github_url"])
    # Profile.objects.aupdate(profile_image = profile.profile_image)

    freelancer.save()

    return HttpResponse({"status": 'Success'}) 

class PreviousProjectsListView(ListAPIView):
  def get(self, request):
    freelancer = Freelancer.objects.get(profile_id=request.GET["freelancer_user_id"])
    bookings = Booking.objects.all().filter(serviceID__freelancerID=freelancer)
    booking_list = [ 
      {"service": booking.serviceID.title,
      "freelancer": booking.serviceID.freelancerID.profile.user.username,
      "review": booking.review,
      "rating": booking.rating,
      "status": booking.status,
      "price":  booking.serviceID.price,
      "user_id": booking.userID.user.id} 
      for booking in bookings
    ]
    return HttpResponse(json.dumps(booking_list))
  
class PreviousBookingsListView(ListAPIView):
  def get(self, request):
    profile = Profile.objects.get(pk=request.GET["user_id"])
    bookings = Booking.objects.all().filter(userID=profile)
    booking_list = [ 
      {"service": booking.serviceID.title,
      "freelancer": booking.serviceID.freelancerID.profile.user.username,
      "review": booking.review,
      "rating": booking.rating,
      "status": booking.status,
      "price":  booking.serviceID.price,
      "user_id": booking.userID.user.id} 
      for booking in bookings
    ]
    return HttpResponse(json.dumps(booking_list))

class UserListView(ListAPIView):  
  permission_classes = (IsAuthenticated, )
  authentication_classes = (TokenAuthentication,)
  def get(self, request):
    # user = User.objects.get(pk=request.GET["user_id"])
    # user = Token.objects.get(key='token string').user_id
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = User.objects.get(id=user_id)
    profiles = Profile.objects.all().filter(user=user) 
    user_list = [ 
      {"username": profile.user.username,
      "first_name": profile.user.first_name,
      "last_name": profile.user.last_name,
      "email": profile.user.email,
      "contact": profile.contact,
      "is_freelancer": profile.is_freelancer,
      "profile_image": settings.API_URL + profile.profile_image.url,
      "user_id": profile.user.id} 
      for profile in profiles
    ]
    return HttpResponse(json.dumps(user_list))

  def put(self, request, *args, **kwargs):
    print(request.data)

    user_id = Token.objects.get(key=request.auth.key).user_id
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user_id = user)
    user.first_name = (request.data["first_name"])
    user.last_name = (request.data["last_name"])
    user.email = (request.data["email"])
    profile.contact = (request.data["contact"])
    profile.profile_image = (request.data["profile_image"])
    # Profile.objects.aupdate(profile_image = profile.profile_image)
    user.save()
    profile.save()

    return HttpResponse({"status": 'Success'}) 
  

  # def get(self, request, *args, **kwargs):
  #   queryset = Profile.objects.select_related("user").all()
  #   serializer_class = ProfileSerializer
  #   return HttpResponse(json.dumps(queryset)) 

# def home(request):
#   profiles = Profile.objects.all()
#   for profile in profiles:
#     print(profile.contact)

class ServiceListView(ListAPIView):
  permission_classes = (IsAuthenticated, )
  queryset = Service.objects.all()
  serializer_class = ServiceSerializer
  pagination_class = None
  authentication_classes = (TokenAuthentication,)

  @csrf_exempt 
  def post(self, request, *args, **kwargs):
    
    user = User.objects.get(pk=request.data['userID'] )
    freelancer = Freelancer.objects.get(profile__user=user)

    serviceName = request.data['serviceName'] 
    serviceDescription = request.data['serviceDescription'] 
    servicePrice = request.data['servicePrice']
    serviceImage = request.data['serviceImage']

    Service.objects.create(
        freelancerID=freelancer,
        title=serviceName,
        description=serviceDescription,
        price=round( float(servicePrice), 2 ),
        image=serviceImage
    )
    return HttpResponse({"status": 'Success'}) 

class MyServiceListView(ListAPIView):
  permission_classes = (IsAuthenticated, )
  authentication_classes = (TokenAuthentication,)
  def get(self, request, *args, **kwargs):
    # Get related join data
    user_id = Token.objects.get(key=request.auth.key).user_id
    freelancer = User.objects.get(id=user_id)
    services = Service.objects.all().select_related("freelancerID__profile__user").filter(freelancerID__profile__user=freelancer)
    
    # Get query data into respective key-value pair
    myServices = [{"service_id": service.pk, 
                  "freelancer_name": service.freelancerID.profile.user.username, 
                  "service_title": service.title, 
                  "service_description": service.description, 
                  "service_price": service.price,
                  "service_image": settings.API_URL + service.image.url} 
    for service in services]
    
    return HttpResponse(json.dumps(myServices)) 
  
  def put(self, request, *args, **kwargs):

    selectedService = Service.objects.get(pk=request.data["serviceID"])

    selectedService.title = request.data["serviceName"]
    selectedService.description = request.data["serviceDescription"]
    selectedService.price = request.data["servicePrice"]

    # Check whether image need to be update
    if request.data["serviceImage"] != 'null':
      selectedService.image = request.data["serviceImage"]

    selectedService.save()

    return HttpResponse({"status": 'Success'}) 

  def delete(self, request, *args, **kwargs):

    selectedService = Service.objects.get(pk=request.GET["id"])
    selectedService.delete()

    return HttpResponse({"status": 'Success'}) 

class ClientRequestListView(ListAPIView):
  permission_classes = (IsAuthenticated, )
  authentication_classes = (TokenAuthentication,)

  def get(self, request, *args, **kwargs):
    # Get related join data
    user_id = Token.objects.get(key=request.auth.key).user_id
    freelancer = User.objects.get(id=user_id)
    bookings = Booking.objects.all().select_related("serviceID__freelancerID__profile__user").select_related('userID__user').filter(serviceID__freelancerID__profile__user=freelancer)
    
    # Get query data into respective key-value pair
    serviceBooking = [{"booking_id": booking.pk, 
                      "freelancer_id": booking.serviceID.freelancerID.profile.user.pk, 
                      "service_id": booking.serviceID.pk,  
                      "service_title": booking.serviceID.title, 
                      "service_description": booking.serviceID.description, 
                      "service_price": booking.serviceID.price,
                      "service_image": settings.API_URL + booking.serviceID.image.url, 
                      "booking_client": booking.userID.user.username, 
                      "booking_status": booking.status, 
                      "booking_remark": booking.remark} 
    for booking in bookings]
    
    return HttpResponse(json.dumps(serviceBooking)) 
  
  def put(self, request, *args, **kwargs):
    permission_classes = (IsAuthenticated, )
    for selectedBooking in request.data['selected']:
      selected = Booking.objects.get(pk=selectedBooking['booking_id'])
    
      if request.data['action'] == 'accept':
        selected.status = 'Accepted'
      elif request.data['action'] == 'reject':
        selected.status = 'Rejected'
      else:
        selected.status = 'Completed'

      selected.save()
      
      messageToClient = 'Your booking for ' + selected.serviceID.title + ' service have been ' + selected.status.lower() + ' by ' +  selected.serviceID.freelancerID.profile.user.username + '.'
      messageToFreelancer = 'You have ' + selected.status.lower() + ' booking of ' + selected.userID.user.username + ' for your ' + selected.serviceID.title + ' service.'
      
      # Get client profile
      clientUser = User.objects.get(pk=selected.userID.user.pk)
      client = Profile.objects.filter(user=clientUser).first()

      # Get freelancer profile
      freelancerUser = User.objects.get(pk=selected.serviceID.freelancerID.profile.user.pk)
      freelancer = Profile.objects.filter(user=freelancerUser).first()

      # Create Notification for client
      Notification.objects.create(
        booking_ID=selected,
        to_userID=client,
        message=messageToClient,
        status="Unread"  
      )

      # Create Notification for freelancer
      Notification.objects.create(
        booking_ID=selected,
        to_userID=freelancer,
        message=messageToFreelancer,
        status="Unread"  
      )

    return HttpResponse({"status": 'Success'}) 

class MyRequestListView(ListAPIView):
  permission_classes = (IsAuthenticated, )
  authentication_classes = (TokenAuthentication,)

  def get(self, request, *args, **kwargs):
    # Get related join data
    user_id = Token.objects.get(key=request.auth.key).user_id
    client = User.objects.get(id=user_id)
    bookings = Booking.objects.all().select_related("serviceID__freelancerID__profile__user").select_related('userID__user').filter(userID__user=client)
    
    # Get query data into respective key-value pair
    serviceBooking = [{"booking_id": booking.pk, 
                      "freelancer_id": booking.serviceID.freelancerID.profile.user.pk,
                      "freelancer_name": booking.serviceID.freelancerID.profile.user.username, 
                      "service_id": booking.serviceID.pk,  
                      "service_title": booking.serviceID.title, 
                      "service_description": booking.serviceID.description, 
                      "service_price": booking.serviceID.price,
                      "service_image": settings.API_URL + booking.serviceID.image.url, 
                      "booking_client": booking.userID.user.username, 
                      "booking_status": booking.status, 
                      "booking_remark": booking.remark} 
    for booking in bookings]
    
    return HttpResponse(json.dumps(serviceBooking)) 
  
  def put(self, request, *args, **kwargs):

    for selectedBooking in request.data:
      selected = Booking.objects.get(pk=selectedBooking['booking_id'])
      selected.status = 'Cancelled'
      selected.save()

      messageToClient = 'You have cancelled to book for ' + selected.serviceID.title + ' service.'
      messageToFreelancer = selected.userID.user.username + ' have cancelled to book for your ' + selected.serviceID.title + ' service.'
      
      # Get client profile
      clientUser = User.objects.get(pk=selected.userID.user.pk)
      client = Profile.objects.filter(user=clientUser).first()

      # Get freelancer profile
      freelancerUser = User.objects.get(pk=selected.serviceID.freelancerID.profile.user.pk)
      freelancer = Profile.objects.filter(user=freelancerUser).first()

      # Create Notification for client
      Notification.objects.create(
        booking_ID=selected,
        to_userID=client,
        message=messageToClient,
        status="Unread"  
      )

      # Create Notification for freelancer
      Notification.objects.create(
        booking_ID=selected,
        to_userID=freelancer,
        message=messageToFreelancer,
        status="Unread"  
      )

    return HttpResponse({"status": 'Success'}) 

class NotificationListView(ListAPIView):
  permission_classes = (IsAuthenticated, )
  authentication_classes = (TokenAuthentication,)

  def get(self, request, *args, **kwargs):
    # Get related join data
    # user = User.objects.get(pk=request.GET["id"])
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = User.objects.get(id=user_id)
    notifications = Notification.objects.filter(to_userID__user=user).order_by('-created_date')
    
    # Get query data into respective key-value pair
    myNotifications = [{"notification_id": notification.pk,
                      "booking_id": notification.booking_ID.pk, 
                      "to_userId": notification.to_userID.user.pk,
                      "message": notification.message, 
                      "created_date": notification.created_date.isoformat(),  
                      "status": notification.status} 
    for notification in notifications]

    return HttpResponse(json.dumps(myNotifications))

  def put(self, request, *args, **kwargs):
    
    for notication in request.data:
      noti = Notification.objects.get(pk=notication['notification_id'])
      
      if noti.status == 'Unread':
        noti.status = 'Read'
        noti.save()

    return HttpResponse({"status": 'Success'}) 

class NewNotificationListView(ListAPIView):
  permission_classes = (IsAuthenticated, )
  authentication_classes = (TokenAuthentication,)

  def get(self, request, *args, **kwargs):
    # Get related join data
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = User.objects.get(id=user_id)
    notifications = Notification.objects.filter(to_userID__user=user) & Notification.objects.filter(status="Unread")

    # Get query data into respective key-value pair
    newNotifications = [{"notification_id": notification.pk,
                      "booking_id": notification.booking_ID.pk, 
                      "to_userId": notification.to_userID.user.pk,
                      "message": notification.message, 
                      "created_date": notification.created_date.isoformat(),  
                      "status": notification.status} 
    for notification in notifications]

    return HttpResponse(json.dumps(newNotifications))

# User Viewset for Authentication
class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.AllowAny,)


  # @csrf_exempt 
  # def create(self, request, *args, **kwargs):
  #   serializer = self.get_serializer(data=request.data)
  #   serializer.is_valid(raise_exception=True)
  #   self.perform_create(serializer)
  #   headers = self.get_success_headers(serializer.data)
  #   return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

  # def perform_create(self, serializer):
  #   user = serializer.save()
  #   token, created = Token.objects.get_or_create(user=user)
  #   return Response({'token': token.key})
