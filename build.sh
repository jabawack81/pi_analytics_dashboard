#!/bin/bash

# Build script for PostHog Pi Dashboard
# This script builds the React frontend and prepares the application for deployment

echo "Building PostHog Pi Dashboard..."

# Check if we're in the right directory
if [ ! -f "backend/app.py" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Build React frontend
echo "Building React frontend..."
cd frontend
npm install
npm run build

if [ $? -eq 0 ]; then
    echo "✅ React frontend built successfully"
else
    echo "❌ React frontend build failed"
    exit 1
fi

# Go back to project root
cd ..

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Python dependencies installation failed"
    exit 1
fi

echo "🎉 Build complete!"
echo ""
echo "To run the application locally:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python3 app.py"
echo ""
echo "Then visit http://localhost:5000 in your browser"