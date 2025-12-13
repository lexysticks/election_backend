
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings

ELECTION_TYPES = (
    ("presidential", "Presidential"),
    ("governorship", "Governorship"),
    ("senatorial", "Senatorial"),
)

class Candidate(models.Model):
    election_type = models.CharField(max_length=20, choices=ELECTION_TYPES,db_index=True)
    name = models.CharField(max_length=100,db_index=True)
    party = models.CharField(max_length=100,db_index=True)
    party_image = CloudinaryField("party_image")
    age = models.IntegerField()
    image = CloudinaryField("image")
    
    
    class Meta:
        indexes = [
            models.Index(fields=['election_type', 'party','name']),  
        ]
   
    def __str__(self):
        return f"{self.name} - {self.election_type}"


class PartyVoteCount(models.Model):
    election_type = models.CharField(max_length=20, choices=ELECTION_TYPES,db_index=True)
    party = models.CharField(max_length=100,db_index=True)
    vote_count = models.PositiveIntegerField(default=0)
    party_image = CloudinaryField("party_image", null=True, blank=True)
    
    class Meta:
        unique_together = ("election_type", "party")

    def __str__(self):
        return f"{self.party} ({self.election_type}): {self.vote_count}"


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election_type = models.CharField(max_length=20, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "election_type"],
                name="unique_vote_per_election"
            )
        ]

    def save(self, *args, **kwargs):
        
        self.election_type = self.candidate.election_type
        super().save(*args, **kwargs)

        
        party_count, created = PartyVoteCount.objects.get_or_create(
            election_type=self.election_type,
            party=self.candidate.party,
            defaults={"party_image": self.candidate.party_image}
        )
        if not created:
            party_count.vote_count += 1
        
            if not party_count.party_image:
                party_count.party_image = self.candidate.party_image
        else:
            party_count.vote_count = 1  

        party_count.save()

    def __str__(self):
        return f"{self.user} voted for {self.candidate.name}"
