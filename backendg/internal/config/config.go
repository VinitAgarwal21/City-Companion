package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	DatabaseURL string
	ServerPort  string
}

func Load() Config {

	err := godotenv.Load()

	if err != nil {
		log.Println(
			"No .env file found, using environment variables",
		)
	}

	return Config{
		DatabaseURL: os.Getenv("DATABASE_URL"),
		ServerPort:  os.Getenv("SERVER_PORT"),
	}
}
