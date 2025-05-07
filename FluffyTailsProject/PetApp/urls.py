from django.urls import path
from . import views

urlpatterns = [

    path('',views.dashboard1_view,name='dashboard1'),
    path('index',views.index_view,name='index'),
    path('home/', views.home_view, name='home'),
    path('learn2/',views.learn2,name='learn2'),
    path('learn3/',views.learn3,name='learn3'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('view-profile/', views.view_profile, name='view_profile'),
    path('view-profile_admin/', views.view_profile_admin, name='view_profile_admin'),
    


    path('addbreed/', views.add_breed_view, name='addbreed'),
    path('breed/<int:breed_id>/pets/', views.breed_pet_list_view, name='breed_pet_list'),
    path('breed/<int:breed_id>/delete/', views.delete_breed_view, name='delete_breed'),
    path('breed/<int:breed_id>/update/', views.update_breed_view, name='update_breed'),
  

    path('registerpet/', views.register_pet_view, name='registerpet'),


    path('dogs/', views.dogs_view, name='dogs'),
    path('cats/', views.cats_view, name='cats'),

    path('add-to-cart/<int:pet_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pet_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('adopt/', views.adopt_pets, name='adopt_pets'),

    path('about-us/', views.aboutus, name='aboutus'),
    path('about-us2/', views.aboutus2, name='aboutus2'),  # or aboutus
    path('adopting-pets/', views.adopting_pets, name='adoptingpets'),
    path('foundation/', views.foundation, name='foundation'),
    path('dog-adoption/', views.dog_puppies_adoption, name='dogPuppiesAdoption'),
    path('dog-behavior/', views.behavior_dog, name='behaviordog'),
    path('cat-adoption/', views.cat_kitten_adoption, name='catKittenAdoption'),
    path('cat-behavior/', views.behavior_cat, name='behaviorcat'),
    # path('contact/', views.contact_view, name='contact'),

    path('cart/adopt/', views.adopt_pets, name='adopt_pets'),
    path('orders/', views.orders_view, name='orders'),


    path('orders/accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('orders/reject/<int:order_id>/', views.reject_order, name='reject_order'),

    path('contactus/', views.contact_view, name='contactus'),
    path('view-messages/', views.view_messages, name='view_messages'),
]