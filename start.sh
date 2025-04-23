#!/bin/bash

# Generate docker-compose.yml from config
python generate_compose.py config.yaml

# Start the services
docker compose up $@