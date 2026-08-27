from rest_framework import serializers
from .models import Category, Event


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category CRUD."""

    event_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "event_count", "created_at"]
        read_only_fields = ["id", "slug", "created_at"]


class EventListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for event list views (no description)."""

    category_name = serializers.CharField(
        source="category.name", read_only=True, default=None
    )
    category_slug = serializers.CharField(
        source="category.slug", read_only=True, default=None
    )
    spots_left = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "slug",
            "category_name",
            "category_slug",
            "status",
            "location_name",
            "latitude",
            "longitude",
            "date",
            "time",
            "max_participants",
            "current_participants",
            "spots_left",
            "created_by_name",
            "created_at",
        ]

    def get_spots_left(self, obj):
        return max(0, obj.max_participants - obj.current_participants)


class EventDetailSerializer(serializers.ModelSerializer):
    """Full serializer for single event detail views."""

    category_name = serializers.CharField(
        source="category.name", read_only=True, default=None
    )
    category_slug = serializers.CharField(
        source="category.slug", read_only=True, default=None
    )
    spots_left = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "category",
            "category_name",
            "category_slug",
            "status",
            "location_name",
            "latitude",
            "longitude",
            "date",
            "time",
            "max_participants",
            "current_participants",
            "spots_left",
            "created_by_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "updated_at",
        ]

    def get_spots_left(self, obj):
        return max(0, obj.max_participants - obj.current_participants)


class EventWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating events with validation."""

    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "category",
            "location_name",
            "latitude",
            "longitude",
            "date",
            "time",
            "max_participants",
            "created_by_name",
        ]

    def validate_max_participants(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "max_participants must be at least 1."
            )
        return value

    def validate(self, attrs):
        # On partial updates, location_name may not be in attrs — that's fine.
        # Only reject if it's explicitly provided as empty, or missing on create.
        is_partial = self.instance is not None and self.partial
        if not is_partial and not attrs.get("location_name"):
            raise serializers.ValidationError(
                {"location_name": "Location name is required."}
            )
        if "location_name" in attrs and not attrs["location_name"]:
            raise serializers.ValidationError(
                {"location_name": "Location name cannot be empty."}
            )
        return attrs

    def to_representation(self, instance):
        """Return full detail representation after create/update."""
        return EventDetailSerializer(instance, context=self.context).data
