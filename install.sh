#!/bin/bash

# Research Memory Installation Script
# This script installs Research Memory as a Claude Code plugin (superpowers-style)

set -e

echo "🚀 Installing Research Memory..."

# Check if research-memory already exists
if [ -d "research-memory" ]; then
    echo "✅ research-memory already exists locally"
    cd research-memory
    echo "🔄 Updating repository..."
    git pull
else
    echo "📥 Cloning research-memory..."
    git clone https://github.com/syfyufei/research-memory.git
    cd research-memory
fi

echo "🔧 Adding plugin marketplace..."
claude plugin marketplace add .

echo "📦 Installing Research Memory plugin..."
claude plugin install research-memory@research-memory-dev

echo "✨ Research Memory installed successfully!"
echo ""
echo "🎉 You can now use Research Memory in any Claude Code session:"
echo "   'Research Memory, help me get back up to speed with my project'"
echo "   'Log this work session to Research Memory'"
echo "   'Search for our decisions about spatial lag models'"
echo ""
echo "To uninstall: claude plugin uninstall research-memory"