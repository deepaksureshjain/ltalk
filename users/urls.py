from .views import UserRegister,SignIn,logout,EditProfile,MyAccount
from django.urls import path
urlpatterns = [
    path('register/', UserRegister.as_view(), name="register"),
    path('login/', SignIn.as_view(), name="login"),
    path('logout/', logout, name="logout"),
    path('editprofile/', EditProfile.as_view(), name="profileEdit"),
    path('myaccount/', MyAccount.as_view(), name="myaccount")
]
