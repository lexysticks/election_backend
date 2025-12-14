from rest_framework import serializers
from .models import Candidate, PartyVoteCount, Vote

# ------------------------
# Candidate Serializer
# ------------------------
class CandidateSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    party_votes = serializers.SerializerMethodField()
    user_voted = serializers.SerializerMethodField()
    party_image_url = serializers.SerializerMethodField()

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
            "party_image_url",
        ]

    def get_image_url(self, obj):
        try:
            return obj.image.url
        except Exception:
            return None

    def get_party_votes(self, obj):
        # Use pre-fetched context if available to reduce queries
        party_votes_dict = self.context.get("party_votes", {})
        return party_votes_dict.get((obj.election_type, obj.party), 0)

    def get_user_voted(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user and getattr(user, "is_authenticated", False):
            return Vote.objects.filter(
                user=user,
                election_type=obj.election_type
            ).exists()
        return False

    def get_party_image_url(self, obj):
        try:
            return obj.party_image.url
        except Exception:
            return None


# ------------------------
# PartyVoteCount Serializer
# ------------------------
class PartyVoteCountSerializer(serializers.ModelSerializer):
    party_image_url = serializers.SerializerMethodField()

    class Meta:
        model = PartyVoteCount
        fields = ["party", "vote_count", "election_type", "party_image_url"]

    def get_party_image_url(self, obj):
        try:
            return obj.party_image.url
        except Exception:
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
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            raise serializers.ValidationError("Authentication required.")

        candidate = Candidate.objects.get(id=validated_data["candidate_id"])

        # Prevent double voting
        if Vote.objects.filter(user=user, election_type=candidate.election_type).exists():
            raise serializers.ValidationError("You have already voted in this election.")

        vote = Vote.objects.create(user=user, candidate=candidate)
        return vote
