from django.urls import path
from .views import ContentView, FilterContentView, OneContentView

urlpatterns = [
    path('contents/', ContentView.as_view()),
    path('contents/<int:content_id>/', OneContentView.as_view()),
    path('contents/filter/', FilterContentView.as_view()),
]