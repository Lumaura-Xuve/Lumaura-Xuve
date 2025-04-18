#!/bin/bash
# Script to update the GitHub repository with all LUMAURA x XUVE components

echo "LUMAURA x XUVE GitHub Repository Update Script"
echo "==============================================="
echo

# Clone the repository
echo "Step 1: Cloning the repository..."
git clone https://github.com/Lumaura-Xuve/Lumaura-Xuve.git
cd Lumaura-Xuve

# Copy files from our full repository
echo "Step 2: Copying files from the complete LUMAURA x XUVE system..."
cp -r /home/runner/workspace/full_repository/* ./
cp -r /home/runner/workspace/full_repository/.[a-zA-Z]* ./ 2>/dev/null || true

# Add all files to git
echo "Step 3: Adding files to Git..."
git add .

# Commit the changes
echo "Step 4: Committing changes..."
git commit -m "Add complete LUMAURA x XUVE system with all components"

# Push to GitHub
echo "Step 5: Pushing to GitHub..."
git push

echo
echo "Repository update complete!"
echo "Visit: https://github.com/Lumaura-Xuve/Lumaura-Xuve"