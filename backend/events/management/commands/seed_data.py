import random
from datetime import date, timedelta, time
from django.core.management.base import BaseCommand
from events.models import Category, Event


CATEGORIES = [
    ("Movies", "movies"),
    ("Gaming", "gaming"),
    ("Sports", "sports"),
    ("Food", "food"),
    ("Music", "music"),
    ("Outdoors", "outdoors"),
    ("Nightlife", "nightlife"),
    ("Other", "other"),
]

SAMPLE_EVENTS = [
    {
        "title": "Friday Night Bowling",
        "description": "Looking for 3-4 people to join for bowling at Blu-O. Casual game, no experience needed!",
        "category_slug": "sports",
        "location_name": "Blu-O Bowling, Ambience Mall",
        "latitude": 28.5040,
        "longitude": 77.0960,
        "max_participants": 5,
    },
    {
        "title": "Weekend Hiking to Triund",
        "description": "Planning a day hike to Triund. Starting early morning. Bring water and snacks.",
        "category_slug": "outdoors",
        "location_name": "McLeod Ganj Bus Stand",
        "latitude": 32.2396,
        "longitude": 76.3210,
        "max_participants": 8,
    },
    {
        "title": "Marvel Marathon at My Place",
        "description": "Watching the Infinity Saga back to back. Popcorn and pizza provided. Bring snacks if you want!",
        "category_slug": "movies",
        "location_name": "Sector 62, Noida",
        "latitude": 28.6274,
        "longitude": 77.3646,
        "max_participants": 6,
    },
    {
        "title": "Valorant 5-Stack Tonight",
        "description": "Need 2 more for a ranked 5-stack. Plat+ preferred but chill vibes. Discord required.",
        "category_slug": "gaming",
        "location_name": "Online (Discord)",
        "latitude": None,
        "longitude": None,
        "max_participants": 5,
    },
    {
        "title": "Street Food Walk in Chandni Chowk",
        "description": "Exploring the best street food spots in Old Delhi. Meeting at Jama Masjid metro station.",
        "category_slug": "food",
        "location_name": "Jama Masjid Metro Station",
        "latitude": 28.6507,
        "longitude": 77.2334,
        "max_participants": 10,
    },
    {
        "title": "Open Mic Night at Piano Man",
        "description": "Open mic comedy + music night. Come perform or just watch. Cover charge applies.",
        "category_slug": "music",
        "location_name": "Piano Man Jazz Club, Safdarjung",
        "latitude": 28.5672,
        "longitude": 77.2022,
        "max_participants": 4,
    },
    {
        "title": "Saturday Morning Cricket",
        "description": "Casual cricket match at the local ground. All skill levels welcome. Bring your own kit if possible.",
        "category_slug": "sports",
        "location_name": "DDA Sports Complex, Dwarka",
        "latitude": 28.5823,
        "longitude": 77.0500,
        "max_participants": 12,
    },
    {
        "title": "Board Games Cafe Meetup",
        "description": "Settlers of Catan, Ticket to Ride, Codenames — pick your poison. Meeting at Board Game Cafe.",
        "category_slug": "gaming",
        "location_name": "Board Game Cafe, Hauz Khas",
        "latitude": 28.5494,
        "longitude": 77.2001,
        "max_participants": 6,
    },
    {
        "title": "Late Night Maggi at Ridge",
        "description": "Nothing fancy — just hot maggi and chai at Ridge Road. BYOB (bring your own blanket).",
        "category_slug": "food",
        "location_name": "Ridge Road, North Campus",
        "latitude": 28.6950,
        "longitude": 77.2100,
        "max_participants": 8,
    },
    {
        "title": "Pub Crawl in Cyber Hub",
        "description": "Hitting 3-4 pubs in Cyber Hub. Starting at 8 PM. Splitting tabs individually.",
        "category_slug": "nightlife",
        "location_name": "Cyber Hub, Gurgaon",
        "latitude": 28.4945,
        "longitude": 77.0889,
        "max_participants": 6,
    },
]

NAMES = [
    "Aarav", "Priya", "Rohan", "Sneha", "Vikram",
    "Ananya", "Karan", "Diya", "Arjun", "Meera",
]


class Command(BaseCommand):
    help = "Seed the database with sample categories and events."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            Event.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing data."))

        # Create categories
        categories = {}
        for name, slug in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=slug, defaults={"name": name}
            )
            categories[slug] = cat
            status_msg = "Created" if created else "Exists"
            self.stdout.write(f"  {status_msg}: Category '{name}'")

        # Create events
        today = date.today()
        created_count = 0
        for event_data in SAMPLE_EVENTS:
            cat_slug = event_data.pop("category_slug")
            event_date = today + timedelta(days=random.randint(1, 14))
            event_time = time(
                hour=random.choice([9, 10, 14, 17, 18, 19, 20, 21]),
                minute=random.choice([0, 15, 30, 45]),
            )
            current = random.randint(1, event_data["max_participants"] - 1)

            _, created = Event.objects.get_or_create(
                title=event_data["title"],
                defaults={
                    **event_data,
                    "category": categories[cat_slug],
                    "date": event_date,
                    "time": event_time,
                    "current_participants": current,
                    "created_by_name": random.choice(NAMES),
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! Created {created_count} events across {len(categories)} categories."
            )
        )
