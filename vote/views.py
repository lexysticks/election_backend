from rest_framework import generics, filters, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import F

from .models import Candidate, PartyVoteCount, Vote
from .serializers import CandidateSerializer, PartyVoteCountSerializer


# ------------------------
# Candidate List
# ------------------------
class CandidateListView(generics.ListAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'party']
    ordering_fields = ['name', 'age']
    ordering = ['name']

    def list(self, request, *args, **kwargs):
        election_type = self.kwargs.get('election_type', '').lower()
        query_string = request.GET.urlencode()
        cache_key = f"candidates_{election_type}_{query_string}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = Candidate.objects.filter(
            election_type__iexact=election_type
        ).order_by(*self.ordering)

        # Preload PartyVoteCount to reduce DB hits
        party_votes_qs = PartyVoteCount.objects.filter(election_type__iexact=election_type)
        party_votes_dict = {
            (p.election_type, p.party): p.vote_count
            for p in party_votes_qs
        }

        serializer = self.get_serializer(
            queryset,
            many=True,
            context={"request": request, "party_votes": party_votes_dict}
        )

        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)


# ------------------------
# Party Vote Count List
# ------------------------
class PartyVoteCountListView(generics.ListAPIView):
    serializer_class = PartyVoteCountSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['party']
    ordering_fields = ['vote_count']
    ordering = ['-vote_count']

    def list(self, request, *args, **kwargs):
        election_type = self.kwargs.get('election_type', '').lower()
        query_string = request.GET.urlencode()
        cache_key = f"party_votes_{election_type}_{query_string}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = PartyVoteCount.objects.filter(
            election_type__iexact=election_type
        ).order_by('-vote_count')

        serializer = self.get_serializer(queryset, many=True)

        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)


# ------------------------
# Cast Vote
# ------------------------
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

        # Prevent multiple votes in same election
        if Vote.objects.filter(user=user, election_type=election_type).exists():
            return Response({"error": "You have already voted in this election."}, status=status.HTTP_400_BAD_REQUEST)

        # Create vote safely
        Vote.objects.create(user=user, candidate=candidate)

        # Increment PartyVoteCount safely
        pvc, created = PartyVoteCount.objects.get_or_create(
            election_type=election_type,
            party=candidate.party,
            defaults={"party_image": candidate.party_image, "vote_count": 1}
        )
        if not created:
            PartyVoteCount.objects.filter(pk=pvc.pk).update(vote_count=F("vote_count") + 1)
            if not pvc.party_image:
                pvc.party_image = candidate.party_image
                pvc.save()

        # Clear cache safely
        if hasattr(cache, "delete_pattern"):
            cache.delete_pattern(f"candidates_{election_type}_*")
            cache.delete_pattern(f"party_votes_{election_type}_*")
        else:
            cache.clear()

        serializer = CandidateSerializer(candidate, context={"request": request})
        return Response({"message": "Vote submitted successfully!", "candidate": serializer.data}, status=status.HTTP_201_CREATED)
