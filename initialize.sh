#!/bin/bash
# LUMAURA x XUVE Initialization Script
# This script initializes the development environment and database

echo "🌟 Initializing LUMAURA x XUVE environment..."

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads/videos
mkdir -p instance

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "   ⚠️ Please update .env file with your configuration."
fi

echo "🚀 Initialization complete!"
echo "   Run the application with: python main.py"
echo "   Visit http://localhost:5000 in your browser to access the application."
