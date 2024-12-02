#!/bin/bash

# Enable strict error handling
set -euo pipefail

# Define variables
DOCKER_IMAGE=${1:-xowlpost/glibc}
GLIBC_VERSION=${2:-2.38}
PLATFORMS=${3:-linux/amd64,linux/arm64}
LOG_FILE="build_and_push.log"

# Log function for consistent output
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO]: $1" | tee -a "$LOG_FILE"
}

error() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR]: $1" | tee -a "$LOG_FILE"
    exit 1
}

# Start the log file
echo "Starting build and push process" > "$LOG_FILE"

log "Build and push process initiated for image $DOCKER_IMAGE:$GLIBC_VERSION."

# Step 1: Ensure Docker is logged in
log "Checking Docker login status..."
if ! docker info >/dev/null 2>&1; then
    log "Logging into Docker Hub..."
    docker login || error "Docker login failed. Exiting."
else
    log "Already logged in to Docker Hub."
fi

# Step 2: Set up buildx for multi-architecture builds
log "Setting up buildx builder..."
if ! docker buildx inspect multiarch-builder >/dev/null 2>&1; then
    docker buildx create --name multiarch-builder --use --bootstrap || error "Buildx setup failed."
    log "Buildx multi-architecture builder created successfully."
else
    log "Buildx multi-architecture builder already exists. Using it."
fi

# Step 3: Build and push the image
log "Building and pushing the Docker image for platforms: $PLATFORMS."
{
    docker buildx build \
        --platform "$PLATFORMS" \
        -t "$DOCKER_IMAGE:$GLIBC_VERSION" \
        --push .
} || error "Failed to build and push the image."

log "Build and push process completed successfully for $DOCKER_IMAGE:$GLIBC_VERSION."

# Step 4: Verify the image
log "Verifying the pushed image..."
{
    docker buildx imagetools inspect "$DOCKER_IMAGE:$GLIBC_VERSION" | tee -a "$LOG_FILE"
} || error "Image verification failed."

log "Image verification completed. Multi-architecture support confirmed."

# Final message
log "Build and push process completed successfully. Log file: $LOG_FILE."
