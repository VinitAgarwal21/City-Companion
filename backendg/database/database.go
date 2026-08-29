package database

import (
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"

	"github.com/VinitAgarwal21/City-Companion/internal/config"
)

func Connect(cfg config.Config) *gorm.DB {

	db, err := gorm.Open(
		postgres.Open(cfg.DatabaseURL),
		&gorm.Config{},
	)

	if err != nil {
		log.Fatal(
			"Failed to connect to Neon:",
			err,
		)
	}

	log.Println("Connected to Neon PostgreSQL")

	return db
}
