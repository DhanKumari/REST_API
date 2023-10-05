from django.urls import path, include
from testapp.views import index, person, login, PersonAPI, PeopleViewSet, RegisterAPI , loginAPI

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PeopleViewSet,basename='people')
urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view()),
    path('login/',loginAPI.as_view(),),
    path('index/',index),
    path('person/',person),
    path('login/',login),
    path('persons-class/',PersonAPI.as_view())

]
