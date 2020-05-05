from django.db import models
from django.db.models import Case, When, Value, Count, Q, F
from django.utils import timezone
from datetime import timedelta

from .metadata import TAG_METADATA


class DraftManager(models.Manager):
    def get_queryset(self):
        last_week = timezone.now() - timedelta(days=7)
        queryset = super().get_queryset().annotate(
            last_views=Count(
                'activities',
                distinct=True,
                filter=Q(activities__viewed__gte=last_week)
            ),
            last_favorites=Count(
                'activities',
                distinct=True,
                filter=Q(activities__favorited__gte=last_week)
            ),
            last_likes=Count(
                'activities',
                distinct=True,
                filter=Q(activities__liked__gte=last_week)
            ),
            last_activities=F('last_views')+F('last_favorites')+F('last_likes')
        )

        return queryset


class TagManager(models.Manager):
    def get_queryset(self):
        last_week = timezone.now() - timedelta(days=7)
        queryset = super().get_queryset().annotate(
            icon=Case(
                *[When(name=k, then=Value(v['icon'])) \
                for k, v in TAG_METADATA.items()],
                output_field=models.CharField()
            ),
            description=Case(
                *[When(name=k, then=Value(v['description'])) \
                for k, v in TAG_METADATA.items()],
                output_field=models.CharField()
            ),
            num_drafts=Count('tagged_drafts', distinct=True),
            last_drafts=Count(
                'tagged_drafts',
                distinct=True,
                filter=Q(tagged_drafts__created__gte=last_week)
                |Q(tagged_drafts__updated__gte=last_week)
            ),
            tagged_drafts_last_views=Count(
                'tagged_drafts',
                distinct=True,
                filter=Q(tagged_drafts__activities__viewed__gte=last_week)
            ),
            tagged_drafts_last_favorites=Count(
                'tagged_drafts',
                distinct=True,
                filter=Q(tagged_drafts__activities__favorited__gte=last_week)
            ),
            tagged_drafts_last_likes=Count(
                'tagged_drafts',
                distinct=True,
                filter=Q(tagged_drafts__activities__liked__gte=last_week)
            ),
            tagged_drafts_last_activities=F('tagged_drafts_last_views')
                +F('tagged_drafts_last_favorites')
                +F('tagged_drafts_last_likes'),
        )

        return queryset
