from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add_data/', views.add_new_data, name='add_data'),
    path('product/<int:product_id>/payment/', views.payment_view, name='payment'),
    path('product/<int:product_id>/comment/', views.add_comment_view, name='add_comment'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]