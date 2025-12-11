from django.urls import path
from . import views

urlpatterns = [
    path("candidates/<str:election_type>/", views.get_candidates, name="get_candidates"),
    path("party-votes/<str:election_type>/", views.get_party_votes, name="get_party_votes"),
    path("cast/", views.cast_vote, name="cast_vote"),
]
