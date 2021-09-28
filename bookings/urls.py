from django.urls import path
from bookings.views import ReserveView, BookingHistoryView

urlpatterns = [
    path('', ReserveView.as_view()),
    path('/histories', BookingHistoryView.as_view())
]