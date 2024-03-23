from django.contrib import admin

# Register your models here.
from .models import Match


class MatchAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_over', 'toss_winner', 'toss_choice', 'team1', 'team1_score', 'team1_wicket', 'team1_over', 'team2', 'team2_score', 'team2_wicket', 'team2_over', 'match_winner']


admin.site.register(Match, MatchAdmin)
