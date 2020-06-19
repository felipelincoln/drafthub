from django.db import models
from django.db.models import Case, When, Value, Count, Q, F
from django.utils import timezone
from datetime import timedelta

from .metadata import TAG_METADATA

pop_timedelta = timedelta(days=1)


class DraftManager(models.Manager):
    def get_queryset(self):
        last_week = timezone.now() - pop_timedelta
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
        queryset = queryset.order_by('-last_activities', '-created',)

        return queryset

    def get_random_queryset(self, n):
        from random import randint
        count = self.model.objects.all().count() - n
        rand = randint(0, count)

        return self.all()[rand:rand+n]


class TagManager(models.Manager):
    def get_queryset(self):
        last_week = timezone.now() - pop_timedelta
        queryset = super().get_queryset().annotate(
            pack=Case(
                *[When(name=k, then=Value(v['pack'])) \
                for k, v in TAG_METADATA.items()],
                default=Value(''),
                output_field=models.CharField()
            ),
            icon=Case(
                *[When(name=k, then=Value(v['icon'])) \
                for k, v in TAG_METADATA.items()],
                default=Value(''),
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
        queryset = queryset.order_by(
            '-tagged_drafts_last_activities', 'last_drafts',
        )

        return queryset
