from django.utils import timezone
from datetime import timedelta
from .models import Item


def create_items(data: dict) -> dict:
    response_data = {
        "message": "Items create report!",
        "success": [],
        "failed": [],
    }
    for key, value in data.items():
        item = Item.objects.filter(key=key).first()
        if item and item.expires_at > timezone.now():
            response_data["failed"].append(key)
        elif item and item.expires_at < timezone.now():
            item.value = value
            item.expires_at = timezone.now() + timedelta(minutes=5)
            item.save()
            response_data["success"].append(key)
        elif not item:
            Item.objects.create(
                key=key, value=value, expires_at=timezone.now() + timedelta(minutes=5)
            )
            response_data["success"].append(key)
    return response_data


def filter_items(keys: str) -> dict:
    Item.objects.filter(expires_at__lt=timezone.now()).delete()
    items = Item.objects.filter(expires_at__gte=timezone.now())
    if keys:
        items = items.filter(key__in=keys.split(","))
    data = {}
    for item in items:
        data[item.key] = item.value
        item.expires_at = timezone.now() + timedelta(minutes=5)
        item.save()
    return data

def update_items(data: dict) -> dict:
    response_data = {
        "message": "Items update report!",
        "success": [],
        "failed": [],
    }
    for key, value in data.items():
        item = Item.objects.filter(key=key).first()
        if not item:
            response_data["failed"].append(key)
        elif item.expires_at < timezone.now():
            item.delete()
            response_data["failed"].append(key)
        elif item.expires_at > timezone.now():
            item.value = value
            item.expires_at = timezone.now() + timedelta(minutes=5)
            item.save()
            response_data["success"].append(key)
    return response_data
