#!/usr/bin/env bash
# ==============================================================================
# Setup local development environment without Home Assistant Supervisor
# ==============================================================================
set -e

echo "🔧 Setting up local development environment..."

# Create mock data directory
mkdir -p data
if [ ! -f data/options.json ]; then
    echo '{"log_level": "debug"}' > data/options.json
    echo "✓ Created data/options.json with default options"
fi

# Install dependencies
echo "📦 Installing dependencies with uv..."
uv sync --extra dev

echo ""
echo "✅ Local dev environment ready!"
echo ""
echo "Next steps:"
echo "  1. Run: make dev"
echo "  2. Or run: uv run python -m my_addon"
echo "  3. Visit: http://localhost:8000"
echo ""
