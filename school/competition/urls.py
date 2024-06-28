from django.urls import path
from competition.views import CompetitionViews
from competition.views import CompetitionViewAll

urlpatterns = [
    path('competition/', CompetitionViews.as_view(),name='add-competition'),
    path('competition-view/<int:pk>/',CompetitionViews.as_view(),name='competition-detail'),
    path('competition-view/',CompetitionViewAll.as_view(),name="all-competition")
]