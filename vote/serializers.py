

from rest_framework import serializers
from .models import Candidate, Vote, PartyVoteCount

# ------------------------
# Candidate Serializer
# ------------------------
class CandidateSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    party_votes = serializers.SerializerMethodField()
    user_voted = serializers.SerializerMethodField()  # To track if current user voted
    party_image_url = serializers.SerializerMethodField()  # NEW

    class Meta:
        model = Candidate
        fields = [
            "id",
            "name",
            "party",
            "age",
            "election_type",
            "image_url",
            "party_votes",
            "user_voted",
            "party_image_url",  # include the new field
        ]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_party_votes(self, obj):
        pvc = PartyVoteCount.objects.filter(
            election_type=obj.election_type,
            party=obj.party
        ).first()
        return pvc.vote_count if pvc else 0

    def get_user_voted(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Vote.objects.filter(
                user=request.user, election_type=obj.election_type
            ).exists()
        return False

    def get_party_image_url(self, obj):
        if obj.party_image:
            return obj.party_image.url
        return None


# ------------------------
# PartyVoteCount Serializer
# ------------------------
class PartyVoteCountSerializer(serializers.ModelSerializer):
    party_image_url = serializers.SerializerMethodField()  # NEW

    class Meta:
        model = PartyVoteCount
        fields = ["party", "vote_count", "election_type", "party_image_url"]

    def get_party_image_url(self, obj):
        if obj.party_image:
            return obj.party_image.url
        return None


# ------------------------
# Vote Serializer
# ------------------------
class VoteSerializer(serializers.ModelSerializer):
    candidate_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Vote
        fields = ["candidate_id"]

    def validate_candidate_id(self, value):
        if not Candidate.objects.filter(id=value).exists():
            raise serializers.ValidationError("Candidate does not exist.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        candidate = Candidate.objects.get(id=validated_data["candidate_id"])

        # Prevent double voting in same election type
        if Vote.objects.filter(user=user, election_type=candidate.election_type).exists():
            raise serializers.ValidationError("You have already voted in this election.")

        vote = Vote.objects.create(user=user, candidate=candidate)
        return vote
