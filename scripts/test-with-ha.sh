#!/usr/bin/env bash
# ==============================================================================
# Test add-on with local Home Assistant Supervisor
# ==============================================================================
set -e

echo "🏠 Testing with Home Assistant Supervisor..."

# Check if HA_ADDONS_DIR is set
ADDON_DIR="${HA_ADDONS_DIR:-}"
if [ -z "$ADDON_DIR" ]; then
    echo "⚠️  HA_ADDONS_DIR not set"
    echo "   Please set it to your Home Assistant addons directory"
    echo "   Example: export HA_ADDONS_DIR=/usr/share/hassio/addons/local"
    exit 1
fi

if [ ! -d "$ADDON_DIR" ]; then
    echo "❌ Directory not found: $ADDON_DIR"
    exit 1
fi

# Build the add-on
echo "🏗️  Building add-on..."
./scripts/build-addon.sh

# Copy to HA addons directory
DEST_DIR="$ADDON_DIR/my_addon"
echo "📦 Copying to $DEST_DIR..."

mkdir -p "$DEST_DIR"
cp -r addon/* "$DEST_DIR/"

echo ""
echo "✅ Add-on copied to Home Assistant!"
echo ""
echo "Next steps:"
echo "  1. Open Home Assistant"
echo "  2. Go to Supervisor → Add-on Store"
echo "  3. Refresh the page"
echo "  4. Look for 'My Python Add-on' in Local Add-ons"
echo "  5. Install and start the add-on"
echo ""
