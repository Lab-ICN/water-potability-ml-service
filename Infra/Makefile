SHELL := /bin/bash

# Detect the OS (Linux vs. Darwin/macOS)
OS := $(shell uname -s)

ifeq ($(OS),Linux)
    CERTGEN_SCRIPT = certgen-linux-amd64
else ifeq ($(OS),Darwin)
    CERTGEN_SCRIPT = certgen-mac-arm
else ifeq ($(OS),Windows_NT)
    CERTGEN_SCRIPT = certgen-windows-amd64
else
    $(error Unsupported OS detected: $(OS))
endif

# Define the Docker Compose command based on availability
ifeq ($(shell command -v docker compose > /dev/null 2>&1 && echo found),found)
    DOCKER_CMD = docker compose
else ifeq ($(shell command -v docker-compose > /dev/null 2>&1 && echo found),found)
    DOCKER_CMD = docker-compose
else
    $(error Neither "docker compose" nor "docker-compose" is available on your system. Please install Docker Compose.)
endif

# Add sudo for Linux if required
ifneq (,$(findstring Linux,$(OS)))
    ifneq (,$(shell groups | grep docker))
        # If the user is in the docker group, no need for sudo
        DOCKER_CMD = $(DOCKER_CMD)
    else
        DOCKER_CMD = sudo $(DOCKER_CMD)
    endif
endif

# Default target if you type just `make`
.DEFAULT_GOAL := run

.PHONY: network run down logs clean certs

## network: Create the mlops network if not exists
network:
	@echo "Creating 'mlops' network if it doesn't exist..."
	-docker network create mlops

## certs: Generate certificates using the appropriate script
certs:
	@echo "Generating certificates using $(CERTGEN_SCRIPT)..."
	cd certs && ./$(CERTGEN_SCRIPT) --host "localhost,minio-*"

## run: Create the network first, then run docker compose
run: certs
	@echo "Running '$(DOCKER_CMD) up -d --build'..."
	$(DOCKER_CMD) up -d --build

## down: Stop and remove containers (but keep volumes)
down:
	@echo "Stopping and removing containers..."
	$(DOCKER_CMD) down

## logs: Follow logs of all containers
logs:
	@echo "Attaching logs (Ctrl+C to quit)..."
	$(DOCKER_CMD) logs -f

## clean: Stop containers and remove volumes
clean:
	@echo "Stopping and removing containers, including volumes..."
	$(DOCKER_CMD) down -v