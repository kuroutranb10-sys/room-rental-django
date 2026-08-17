from django.urls import path
from . import views
from .views import (
    login_view,
    logout_view,
)

urlpatterns = [

        path(
            '',
            views.room_list,
            name='room_list'
        ),

        path(
            'add/',
            views.add_room,
            name='add_room'
        ),

        path(
            'edit/<int:room_id>/',
            views.edit_room,
            name='edit_room'
        ),

        path(
            'delete/<int:room_id>/',
            views.delete_room,
            name='delete_room'
        ),


        path(
            'api/wards/',
            views.get_wards,
            name='get_wards'
        ),

        path(
            'detail/<int:room_id>/',
            views.room_detail,
            name='room_detail'
        ),

        path(
            'rooms/<int:room_id>/image/<int:image_id>/delete/',
            views.delete_room_image,
            name='delete_room_image'
        ),

        path(
            'dashboard/',
            views.dashboard,
            name='dashboard'
        ),

        path(
            'login/',
            login_view,
            name='login'
        ),

        path(
            'logout/',
            logout_view,
            name='logout'
        ),

    ]