#!/usr/bin/env bash
# ==============================================================================
# Run add-on locally without Home Assistant Supervisor
# ==============================================================================
set -e

echo "🚀 Starting add-on locally..."

# Ensure dev environment is setup
if [ ! -d data ]; then
    echo "📦 Setting up development environment..."
    ./scripts/setup-local-dev.sh
fi

# Check if options.json exists
if [ ! -f data/options.json ]; then
    echo "⚠️  data/options.json not found, creating with defaults..."
    mkdir -p data
    echo '{"log_level": "debug"}' > data/options.json
fi

echo "📋 Using configuration:"
cat data/options.json | python3 -m json.tool

echo ""
echo "🏃 Running add-on..."
echo "   Press Ctrl+C to stop"
echo ""

# Run the add-on
uv run python -m my_addon
