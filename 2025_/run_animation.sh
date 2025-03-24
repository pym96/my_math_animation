#!/bin/bash
# This script runs the Newton Method animation with all necessary safety measures

# Set safer bash options
set -o pipefail

# Determine the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "=== Newton Method Animation Runner ==="
echo "This script will run the animation with safety measures"
echo ""

# Clean up any problematic files that might be causing issues
echo "Cleaning up any problematic cache files..."
find ../media -name "._*" -type f -delete 2>/dev/null || true

# Run the animation with safe settings
echo "Starting animation with safe settings..."
python render_newton.py

# If the animation fails, try the direct approach
if [ $? -ne 0 ]; then
    echo "Trying alternative rendering method..."
    manim --no_latex_cleanup --disable_caching -pqh newton_method.py NewtonMethodAnimation
fi

echo ""
echo "Animation rendering completed"
echo "Check the 'media' directory for the output video" 