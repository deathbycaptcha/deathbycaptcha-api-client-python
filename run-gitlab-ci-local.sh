#!/bin/bash
# Script to run GitLab CI pipeline locally with gitlab-ci-local
# This script loads credentials from .env and runs the pipeline

set -e

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env file with your credentials:"
    echo "  cp .env.sample .env"
    echo "  # Edit .env with your credentials"
    exit 1
fi

# Load environment variables from .env
set -a
source .env
set +a

# Verify credentials are set
if [ -z "$DBC_TEST_AUTHTOKEN" ] && { [ -z "$DBC_TEST_USERNAME" ] || [ -z "$DBC_TEST_PASSWORD" ]; }; then
    echo "❌ Error: Set DBC_TEST_AUTHTOKEN or both DBC_TEST_USERNAME and DBC_TEST_PASSWORD in .env"
    exit 1
fi

echo "✓ Loaded credentials from .env"
echo "🚀 Running GitLab CI pipeline locally..."
echo ""

# Pass variables to gitlab-ci-local using --variable flag
# gitlab-ci-local needs variables in the format expected by GitLab CI
gitlab-ci-local \
  --file ./.gitlab-ci.yml \
  --variable "DBC_USERNAME=$DBC_TEST_USERNAME" \
  --variable "DBC_PASSWORD=$DBC_TEST_PASSWORD" \
  --variable "DBC_AUTHTOKEN=$DBC_TEST_AUTHTOKEN" \
  "$@"

