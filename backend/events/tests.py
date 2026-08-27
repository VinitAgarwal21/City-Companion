from datetime import date, timedelta, time
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from events.models import Category, Event


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------


class CategoryModelTests(TestCase):
    def test_slug_auto_generated(self):
        cat = Category.objects.create(name="Board Games")
        self.assertEqual(cat.slug, "board-games")

    def test_str(self):
        cat = Category.objects.create(name="Sports")
        self.assertEqual(str(cat), "Sports")


class EventModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Gaming", slug="gaming")

    def test_slug_auto_generated(self):
        event = Event.objects.create(
            title="Friday Night Valorant",
            description="Ranked grind",
            category=self.category,
            location_name="Online",
            date=date.today(),
            time=time(20, 0),
        )
        self.assertEqual(event.slug, "friday-night-valorant")

    def test_slug_uniqueness(self):
        for i in range(3):
            Event.objects.create(
                title="Duplicate Title",
                description=f"Event {i}",
                category=self.category,
                location_name="Somewhere",
                date=date.today(),
                time=time(18, 0),
            )
        slugs = list(
            Event.objects.filter(title="Duplicate Title").values_list(
                "slug", flat=True
            )
        )
        self.assertEqual(len(set(slugs)), 3)

    def test_str(self):
        event = Event.objects.create(
            title="Test Event",
            description="Desc",
            location_name="Here",
            date=date.today(),
            time=time(10, 0),
        )
        self.assertEqual(str(event), "Test Event")


# ---------------------------------------------------------------------------
# Category API Tests
# ---------------------------------------------------------------------------


class CategoryApiTests(APITestCase):
    URL = "/api/v1/categories/"

    def test_create_category(self):
        response = self.client.post(self.URL, {"name": "Sports"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Sports")
        self.assertEqual(response.data["slug"], "sports")

    def test_list_categories(self):
        Category.objects.create(name="Sports", slug="sports")
        Category.objects.create(name="Music", slug="music")
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_category(self):
        cat = Category.objects.create(name="Food", slug="food")
        response = self.client.get(f"{self.URL}{cat.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Food")

    def test_update_category(self):
        cat = Category.objects.create(name="Sportz", slug="sportz")
        response = self.client.put(f"{self.URL}{cat.id}/", {"name": "Sports"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Sports")

    def test_delete_category(self):
        cat = Category.objects.create(name="Temp", slug="temp")
        response = self.client.delete(f"{self.URL}{cat.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=cat.id).exists())

    def test_duplicate_name_rejected(self):
        Category.objects.create(name="Sports", slug="sports")
        response = self.client.post(self.URL, {"name": "Sports"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------
# Event API Tests
# ---------------------------------------------------------------------------


class EventApiTests(APITestCase):
    URL = "/api/v1/events/"

    def setUp(self):
        self.category = Category.objects.create(name="Sports", slug="sports")
        self.event_data = {
            "title": "Saturday Cricket",
            "description": "Casual match at the local ground.",
            "category": self.category.id,
            "location_name": "DDA Ground",
            "latitude": 28.58,
            "longitude": 77.05,
            "date": str(date.today() + timedelta(days=1)),
            "time": "10:00:00",
            "max_participants": 12,
            "created_by_name": "Rohan",
        }

    def _create_event(self, **overrides):
        data = {**self.event_data, **overrides}
        return self.client.post(self.URL, data, format="json")

    # -- CRUD ---------------------------------------------------------------

    def test_create_event(self):
        response = self._create_event()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Saturday Cricket")
        self.assertEqual(response.data["category_name"], "Sports")
        self.assertEqual(response.data["status"], "open")
        self.assertIn("slug", response.data)

    def test_create_event_without_category(self):
        response = self._create_event(category=None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["category_name"])

    def test_create_event_missing_title(self):
        data = {**self.event_data}
        del data["title"]
        response = self.client.post(self.URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_invalid_max_participants(self):
        response = self._create_event(max_participants=0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_missing_location(self):
        response = self._create_event(location_name="")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_events(self):
        self._create_event(title="Event 1")
        self._create_event(title="Event 2")
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        # List view should NOT include description
        self.assertNotIn("description", response.data["results"][0])

    def test_retrieve_event(self):
        create_resp = self._create_event()
        event_id = create_resp.data["id"]
        response = self.client.get(f"{self.URL}{event_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Detail view SHOULD include description
        self.assertIn("description", response.data)
        self.assertEqual(response.data["spots_left"], 11)

    def test_update_event(self):
        create_resp = self._create_event()
        event_id = create_resp.data["id"]
        updated = {**self.event_data, "title": "Sunday Cricket"}
        response = self.client.put(
            f"{self.URL}{event_id}/", updated, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Sunday Cricket")

    def test_partial_update_event(self):
        create_resp = self._create_event()
        event_id = create_resp.data["id"]
        response = self.client.patch(
            f"{self.URL}{event_id}/",
            {"title": "Updated Title"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_event(self):
        create_resp = self._create_event()
        event_id = create_resp.data["id"]
        response = self.client.delete(f"{self.URL}{event_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # -- Filtering ----------------------------------------------------------

    def test_filter_by_category(self):
        music = Category.objects.create(name="Music", slug="music")
        self._create_event(title="Cricket", category=self.category.id)
        self._create_event(title="Concert", category=music.id)
        response = self.client.get(f"{self.URL}?category__slug=sports")
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Cricket")

    def test_filter_by_status(self):
        resp = self._create_event(title="Open Event")
        event_id = resp.data["id"]
        # Cancel the event
        self.client.post(f"{self.URL}{event_id}/cancel/")
        # Filter for open events
        response = self.client.get(f"{self.URL}?status=open")
        for event in response.data["results"]:
            self.assertEqual(event["status"], "open")

    # -- Search -------------------------------------------------------------

    def test_search_by_title(self):
        self._create_event(title="Bowling Night")
        self._create_event(title="Cricket Match")
        response = self.client.get(f"{self.URL}?search=bowling")
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Bowling Night")

    def test_search_by_description(self):
        self._create_event(
            title="Game Night",
            description="Playing Valorant ranked",
        )
        self._create_event(
            title="Movie Night",
            description="Watching Inception",
        )
        response = self.client.get(f"{self.URL}?search=valorant")
        self.assertEqual(len(response.data["results"]), 1)

    # -- Ordering -----------------------------------------------------------

    def test_ordering_by_date(self):
        tomorrow = date.today() + timedelta(days=1)
        next_week = date.today() + timedelta(days=7)
        self._create_event(title="Later", date=str(next_week))
        self._create_event(title="Sooner", date=str(tomorrow))
        response = self.client.get(f"{self.URL}?ordering=date")
        titles = [e["title"] for e in response.data["results"]]
        self.assertEqual(titles[0], "Sooner")
        self.assertEqual(titles[1], "Later")

    # -- Custom Actions -----------------------------------------------------

    def test_cancel_event(self):
        resp = self._create_event()
        event_id = resp.data["id"]
        response = self.client.post(f"{self.URL}{event_id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "cancelled")

    def test_cancel_already_cancelled(self):
        resp = self._create_event()
        event_id = resp.data["id"]
        self.client.post(f"{self.URL}{event_id}/cancel/")
        response = self.client.post(f"{self.URL}{event_id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_complete_event(self):
        resp = self._create_event()
        event_id = resp.data["id"]
        response = self.client.post(f"{self.URL}{event_id}/complete/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")

    def test_complete_cancelled_event_fails(self):
        resp = self._create_event()
        event_id = resp.data["id"]
        self.client.post(f"{self.URL}{event_id}/cancel/")
        response = self.client.post(f"{self.URL}{event_id}/complete/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -- Pagination ---------------------------------------------------------

    def test_pagination(self):
        for i in range(25):
            self._create_event(title=f"Event {i}")
        response = self.client.get(self.URL)
        self.assertEqual(len(response.data["results"]), 20)  # PAGE_SIZE=20
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
