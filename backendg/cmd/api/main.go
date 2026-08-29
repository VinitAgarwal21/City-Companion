package main

import (
	"log"

	"github.com/gin-gonic/gin"

	"github.com/VinitAgarwal21/City-Companion/database"
	"github.com/VinitAgarwal21/City-Companion/handlers"
	"github.com/VinitAgarwal21/City-Companion/internal/config"
	"github.com/VinitAgarwal21/City-Companion/repositories"
	"github.com/VinitAgarwal21/City-Companion/routes"
	"github.com/VinitAgarwal21/City-Companion/services"
)

func main() {

	// Load configuration
	cfg := config.Load()

	// Connect to database
	db := database.Connect(cfg)

	// Run migrations
	database.Migrate(db)

	// Repository
	eventRepository :=
		repositories.NewEventRepository(db)

	// Service
	eventService :=
		services.NewEventService(
			eventRepository,
		)

	// Handler
	eventHandler :=
		handlers.NewEventHandler(
			eventService,
		)

	// Gin
	router := gin.Default()

	// Routes
	routes.Setup(
		router,
		eventHandler,
	)

	log.Println(
		"Server running on port",
		cfg.ServerPort,
	)

	err := router.Run(
		":" + cfg.ServerPort,
	)

	if err != nil {
		log.Fatal(err)
	}
}
