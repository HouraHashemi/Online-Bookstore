
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  
    path('book_list_have_access/', views.book_list_have_access, name='book_list_have_access'),  
    path('logout/', views.logout_view, name='logout'),  
    path('search/', views.search_books, name='search_books'),

    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),

    path('view-cart/', views.view_cart, name='view_cart'),
    # path('submit-order/', views.submit_order, name='submit_order'),

    path('order-submission/', views.order_submission, name='order_submission'),
    path('submit-final-order/', views.submit_final_order, name='submit_final_order'),
   
    path('view-orders/', views.view_orders, name='view_orders'),
    # path('books/<int:book_id>/', views.book_detail, name='book_detail'),

    path("__debug__/", include("debug_toolbar.urls")),

]
