package routes

import (
	"github.com/gin-gonic/gin"

	"github.com/VinitAgarwal21/City-Companion/handlers"
)

func Setup(
	router *gin.Engine,
	eventHandler *handlers.EventHandler,
) {

	api := router.Group("/api")

	events := api.Group("/events")

	{
		events.POST("", eventHandler.CreateEvent)

		events.GET("", eventHandler.GetEvents)

		events.GET(
			"/:id",
			eventHandler.GetEvent,
		)

		events.DELETE(
			"/:id",
			eventHandler.DeleteEvent,
		)
	}
}
