#!/bin/bash

# Generate docker-compose.yml from config
python3 generate_compose.py config.yaml

# Start the services
docker compose up $@