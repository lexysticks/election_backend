from rest_framework import serializers
from .models import Candidate, PartyVoteCount, Vote

# ==============================
# Candidate Serializer
# ==============================
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
        # Return candidate image URL or placeholder
        return obj.image.url if obj.image else "/placeholder.png"

    def get_party_image_url(self, obj):
        # Return party logo URL or placeholder
        return obj.party_image.url if obj.party_image else "/placeholder.png"

    def get_party_votes(self, obj):
        # Use pre-fetched party_votes from context
        party_votes = self.context.get("party_votes", {})
        return party_votes.get((obj.election_type, obj.party), 0)

    def get_user_voted(self, obj):
        # Use pre-fetched user_votes set from context
        user_votes = self.context.get("user_votes", set())
        return obj.id in user_votes


# ==============================
# Party Vote Count Serializer
# ==============================
class PartyVoteCountSerializer(serializers.ModelSerializer):
    party_image_url = serializers.SerializerMethodField()

    class Meta:
        model = PartyVoteCount
        fields = ["party", "vote_count", "election_type", "party_image_url"]

    def get_party_image_url(self, obj):
        return obj.party_image.url if obj.party_image else "/placeholder.png"


# ==============================
# Vote Serializer (Write Only)
# ==============================
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

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")

        candidate = Candidate.objects.get(id=validated_data["candidate_id"])

        # Prevent double voting per election
        if Vote.objects.filter(user=user, election_type=candidate.election_type).exists():
            raise serializers.ValidationError(
                "You have already voted in this election."
            )

        # Create vote
        vote = Vote.objects.create(
            user=user,
            candidate=candidate,
            election_type=candidate.election_type
        )
        return vote








# from rest_framework import serializers
# from .models import Candidate, PartyVoteCount, Vote

# # ==============================
# # Candidate Serializer
# # ==============================
# class CandidateSerializer(serializers.ModelSerializer):
#     image_url = serializers.SerializerMethodField()
#     party_votes = serializers.SerializerMethodField()
#     user_voted = serializers.SerializerMethodField()
#     party_image_url = serializers.SerializerMethodField()

#     class Meta:
#         model = Candidate
#         fields = [
#             "id",
#             "name",
#             "party",
#             "age",
#             "election_type",
#             "image_url",
#             "party_votes",
#             "user_voted",
#             "party_image_url",
#         ]

#     def get_image_url(self, obj):
#         return obj.image.url if obj.image else None

#     def get_party_image_url(self, obj):
#         return obj.party_image.url if obj.party_image else None

#     def get_party_votes(self, obj):
#         """
#         Uses precomputed party_votes from view context for performance
#         """
#         party_votes = self.context.get("party_votes", {})
#         return party_votes.get((obj.election_type, obj.party), 0)

#     def get_user_voted(self, obj):
#         """
#         Returns True only if the current user voted for THIS candidate.
#         """
#         user_votes = self.context.get("user_votes", set())
#         return obj.id in user_votes


# # ==============================
# # Party Vote Count Serializer
# # ==============================
# class PartyVoteCountSerializer(serializers.ModelSerializer):
#     party_image_url = serializers.SerializerMethodField()

#     class Meta:
#         model = PartyVoteCount
#         fields = [
#             "party",
#             "vote_count",
#             "election_type",
#             "party_image_url",
#         ]

#     def get_party_image_url(self, obj):
#         return obj.party_image.url if obj.party_image else None


# # ==============================
# # Vote Serializer (WRITE ONLY)
# # ==============================
# class VoteSerializer(serializers.ModelSerializer):
#     candidate_id = serializers.IntegerField(write_only=True)

#     class Meta:
#         model = Vote
#         fields = ["candidate_id"]

#     def validate_candidate_id(self, value):
#         if not Candidate.objects.filter(id=value).exists():
#             raise serializers.ValidationError("Candidate does not exist.")
#         return value

#     def create(self, validated_data):
#         request = self.context.get("request")
#         user = getattr(request, "user", None)

#         if not user or not user.is_authenticated:
#             raise serializers.ValidationError("Authentication required.")

#         candidate = Candidate.objects.get(id=validated_data["candidate_id"])

#         # Prevent double voting per election
#         if Vote.objects.filter(user=user, election_type=candidate.election_type).exists():
#             raise serializers.ValidationError("You have already voted in this election.")

#         vote = Vote.objects.create(
#             user=user,
#             candidate=candidate,
#             election_type=candidate.election_type
#         )
#         return vote
