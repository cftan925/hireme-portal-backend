from django.urls import path, include
from . import views
from .views import WebAppListView, ServiceListView, MyServiceListView, ClientRequestListView, MyRequestListView, ProfileListView, FreelancerListView, PreviousProjectsListView, UserListView, UserViewSet, PreviousBookingsListView, NotificationListView, NewNotificationListView, ServiceDetailListView, BookServiceListView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register', UserViewSet, obtain_auth_token)


urlpatterns = [
  path('api/', include(router.urls)),
  path('', WebAppListView.as_view()),
  path('create-service/', ServiceListView.as_view()),
  path('my-service/', MyServiceListView.as_view()),
  path('client-request/', ClientRequestListView.as_view()),
  path('my-request/', MyRequestListView.as_view()),
  path('service-detail/', ServiceDetailListView.as_view()),
  path('book-service/', BookServiceListView.as_view()),
  path('serviceListing/', ServiceListView.as_view()),
  path('profile/', ProfileListView.as_view()),
  path('freelancer/', FreelancerListView.as_view()),
  path('previousprojects/', PreviousProjectsListView.as_view()),
  path('previousbookings/', PreviousBookingsListView.as_view()),
  path('user/', UserListView.as_view()),
  path('notification/', NotificationListView.as_view()),
  path('new-notification/', NewNotificationListView.as_view()),
  path('auth/', obtain_auth_token)
]