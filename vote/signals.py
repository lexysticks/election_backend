from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Candidate, PartyVoteCount, Vote



@receiver([post_save, post_delete], sender=Candidate)
def clear_candidates_cache(sender, instance, **kwargs):
    election_type = instance.election_type
    cache.delete(f"candidates_{election_type}")



@receiver([post_save, post_delete], sender=PartyVoteCount)
def clear_party_votes_cache(sender, instance, **kwargs):
    election_type = instance.election_type
    cache.delete(f"party_votes_{election_type}")



@receiver(post_save, sender=Vote)
def clear_votes_cache_on_vote(sender, instance, **kwargs):
    election_type = instance.candidate.election_type
    cache.delete(f"party_votes_{election_type}")
