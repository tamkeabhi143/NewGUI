#!/bin/bash
# Signal Manager Build Script for Linux
# This script creates a standalone executable for the Signal Manager application

echo "Signal Manager - Linux Build Script"
echo "==================================="

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check for required packages
echo "Checking required packages..."
python3 -m pip install -q PyQt5 pyinstaller

# Set project directories
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RELEASE_DIR="$PROJECT_DIR/Release/Linux"

# Create release directory if it doesn't exist
mkdir -p "$RELEASE_DIR"

# Navigate to project directory
cd "$PROJECT_DIR"

# Build the executable with PyInstaller
echo "Building executable with PyInstaller..."
python3 -m PyInstaller --noconfirm --onedir --windowed --add-data "$PROJECT_DIR/Cfg:Cfg" --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtWidgets --name=SignalManager "$PROJECT_DIR/APP/main.py"

# Check if build was successful
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

# Copy the dist folder to the release directory
echo "Copying files to release directory..."
if [ -d "$RELEASE_DIR/SignalManager" ]; then
    rm -rf "$RELEASE_DIR/SignalManager"
fi
cp -r dist/SignalManager "$RELEASE_DIR/"

# Create a launcher script
echo "Creating launcher script..."
cat > "$RELEASE_DIR/run_signal_manager.sh" << 'EOF'
#!/bin/bash
# Signal Manager Launcher Script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/SignalManager/SignalManager" "$@"
EOF

chmod +x "$RELEASE_DIR/run_signal_manager.sh"

# Cleanup
echo "Cleaning up..."
rm -rf build dist
rm -f SignalManager.spec

echo "Build completed successfully!"
echo "Executable is located at: $RELEASE_DIR/SignalManager/SignalManager"
echo "Run the application using: $RELEASE_DIR/run_signal_manager.sh"

exit 0