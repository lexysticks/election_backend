# views.py

from rest_framework import generics, filters, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from .models import Candidate, PartyVoteCount, Vote
from .serializers import CandidateSerializer, PartyVoteCountSerializer, VoteSerializer



class CandidateListView(generics.ListAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.AllowAny]  
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'party']
    ordering_fields = ['name', 'age']
    ordering = ['name'] 

    def get_queryset(self):
        election_type = self.kwargs.get('election_type')
        cache_key = f"candidates_{election_type}_{self.request.GET.urlencode()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        queryset = Candidate.objects.filter(election_type=election_type).only(
            'name', 'party', 'age', 'party_image', 'image'
        )
        cache.set(cache_key, queryset, timeout=3600)  
        return queryset



class PartyVoteCountListView(generics.ListAPIView):
    serializer_class = PartyVoteCountSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['party']
    ordering_fields = ['vote_count']
    ordering = ['-vote_count']  

    def get_queryset(self):
        election_type = self.kwargs.get('election_type')
        cache_key = f"party_votes_{election_type}_{self.request.GET.urlencode()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        queryset = PartyVoteCount.objects.filter(election_type=election_type)
        cache.set(cache_key, queryset, timeout=3600)  
        return queryset



class CastVoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        candidate_id = request.data.get("candidate")
        user = request.user

        if not candidate_id:
            return Response({"error": "Candidate ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)

        election_type = candidate.election_type
        if Vote.objects.filter(user=user, candidate__election_type=election_type).exists():
            return Response({"error": "You have already voted in this election."}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(user=user, candidate=candidate)
        serializer = CandidateSerializer(candidate, context={"request": request})

        # Clear cache after vote
        cache.delete_pattern(f"candidates_{election_type}_*")
        cache.delete_pattern(f"party_votes_{election_type}_*")

        return Response({
            "message": "Vote submitted successfully!",
            "candidate": serializer.data
        }, status=status.HTTP_201_CREATED)
