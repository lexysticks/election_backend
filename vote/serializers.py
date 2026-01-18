from rest_framework import serializers
from .models import Candidate, PartyVoteCount, Vote
from django.conf import settings


# ==============================
# SHARED SAFE IMAGE HELPER
# ==============================
def safe_image_url(request, url):
    """
    Try https first, fallback to http, else placeholder
    """
    if not url:
        return "/placeholder.png"

    # Absolute URL
    absolute_url = request.build_absolute_uri(url)

    if absolute_url.startswith("http://"):
        return absolute_url.replace("http://", "https://")

    return absolute_url


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
        request = self.context.get("request")

        if obj.image and obj.image.url:
            return safe_image_url(request, obj.image.url)

        return "/placeholder.png"

    def get_party_image_url(self, obj):
        request = self.context.get("request")

        if obj.party_image and obj.party_image.url:
            return safe_image_url(request, obj.party_image.url)

        return "/placeholder.png"

    def get_party_votes(self, obj):
        party_votes = self.context.get("party_votes", {})
        return party_votes.get((obj.election_type, obj.party), 0)

    def get_user_voted(self, obj):
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
        request = self.context.get("request")

        if obj.party_image and obj.party_image.url:
            return safe_image_url(request, obj.party_image.url)

        return "/placeholder.png"


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
#         # If image exists, force HTTPS if needed; else fallback to placeholder
#         if obj.image and obj.image.url:
#             return obj.image.url.replace("http://", "https://")
#         return "/placeholder.png"

#     def get_party_image_url(self, obj):
#         if obj.party_image and obj.party_image.url:
#             return obj.party_image.url.replace("http://", "https://")
#         return "/placeholder.png"

#     def get_party_votes(self, obj):
#         party_votes = self.context.get("party_votes", {})
#         return party_votes.get((obj.election_type, obj.party), 0)

#     def get_user_voted(self, obj):
#         user_votes = self.context.get("user_votes", set())
#         return obj.id in user_votes


# # ==============================
# # Party Vote Count Serializer
# # ==============================
# class PartyVoteCountSerializer(serializers.ModelSerializer):
#     party_image_url = serializers.SerializerMethodField()

#     class Meta:
#         model = PartyVoteCount
#         fields = ["party", "vote_count", "election_type", "party_image_url"]

#     def get_party_image_url(self, obj):
#         if obj.party_image and obj.party_image.url:
#             return obj.party_image.url.replace("http://", "https://")
#         return "/placeholder.png"


# # ==============================
# # Vote Serializer (Write Only)
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






















