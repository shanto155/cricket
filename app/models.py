from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Match(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_inning = models.IntegerField(default=1)
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    total_over = models.IntegerField(default=0)
    toss_winner = models.CharField(max_length=100)
    toss_choice = models.CharField(max_length=100)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    team1_wicket = models.IntegerField(default=0)
    team2_wicket = models.IntegerField(default=0)
    team1_over = models.IntegerField(default=0)
    team2_over = models.IntegerField(default=0)
    match_winner = models.CharField(max_length=100)

    def __str__(self):
        return self.team1 + " vs " + self.team2
