
# from django.urls import path
# from .views import CandidateListView, PartyVoteCountListView, CastVoteView

# urlpatterns = [
#     path('candidates/<str:election_type>/', CandidateListView.as_view(), name='candidates-list'),
#     path('party-votes/<str:election_type>/', PartyVoteCountListView.as_view(), name='party-votes-list'),
#     path('cast/', CastVoteView.as_view(), name='cast-vote'),  
# ]
from django.urls import path
from .views import CandidateListView, PartyVoteListView, CastVoteView

urlpatterns = [
    path("candidates/<str:election_type>/", CandidateListView.as_view()),
    path("party-votes/<str:election_type>/", PartyVoteListView.as_view()),
    path("cast/", CastVoteView.as_view()),
]
