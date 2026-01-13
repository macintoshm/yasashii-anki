#!/bin/bash
# Yasashii Anki Setup Script
# This script helps you get started with Yasashii Anki quickly

set -e

echo "=========================================="
echo "  Yasashii Anki Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check for Python 3.13+
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 13 ]; then
        print_status "Python $PYTHON_VERSION found"
    else
        print_error "Python 3.13+ is required (found $PYTHON_VERSION)"
        echo "Please install Python 3.13 or newer: https://www.python.org/downloads/"
        exit 1
    fi
else
    print_error "Python 3 not found"
    echo "Please install Python 3.13+: https://www.python.org/downloads/"
    exit 1
fi

# Check for uv
echo ""
echo "Checking for uv package manager..."
if command -v uv &> /dev/null; then
    print_status "uv found"
else
    print_warning "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    print_status "uv installed"
fi

# Unzip JMDict if needed
echo ""
echo "Checking for JMDict dictionary..."
if [ -f "jmdict-with-examples.json" ]; then
    print_status "jmdict-with-examples.json found"
elif [ -f "jmdict-with-examples.zip" ]; then
    echo "Unzipping jmdict-with-examples.zip..."
    unzip -o jmdict-with-examples.zip
    print_status "Dictionary unzipped"
else
    print_error "jmdict-with-examples.zip not found"
    echo "Please download jmdict-with-examples.zip from:"
    echo "https://github.com/scriptin/jmdict-simplified/releases"
    echo "Place the zip file in the project root directory and run this script again."
    exit 1
fi

# Create .env if it doesn't exist
echo ""
echo "Setting up configuration..."
if [ -f ".env" ]; then
    print_warning ".env already exists. Skipping..."
else
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_status ".env created from .env.example"

        echo ""
        echo "Please edit .env and set your Anki deck name."
        echo "You can do this now or later."
        read -p "Enter your Anki deck name (default: Japanese): " DECK_NAME
        DECK_NAME=${DECK_NAME:-Japanese}

        # Update the deck name in .env
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/AUTO_ANKI_DECK_NAME=.*/AUTO_ANKI_DECK_NAME=$DECK_NAME/" .env
        else
            # Linux
            sed -i "s/AUTO_ANKI_DECK_NAME=.*/AUTO_ANKI_DECK_NAME=$DECK_NAME/" .env
        fi
        print_status "Deck name set to: $DECK_NAME"
    else
        print_error ".env.example not found"
        exit 1
    fi
fi

# Install the package
echo ""
echo "Installing Yasashii Anki..."
uv pip install -e .
print_status "Installation complete"

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Make sure Anki is running with AnkiConnect installed"
echo "   (Get AnkiConnect: https://ankiweb.net/shared/info/2055492159)"
echo ""
echo "2. Create your deck in Anki (if not already created)"
echo ""
echo "3. Edit .env to configure your card type and field names"
echo ""
echo "4. Try it out:"
echo "   yasashii 猫           # Look up a word"
echo "   yasashii 猫 -c        # Look up and create card"
echo "   yasashii-gui          # Open the GUI"
echo ""
