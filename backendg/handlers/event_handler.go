package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"

	"github.com/VinitAgarwal21/City-Companion/models"
	"github.com/VinitAgarwal21/City-Companion/services"
)

type EventHandler struct {
	service *services.EventService
}

func NewEventHandler(
	service *services.EventService,
) *EventHandler {

	return &EventHandler{
		service: service,
	}
}

func (h *EventHandler) CreateEvent(
	c *gin.Context,
) {

	var event models.Event

	if err := c.ShouldBindJSON(&event); err != nil {

		c.JSON(
			http.StatusBadRequest,
			gin.H{
				"error": "invalid request body",
			},
		)

		return
	}

	err := h.service.CreateEvent(&event)

	if err != nil {

		c.JSON(
			http.StatusBadRequest,
			gin.H{
				"error": err.Error(),
			},
		)

		return
	}

	c.JSON(
		http.StatusCreated,
		event,
	)
}

func (h *EventHandler) GetEvents(
	c *gin.Context,
) {

	events, err :=
		h.service.GetEvents()

	if err != nil {

		c.JSON(
			http.StatusInternalServerError,
			gin.H{
				"error": "failed to fetch events",
			},
		)

		return
	}

	c.JSON(
		http.StatusOK,
		events,
	)
}

func (h *EventHandler) GetEvent(
	c *gin.Context,
) {

	id, err := strconv.ParseUint(
		c.Param("id"),
		10,
		64,
	)

	if err != nil {

		c.JSON(
			http.StatusBadRequest,
			gin.H{
				"error": "invalid event id",
			},
		)

		return
	}

	event, err :=
		h.service.GetEvent(uint(id))

	if err != nil {

		c.JSON(
			http.StatusNotFound,
			gin.H{
				"error": "event not found",
			},
		)

		return
	}

	c.JSON(
		http.StatusOK,
		event,
	)
}

func (h *EventHandler) DeleteEvent(
	c *gin.Context,
) {

	id, err := strconv.ParseUint(
		c.Param("id"),
		10,
		64,
	)

	if err != nil {

		c.JSON(
			http.StatusBadRequest,
			gin.H{
				"error": "invalid event id",
			},
		)

		return
	}

	err = h.service.DeleteEvent(uint(id))

	if err != nil {

		c.JSON(
			http.StatusInternalServerError,
			gin.H{
				"error": "failed to delete event",
			},
		)

		return
	}

	c.Status(http.StatusNoContent)
}
