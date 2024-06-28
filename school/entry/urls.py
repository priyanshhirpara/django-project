from django.urls import path
from entry.views import EntryView,CompetitionViewAll,EntryViewAll

urlpatterns = [
    path('entry/', EntryView.as_view(),name='add-entry'),
    path('entry/<int:pk>/',EntryView.as_view(),name='entry-detail'),
    path('entry/competition/',CompetitionViewAll.as_view(),name='get-detail'),
    path('entry/',EntryViewAll.as_view(),name='entry-detail')
]