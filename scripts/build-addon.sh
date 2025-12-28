#!/usr/bin/env bash
# ==============================================================================
# Build Home Assistant add-on container using Podman
# ==============================================================================
set -e

ARCH=${1:-amd64}
TAG=${2:-local/my-addon:latest}

# Map architecture names
case "$ARCH" in
    amd64|x86_64)
        BUILD_ARCH="amd64"
        ;;
    aarch64|arm64)
        BUILD_ARCH="aarch64"
        ;;
    armv7|armhf)
        BUILD_ARCH="armv7"
        ;;
    *)
        echo "❌ Unsupported architecture: $ARCH"
        echo "Supported: amd64, aarch64, armv7, armhf, i386"
        exit 1
        ;;
esac

echo "🏗️  Building add-on for $BUILD_ARCH..."
echo "📦 Tag: $TAG"

# Get the base image from build.yaml
BASE_IMAGE="ghcr.io/home-assistant/${BUILD_ARCH}-base-python:3.11-alpine3.18"

# Build with Podman
podman build \
    --build-arg BUILD_FROM="$BASE_IMAGE" \
    --build-arg BUILD_ARCH="$BUILD_ARCH" \
    --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --build-arg BUILD_DESCRIPTION="My Python Add-on" \
    --build-arg BUILD_NAME="My Python Add-on" \
    --build-arg BUILD_REF="$(git rev-parse HEAD 2>/dev/null || echo 'unknown')" \
    --build-arg BUILD_REPOSITORY="$(git remote get-url origin 2>/dev/null || echo 'local')" \
    --build-arg BUILD_VERSION="0.1.0" \
    -f addon/Dockerfile \
    -t "$TAG" \
    .

echo ""
echo "✅ Build complete!"
echo "📦 Image: $TAG"
echo ""
echo "Next steps:"
echo "  1. Test locally: make run"
echo "  2. Or run: podman run --rm -p 8000:8000 $TAG"
echo ""
