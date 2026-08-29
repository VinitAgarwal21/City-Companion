package services

import (
	"errors"

	"github.com/VinitAgarwal21/City-Companion/models"
	"github.com/VinitAgarwal21/City-Companion/repositories"
)

type EventService struct {
	repository *repositories.EventRepository
}

func NewEventService(
	repository *repositories.EventRepository,
) *EventService {

	return &EventService{
		repository: repository,
	}
}

func (s *EventService) CreateEvent(
	event *models.Event,
) error {

	if event.Title == "" {
		return errors.New("event title is required")
	}

	if event.Description == "" {
		return errors.New("event description is required")
	}

	if event.MaxParticipants < 1 {
		return errors.New(
			"max participants must be at least 1",
		)
	}

	if event.Latitude < -90 ||
		event.Latitude > 90 {

		return errors.New(
			"invalid latitude",
		)
	}

	if event.Longitude < -180 ||
		event.Longitude > 180 {

		return errors.New(
			"invalid longitude",
		)
	}

	event.CurrentParticipants = 1

	return s.repository.Create(event)
}

func (s *EventService) GetEvents() (
	[]models.Event,
	error,
) {

	return s.repository.FindAll()
}

func (s *EventService) GetEvent(
	id uint,
) (*models.Event, error) {

	return s.repository.FindByID(id)
}

func (s *EventService) UpdateEvent(
	event *models.Event,
) error {

	return s.repository.Update(event)
}

func (s *EventService) DeleteEvent(
	id uint,
) error {

	return s.repository.Delete(id)
}
