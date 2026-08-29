package models

import (
	"time"

	"gorm.io/gorm"
)

type Event struct {
	ID        uint           `gorm:"primaryKey" json:"id"`
	CreatedAt time.Time      `json:"createdAt"`
	UpdatedAt time.Time      `json:"updatedAt"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`

	Title       string `json:"title"`
	Description string `json:"description"`

	Category string `json:"category"`

	LocationName string  `json:"locationName"`
	Latitude     float64 `json:"latitude"`
	Longitude    float64 `json:"longitude"`

	Date time.Time `json:"date"`

	MaxParticipants     int `json:"maxParticipants"`
	CurrentParticipants int `json:"currentParticipants"`
}
