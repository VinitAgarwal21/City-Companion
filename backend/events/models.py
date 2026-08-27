from django.db import models
from django.utils.text import slugify
import itertools


class Category(models.Model):
    """Event category (e.g., Movies, Gaming, Sports)."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    """A local activity that users can discover and join."""

    STATUS_CHOICES = [
        ("open", "Open"),
        ("full", "Full"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="open"
    )

    # Location
    location_name = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Scheduling
    date = models.DateField()
    time = models.TimeField()

    # Participation
    max_participants = models.PositiveIntegerField(default=5)
    current_participants = models.PositiveIntegerField(default=1)

    # Ownership — simple string until auth is implemented
    created_by_name = models.CharField(max_length=255, default="Anonymous")

    # Soft delete
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            for i in itertools.count(1):
                if not Event.objects.filter(slug=slug).exists():
                    break
                slug = f"{base_slug}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
