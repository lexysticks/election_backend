
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status

# from .models import Candidate, PartyVoteCount, Vote
# from .serializers import CandidateSerializer, PartyVoteCountSerializer, VoteSerializer


# @api_view(["GET"])
# def get_candidates(request, election_type):
#     candidates = Candidate.objects.filter(election_type=election_type)
#     serializer = CandidateSerializer(candidates, many=True, context={"request": request})
#     return Response(serializer.data)


# @api_view(["GET"])
# def get_party_votes(request, election_type):
#     party_votes = PartyVoteCount.objects.filter(election_type=election_type)
#     serializer = PartyVoteCountSerializer(party_votes, many=True)
#     return Response(serializer.data)



# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def cast_vote(request):
#     candidate_id = request.data.get("candidate")
#     user = request.user

#     if not candidate_id:
#         return Response({"error": "Candidate ID is required."}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         candidate = Candidate.objects.get(id=candidate_id)
#     except Candidate.DoesNotExist:
#         return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)

#     election_type = candidate.election_type


#     if Vote.objects.filter(user=user, candidate__election_type=election_type).exists():
#         return Response({"error": "You have already voted in this election."}, status=status.HTTP_400_BAD_REQUEST)

#     # Create vote
#     Vote.objects.create(user=user, candidate=candidate)
#     return Response({"message": "Vote submitted successfully!"}, status=status.HTTP_201_CREATED)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Candidate, PartyVoteCount, Vote
from .serializers import CandidateSerializer, PartyVoteCountSerializer, VoteSerializer


@api_view(["GET"])
def get_candidates(request, election_type):
    """
    Get all candidates for a specific election type.
    Includes candidate info, votes, and party image.
    """
    candidates = Candidate.objects.filter(election_type=election_type)
    serializer = CandidateSerializer(candidates, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def get_party_votes(request, election_type):
    """
    Get all parties with their vote counts for a specific election type.
    Includes party image.
    """
    party_votes = PartyVoteCount.objects.filter(election_type=election_type)
    serializer = PartyVoteCountSerializer(party_votes, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cast_vote(request):
    """
    Cast a vote for a candidate. Prevents double voting.
    Returns the updated candidate info including party votes and party image.
    """
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

    # Create vote
    Vote.objects.create(user=user, candidate=candidate)

    # Serialize updated candidate info
    serializer = CandidateSerializer(candidate, context={"request": request})

    return Response({
        "message": "Vote submitted successfully!",
        "candidate": serializer.data  # includes party_votes and party_image_url
    }, status=status.HTTP_201_CREATED)
