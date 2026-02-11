#!/bin/bash
set -e

# Configuration
IMAGE_NAME="ghcr.io/b-robotized/erpnext_nextcloud_sso:stable"
# Volume names as defined in docker-compose.yaml
VOLUMES=(
    "erpnext_nextcloud_sso_docker_db-data"
    "erpnext_nextcloud_sso_docker_redis-queue-data"
    "erpnext_nextcloud_sso_docker_sites"
)

# Function to show help
show_help() {
    echo "Usage: ./manage.sh [OPTIONS]"
    echo ""
    echo "Automates the cleanup and restart of the local Docker test environment."
    echo ""
    echo "Options:"
    echo "  --clean-only    Stop containers, remove volumes and images, then exit."
    echo "  --help          Show this help message."
    echo ""
}

# Cleanup function
cleanup() {
    echo ""
    echo "=========================================="
    echo "Stopping Docker containers..."
    echo "=========================================="
    docker compose down

    echo ""
    echo "=========================================="
    echo "Cleaning up Docker volumes..."
    echo "=========================================="
    for vol in "${VOLUMES[@]}"; do
        if docker volume inspect "$vol" >/dev/null 2>&1; then
            docker volume rm "$vol"
            echo "✓ Removed volume: $vol"
        else
            echo "- Volume not found (skipped): $vol"
        fi
    done

    echo ""
    echo "=========================================="
    echo "Removing Docker image..."
    echo "=========================================="
    if docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
        docker rmi "$IMAGE_NAME"
        echo "✓ Removed image: $IMAGE_NAME"
    else
        echo "- Image not found (skipped): $IMAGE_NAME"
    fi
}

# Parse arguments
CLEAN_ONLY=false

for arg in "$@"; do
    case $arg in
        --clean-only)
            CLEAN_ONLY=true
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            show_help
            exit 1
            ;;
    esac
done

# Switch to docker directory for correct context
# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/docker" || { echo "Error: docker directory not found"; exit 1; }

# Perform initial cleanup to ensure fresh state
cleanup

# Exit if clean-only mode
if [ "$CLEAN_ONLY" = true ]; then
    echo ""
    echo "Cleanup complete. Exiting."
    exit 0
fi

# Register trap to ensure cleanup happens on exit
trap cleanup EXIT INT TERM

echo ""
echo "=========================================="
echo "Starting Docker environment..."
echo "=========================================="
docker compose up -d --build

echo ""
echo "=========================================="
echo "Following configurator logs..."
echo "=========================================="
echo "Press Ctrl+C to stop following logs (Cleanup will run automatically)."
echo ""
docker compose logs -f configurator
