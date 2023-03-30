from django.urls import path
from . import views

urlpatterns = [
    path('', views.local_host, name='local_host'),
    path('none_of_your_bussiness/', views.none_of_your_bussiness, name='none_of_your_bussiness'),
    path('accounts/login/', views.sign_in, name='sign_in'),
    path('menu/<int:type_id>/', views.view_menu, name='view_menu'),
    path('about/', views.about, name='about'),
    path('<int:emp_id>/', views.home_page, name='home_page'),
    path('<int:emp_id>/sign_out/', views.sign_out, name='sign_out'),
    path('<int:emp_id>/view_order/', views.view_order, name='view_order'),
    path('<int:emp_id>/update_menu/', views.update_menu, name='update_menu'),
    path('<int:emp_id>/item_list/', views.view_item, name='view_item'),
    path('<int:emp_id>/order/', views.new_order, name='new_order'),
    path('<int:emp_id>/order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:emp_id>/order/<int:order_id>/update_items/<int:item_id>/', views.update_items, name='update_items'),
    path('<int:emp_id>/order/<int:order_id>/update_items/<int:item_id>/cancel/', views.cancel, name='cancel'),
    path('<int:emp_id>/order/<int:order_id>/add_item/', views.add_order_item, name='add_order_item'),
    path('<int:emp_id>/order/<int:order_id>/complete/', views.complete_order, name='complete_order'),
]
