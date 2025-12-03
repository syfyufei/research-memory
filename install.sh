#!/bin/bash

# Research Memory Installation Script
# Supports both GitHub remote and local installation

set -e

echo "🚀 Installing Research Memory..."

# Check if running from the repository directory
if [ -f ".claude-plugin/marketplace.json" ] && [ -f "skills/research-memory.md" ]; then
    echo "📍 Installing from local directory..."
    LOCAL_INSTALL=true
else
    echo "📥 Installing from GitHub..."
    LOCAL_INSTALL=false
fi

if [ "$LOCAL_INSTALL" = true ]; then
    # Local installation
    MARKETPLACE_PATH=$(pwd)
    echo "🔧 Adding local marketplace from: $MARKETPLACE_PATH"
    claude plugin marketplace add "$MARKETPLACE_PATH"

    echo "📦 Installing Research Memory plugin..."
    claude plugin install research-memory@research-memory-marketplace
else
    # Remote installation
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    echo "📥 Cloning research-memory from GitHub..."
    git clone https://github.com/syfyufei/research-memory.git
    cd research-memory

    echo "🔧 Adding marketplace..."
    claude plugin marketplace add .

    echo "📦 Installing Research Memory plugin..."
    claude plugin install research-memory@research-memory-marketplace

    echo "🧹 Cleaning up temporary files..."
    cd ~
    rm -rf "$TEMP_DIR"
fi

echo ""
echo "✨ Research Memory installed successfully!"
echo ""
echo "🎉 You can now use Research Memory in any Claude Code session:"
echo "   'Research Memory, help me get back up to speed with my project'"
echo "   'Log this work session to Research Memory'"
echo "   'Search for our decisions about spatial lag models'"
echo ""
echo "📚 Commands:"
echo "   - List plugins: claude plugin list"
echo "   - Update: claude plugin update research-memory"
echo "   - Uninstall: claude plugin uninstall research-memory"