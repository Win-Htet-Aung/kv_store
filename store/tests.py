import json
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Item
from .services import create_items


class StoreTestCase(TestCase):
    def setUp(self) -> None:
        data = {
            "key-1": "value-1",
            "key-2": "value-2",
        }
        create_items(data)

    def test_create_items(self) -> None:
        Item.objects.filter(key="key-1").update(
            expires_at=timezone.now() - timedelta(minutes=5)
        )
        test_data = {
            "key-1": "value-11",
            "key-3": "value-3",
        }
        response = self.client.post(
            path="/values", data=test_data, content_type="application/json"
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["message"], "Items create report!")
        self.assertEqual(data["success"], ["key-1", "key-3"])
        response = self.client.get(path="/values?keys=key-1,key-3")
        data = json.loads(response.content)
        self.assertEqual(data, test_data)
    
    def test_create_items_failed(self) -> None:
        test_data = {"key-1": "value-1"}
        response = self.client.post(
            path="/values", data=test_data, content_type="application/json"
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["message"], "Items create report!")
        self.assertEqual(data["success"], [])
        self.assertEqual(data["failed"], ["key-1"])

    def test_create_items_empty_body(self) -> None:
        response = self.client.post(
            path="/values", data=None, content_type="application/json"
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Empty body!")

    def test_get_items(self) -> None:
        response = self.client.get(path="/values")
        data = json.loads(response.content)
        self.assertEqual(data, {"key-1": "value-1", "key-2": "value-2"})

    def test_get_expired_items(self) -> None:
        Item.objects.filter(key="key-1").update(
            expires_at=timezone.now() - timedelta(minutes=5)
        )
        response = self.client.get(path="/values")
        data = json.loads(response.content)
        self.assertEqual(data, {"key-2": "value-2"})
        self.assertFalse(Item.objects.filter(key="key-1").exists())

    def test_filter_items(self) -> None:
        Item.objects.filter(key="key-1").update(
            expires_at=timezone.now() - timedelta(minutes=5)
        )
        response = self.client.get(path="/values?keys=key-1,key-2,key-3")
        data = json.loads(response.content)
        self.assertEqual(data, {"key-2": "value-2"})

    def test_get_items_ttl_reset(self) -> None:
        old_time = Item.objects.get(key="key-1").expires_at
        self.client.get(path="/values?keys=key-1")
        self.assertGreater(Item.objects.get(key="key-1").expires_at, old_time)

    def test_get_items_not_found(self) -> None:
        response = self.client.get(path="/values?keys=key-3")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {"message": "No items found!"})

    def test_update_items(self) -> None:
        Item.objects.filter(key="key-1").update(
            expires_at=timezone.now() - timedelta(minutes=5)
        )
        update_data = {
            "key-1": "value-11",
            "key-2": "value-22",
            "key-3": "value-33",
        }
        response = self.client.patch(path="/values", data=update_data, content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Items update report!")
        self.assertEqual(data["success"], ["key-2"])
        self.assertEqual(data["failed"], ["key-1", "key-3"])
        response = self.client.get(path="/values")
        data = json.loads(response.content)
        self.assertEqual(data, {"key-2": "value-22"})
