#!/bin/bash

# Research Memory Installation Script
# This script installs Research Memory via Adrian's plugin marketplace

set -e

echo "🚀 Installing Research Memory..."

# Check if adrian-marketplace already exists
if [ -d "adrian-marketplace" ]; then
    echo "✅ adrian-marketplace already exists locally"
else
    echo "📥 Cloning adrian-marketplace..."
    git clone https://github.com/syfyufei/adrian-marketplace.git
fi

echo "🔧 Adding plugin marketplace..."
claude plugin marketplace add ./adrian-marketplace

echo "📦 Installing Research Memory plugin..."
claude plugin install research-memory@adrian-marketplace

echo "✨ Research Memory installed successfully!"
echo ""
echo "🎉 You can now use Research Memory in any Claude Code session:"
echo "   'Research Memory, help me get back up to speed with my project'"
echo "   'Log this work session to Research Memory'"
echo "   'Search for our decisions about spatial lag models'"
echo ""
echo "To uninstall: claude plugin uninstall research-memory"