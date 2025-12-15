from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django.core.cache import cache
from .models import Candidate, PartyVoteCount, Vote
from .serializers import CandidateSerializer, PartyVoteCountSerializer, VoteSerializer

# -----------------------------
# Candidate List View with Cache
# -----------------------------
class CandidateListView(generics.ListAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        election_type = self.kwargs.get("election_type", "").lower()
        return Candidate.objects.filter(election_type__iexact=election_type).order_by("name")

    def list(self, request, *args, **kwargs):
        election_type = self.kwargs.get("election_type", "").lower()
        cache_key = f"candidates_{election_type}_{request.user.id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = self.get_queryset()

        # Prefetch votes by current user
        user_votes = set(
            Vote.objects.filter(user=request.user, election_type=election_type)
            .values_list("candidate_id", flat=True)
        )

        # Prefetch party votes
        votes = PartyVoteCount.objects.filter(election_type=election_type)
        party_votes_dict = {(v.election_type, v.party): v.vote_count for v in votes}

        serializer = self.get_serializer(
            queryset,
            many=True,
            context={"request": request, "user_votes": user_votes, "party_votes": party_votes_dict}
        )

        cache.set(cache_key, serializer.data, timeout=3600)  # cache for 1 min
        return Response(serializer.data)


# -----------------------------
# Party Vote List View with Cache
# -----------------------------
class PartyVoteListView(generics.ListAPIView):
    serializer_class = PartyVoteCountSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["party"]
    ordering_fields = ["vote_count", "party"]
    ordering = ["-vote_count"]

    def get_queryset(self):
        election_type = self.kwargs.get("election_type", "").lower()
        return PartyVoteCount.objects.filter(election_type__iexact=election_type).order_by("-vote_count", "party")

    def list(self, request, *args, **kwargs):
        election_type = self.kwargs.get("election_type", "").lower()
        query_string = request.GET.urlencode()
        cache_key = f"party_votes_{election_type}_{query_string}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        cache.set(cache_key, serializer.data, timeout=360)  
        return Response(serializer.data)


# -----------------------------
# Cast Vote View
# -----------------------------




from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import F
from django.core.cache import cache
from .models import Candidate, PartyVoteCount, Vote
from .serializers import VoteSerializer

class CastVoteView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        candidate = Candidate.objects.get(id=serializer.validated_data["candidate_id"])
        election_type = candidate.election_type

        # ----------------------------
        # Prevent double voting
        # ----------------------------
        if Vote.objects.filter(user=request.user, election_type=election_type).exists():
            return Response(
                {"error": "You have already voted in this election."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ----------------------------
        # Create vote
        # ----------------------------
        Vote.objects.create(
            user=request.user,
            candidate=candidate,
            election_type=election_type
        )

        # ----------------------------
        # Atomic increment of party vote
        # ----------------------------
        party_count, created = PartyVoteCount.objects.get_or_create(
            election_type=election_type,
            party=candidate.party,
            defaults={"party_image": candidate.party_image, "vote_count": 0}
        )

        # F() ensures atomic increment
        PartyVoteCount.objects.filter(id=party_count.id).update(
            vote_count=F('vote_count') + 1,
            party_image=candidate.party_image if not party_count.party_image else party_count.party_image
        )

        # ----------------------------
        # Clear caches
        # ----------------------------
        cache.delete(f"candidates_{election_type}_{request.user.id}")
        try:
            keys = cache.keys(f"party_votes_{election_type}*")
            for key in keys:
                cache.delete(key)
        except NotImplementedError:
            cache.delete(f"party_votes_{election_type}_")

        return Response(
            {"message": "Vote submitted successfully!"},
            status=status.HTTP_201_CREATED
        )
