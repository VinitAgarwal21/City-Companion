package repositories

import (
	"github.com/VinitAgarwal21/City-Companion/models"

	"gorm.io/gorm"
)

type EventRepository struct {
	db *gorm.DB
}

func NewEventRepository(db *gorm.DB) *EventRepository {
	return &EventRepository{
		db: db,
	}
}

func (r *EventRepository) Create(
	event *models.Event,
) error {

	return r.db.Create(event).Error
}

func (r *EventRepository) FindAll() ([]models.Event, error) {

	var events []models.Event

	err := r.db.
		Order("created_at DESC").
		Find(&events).
		Error

	return events, err
}

func (r *EventRepository) FindByID(
	id uint,
) (*models.Event, error) {

	var event models.Event

	err := r.db.
		First(&event, id).
		Error

	if err != nil {
		return nil, err
	}

	return &event, nil
}

func (r *EventRepository) Update(
	event *models.Event,
) error {

	return r.db.Save(event).Error
}

func (r *EventRepository) Delete(
	id uint,
) error {

	return r.db.Delete(
		&models.Event{},
		id,
	).Error
}
