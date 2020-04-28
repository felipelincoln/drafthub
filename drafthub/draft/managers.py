from django.db import models
from django.db.models import Case, When, Value, Count, Q
from django.utils import timezone
from datetime import timedelta

from . import onlinedata


class DraftManager(models.Manager):
    def get_queryset(self):
        latest_date = timezone.now() - timedelta(days=7) # everything from the last minute is considered new
        queryset = super().get_queryset().annotate(
            last_views=Count('activities', filter=Q(activities__viewed__gte=latest_date)),
            last_favorites=Count('activities', filter=Q(activities__favorited__gte=latest_date)),
            last_likes=Count('activities', filter=Q(activities__liked__gte=latest_date)),
        )
        return queryset


class TagManager(models.Manager):
    online_data = onlinedata.TAG_ONLINE_DATA

    def get_queryset(self):
        latest_date = timezone.now() - timedelta(days=7) # everything from the last minute is considered new
        queryset = super().get_queryset().annotate(
            icon=Case(
            *[When(name=k, then=Value(v['icon'])) for k, v in self.online_data.items()],
            output_field=models.CharField()
            ),
            description=Case(
            *[When(name=k, then=Value(v['description'])) for k, v in self.online_data.items()],
            output_field=models.CharField()
            ),
            num_drafts=Count('tagged_drafts'),
            last_drafts=Count('tagged_drafts', filter=Q(tagged_drafts__pub_date__gte=latest_date)
                |Q(tagged_drafts__last_update__gte=latest_date)
            )
        )
        return queryset
