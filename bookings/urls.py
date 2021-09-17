from django.urls import path
from bookings.views import BookingHistoryView, ReserveView

urlpatterns = [
    path('/history', BookingHistoryView.as_view()),
    path('', ReserveView.as_view())
]