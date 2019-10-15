from django.urls import path

from . import views

urlpatterns = [
    path('objects', views.ObjectsView.as_view(), name='objects_view'),
    path('test', views.TestPage.as_view(), name='test'),
    path('reservations/property/<pid>', views.SmartHotelView.as_view(), name='smart_hotel_view_dash'),
    path('objects/<iid>/publishers/<oid>/events/<eid>', views.EventHandler.as_view(), name='event_handler'),
]