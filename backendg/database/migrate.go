package database

import (
	"log"

	"github.com/VinitAgarwal21/City-Companion/models"

	"gorm.io/gorm"
)

func Migrate(db *gorm.DB) {

	err := db.AutoMigrate(
		&models.Event{},
	)

	if err != nil {
		log.Fatal("Database migration failed:", err)
	}

	log.Println("Database migration completed")
}
