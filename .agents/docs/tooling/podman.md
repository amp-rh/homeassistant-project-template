# Podman for Home Assistant Add-ons

Podman is used to build and test Home Assistant add-on containers locally. This guide covers using Podman specifically for HA add-on development.

## Overview

Home Assistant add-ons are containers built from official Home Assistant base images. Podman allows you to:
- Build add-on containers locally
- Test add-ons without Home Assistant Supervisor
- Develop and iterate quickly
- Debug container issues

## Installation

### Linux
```bash
# Fedora/RHEL/CentOS
sudo dnf install podman

# Ubuntu/Debian
sudo apt-get install podman

# Arch Linux
sudo pacman -S podman
```

### macOS
```bash
brew install podman
podman machine init
podman machine start
```

## Building Add-ons

### Basic Build

```bash
# Build for current architecture
podman build \
    --build-arg BUILD_FROM="ghcr.io/home-assistant/amd64-base-python:3.11-alpine3.18" \
    -f addon/Dockerfile \
    -t local/my-addon:latest \
    .
```

### Multi-Architecture Build

Home Assistant add-ons support multiple architectures. Build for specific platforms:

```bash
# AMD64 (x86_64)
podman build \
    --build-arg BUILD_FROM="ghcr.io/home-assistant/amd64-base-python:3.11-alpine3.18" \
    --build-arg BUILD_ARCH="amd64" \
    -f addon/Dockerfile \
    -t local/my-addon:amd64 \
    .

# ARM64 (aarch64)
podman build \
    --build-arg BUILD_FROM="ghcr.io/home-assistant/aarch64-base-python:3.11-alpine3.18" \
    --build-arg BUILD_ARCH="aarch64" \
    -f addon/Dockerfile \
    -t local/my-addon:aarch64 \
    .

# ARMv7 (armhf)
podman build \
    --build-arg BUILD_FROM="ghcr.io/home-assistant/armv7-base-python:3.11-alpine3.18" \
    --build-arg BUILD_ARCH="armv7" \
    -f addon/Dockerfile \
    -t local/my-addon:armv7 \
    .
```

### Using the Build Script

The template includes a build script that handles architecture selection:

```bash
# Build for default architecture (amd64)
./scripts/build-addon.sh

# Build for specific architecture
./scripts/build-addon.sh aarch64

# Build with custom tag
./scripts/build-addon.sh amd64 my-custom-tag:latest
```

## Running Add-ons Locally

### Basic Run

```bash
# Run the add-on container
podman run --rm -p 8000:8000 local/my-addon:latest
```

### With Volume Mounts

```bash
# Mount local data directory
podman run --rm \
    -p 8000:8000 \
    -v $(pwd)/data:/data:Z \
    local/my-addon:latest
```

### With Environment Variables

```bash
# Set environment variables (for testing)
podman run --rm \
    -p 8000:8000 \
    -v $(pwd)/data:/data:Z \
    -e LOG_LEVEL=debug \
    local/my-addon:latest
```

### Interactive Debugging

```bash
# Run with shell for debugging
podman run --rm -it \
    -v $(pwd)/data:/data:Z \
    local/my-addon:latest \
    /bin/bash

# Execute command in running container
podman exec -it <container-id> /bin/bash
```

## Home Assistant Base Images

Home Assistant provides official base images for add-ons:

### Python Base Images
- `ghcr.io/home-assistant/amd64-base-python:3.11-alpine3.18`
- `ghcr.io/home-assistant/aarch64-base-python:3.11-alpine3.18`
- `ghcr.io/home-assistant/armv7-base-python:3.11-alpine3.18`

### Other Base Images
- `ghcr.io/home-assistant/*-base` - Minimal base
- `ghcr.io/home-assistant/*-base-debian` - Debian-based
- `ghcr.io/home-assistant/*-base-ubuntu` - Ubuntu-based

All base images include:
- s6-overlay for service management
- bashio for configuration and logging
- Home Assistant add-on utilities

## Dockerfile Best Practices

### Use ARG for Build-Time Variables

```dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION
```

### Install Dependencies Efficiently

```dockerfile
# Combine RUN commands to reduce layers
RUN apk add --no-cache \
    python3 \
    py3-pip \
    && python3 -m pip install --break-system-packages uv

# Clean up after installation
RUN apk add --no-cache package \
    && cleanup-command \
    && rm -rf /tmp/*
```

### Copy Files in Correct Order

```dockerfile
# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code last
COPY src/ ./src/
```

### Set Proper Permissions

```dockerfile
# Make scripts executable
RUN chmod a+x /etc/services.d/addon/run
```

## Development Workflow

### 1. Setup Local Environment
```bash
make setup
```

### 2. Develop and Test Locally (without container)
```bash
make dev
```

### 3. Build Container
```bash
make build
```

### 4. Test Container Locally
```bash
make run
```

### 5. Test with Home Assistant
```bash
make test-addon
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
podman logs <container-id>

# Inspect container
podman inspect <container-id>

# Run interactively
podman run --rm -it local/my-addon:latest /bin/bash
```

### Permission Issues

```bash
# Use :Z flag for SELinux contexts
-v $(pwd)/data:/data:Z

# Or disable SELinux for testing (not recommended for production)
--security-opt label=disable
```

### Network Issues

```bash
# Use host networking
podman run --rm --network host local/my-addon:latest

# Map specific ports
podman run --rm -p 8000:8000 -p 8123:8123 local/my-addon:latest
```

### Image Size Issues

```bash
# Check image size
podman images

# Remove unused images
podman image prune

# Clean build cache
podman system prune -a
```

## Makefile Targets

The template provides these Podman-related targets:

```bash
make build        # Build add-on container
make build-addon  # Build add-on container (explicit)
make run          # Run add-on locally
make clean        # Clean up build artifacts
```

## References

- [Podman Documentation](https://docs.podman.io/)
- [Home Assistant Base Images](https://github.com/home-assistant/docker-base)
- [Home Assistant Add-on Tutorial](https://developers.home-assistant.io/docs/add-ons/tutorial)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
