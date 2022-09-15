from django.core.cache import cache
from celery import shared_task

from top_scores.models import Score

@shared_task
def add_or_update_score(count:int) -> None:
    top_scorers = Score.objects.all().order_by('-score')[:count]
    cache.set(f'top_{count}_scorers', list(top_scorers.values_list('id', flat=True)))

    last_score = top_scorers[min(count, len(top_scorers))-1].score
    cache.set(f'top_{count}_last_score', last_score)