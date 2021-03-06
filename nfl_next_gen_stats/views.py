from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import *
import numpy as np


def home(request):
    return render(request, 'nfl_next_gen_stats/home.html')


class SearchResultsView(ListView):
    model = Player
    template_name = 'nfl_next_gen_stats/player-search.html'

    def get_queryset(self):
        query = self.request.GET.get('player')
        if query:
            object_list = Player.objects.filter(Q(full_name__icontains=query))
            return object_list
        else:
            return None


def qb_ngs_api(request, season=None):
    passing_queryset = PassingStats.objects.filter(week=0, season=season).values()

    final = []
    for p in passing_queryset:
        final.append({
            'player': Player.objects.get(gsis_id=p.get('gsis_id')).full_name,
            'stats': p
        })

    return JsonResponse(final, safe=False)


def wr_ngs_api(request, season=None, week=0):
    receiving_queryset = ReceivingStats.objects.filter(week=week, season=season).values()

    final = []
    for p in receiving_queryset:
        final.append({
            'player': Player.objects.get(gsis_id=p.get('gsis_id')).full_name,
            'stats': p
        })

    return JsonResponse(final, safe=False)


def player_page(request, gsis_id=None, season=None):

    player = get_object_or_404(Player, gsis_id=gsis_id)
    passing_stats = player.passing_stats().order_by('season', 'week')
    rushing_stats = player.rushing_stats().order_by('season', 'week')
    receiving_stats = player.receiving_stats().order_by('season', 'week')

    pass_years = np.array(passing_stats.order_by('season').values_list('season', flat=True).distinct())
    rush_years = np.array(rushing_stats.order_by('season').values_list('season', flat=True).distinct())
    rec_years = np.array(receiving_stats.order_by('season').values_list('season', flat=True).distinct())

    years = np.append(pass_years, rush_years)
    years = np.append(years, rec_years)

    context = {
        'player': player,
        'years': years
    }

    if season:
        context.update({
            'title': f"{player.full_name} -- {season}",
            'season': season,
            'passing_stats': passing_stats.filter(~Q(week=0), season=season),
            'rushing_stats': rushing_stats.filter(~Q(week=0), season=season),
            'receiving_stats': receiving_stats.filter(~Q(week=0), season=season),
        })

    else:
        context.update({
            'title': player.full_name,
            'passing_stats': passing_stats.filter(week=0),
            'rushing_stats': rushing_stats.filter(week=0),
            'receiving_stats': receiving_stats.filter(week=0),
        })

    return render(request, 'nfl_next_gen_stats/player.html', context)
