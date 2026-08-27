from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from .models import Category, Event
from .serializers import (
    CategorySerializer,
    EventListSerializer,
    EventDetailSerializer,
    EventWriteSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD for event categories.

    GET    /api/v1/categories/          — list all categories
    POST   /api/v1/categories/          — create a category
    GET    /api/v1/categories/{id}/     — retrieve a category
    PUT    /api/v1/categories/{id}/     — update a category
    DELETE /api/v1/categories/{id}/     — delete a category
    """

    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def get_queryset(self):
        return Category.objects.annotate(event_count=Count("events"))


class EventViewSet(viewsets.ModelViewSet):
    """
    CRUD for events with filtering, search, and ordering.

    GET    /api/v1/events/                  — list events (filterable)
    POST   /api/v1/events/                  — create an event
    GET    /api/v1/events/{id}/             — retrieve event detail
    PUT    /api/v1/events/{id}/             — update an event
    PATCH  /api/v1/events/{id}/             — partial update
    DELETE /api/v1/events/{id}/             — delete an event
    POST   /api/v1/events/{id}/cancel/      — cancel an event
    POST   /api/v1/events/{id}/complete/    — mark event as completed

    Filters:
        ?category=1               — filter by category ID
        ?category__slug=sports    — filter by category slug
        ?status=open              — filter by status
        ?date=2026-09-01          — filter by exact date
        ?is_active=true           — filter active/inactive

    Search:
        ?search=bowling           — search title and description

    Ordering:
        ?ordering=-date           — order by date descending
        ?ordering=created_at      — order by creation date
    """

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "category": ["exact"],
        "category__slug": ["exact"],
        "status": ["exact"],
        "date": ["exact", "gte", "lte"],
        "is_active": ["exact"],
    }
    search_fields = ["title", "description", "location_name"]
    ordering_fields = ["date", "time", "created_at", "max_participants"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Event.objects.select_related("category").filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        if self.action in ("create", "update", "partial_update"):
            return EventWriteSerializer
        return EventDetailSerializer

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel an event. Only open events can be cancelled."""
        event = self.get_object()
        if event.status != "open":
            return Response(
                {"detail": f"Cannot cancel an event with status '{event.status}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        event.status = "cancelled"
        event.save(update_fields=["status", "updated_at"])
        return Response(EventDetailSerializer(event).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """Mark an event as completed. Only open or full events can be completed."""
        event = self.get_object()
        if event.status not in ("open", "full"):
            return Response(
                {"detail": f"Cannot complete an event with status '{event.status}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        event.status = "completed"
        event.save(update_fields=["status", "updated_at"])
        return Response(EventDetailSerializer(event).data)
