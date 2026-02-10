#!/bin/bash

# InfraMind Integration Test Script
# Tests backend connectivity and starts both servers

set -e

echo "=============================================="
echo "🚀 InfraMind Integration Test"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test backend
echo "🔍 Testing Backend Connectivity..."
if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is running at http://localhost:8000${NC}"
    echo ""
    echo "Backend Health:"
    curl -s http://localhost:8000/api/v1/health | python3 -m json.tool
    echo ""
else
    echo -e "${RED}❌ Backend is NOT running${NC}"
    echo ""
    echo -e "${YELLOW}Starting backend...${NC}"
    echo "Run this command in a separate terminal:"
    echo ""
    echo "  cd /Users/vaishnavikamdi/Documents/InfraMind"
    echo "  source venv/bin/activate"
    echo "  uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload"
    echo ""
    exit 1
fi

echo "=============================================="
echo "🎨 Frontend Setup"
echo "=============================================="
echo ""

# Check if frontend directory exists
if [ ! -d "/Users/vaishnavikamdi/Documents/InfraMind/infra-mind-dashboard-ui" ]; then
    echo -e "${RED}❌ Frontend directory not found${NC}"
    exit 1
fi

cd /Users/vaishnavikamdi/Documents/InfraMind/infra-mind-dashboard-ui

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    pnpm install
fi

echo ""
echo "=============================================="
echo "✅ Integration Test Complete!"
echo "=============================================="
echo ""
echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo "📍 Frontend: http://localhost:3000 (start with 'pnpm dev')"
echo ""
echo "🚀 Start the frontend now:"
echo ""
echo "  cd /Users/vaishnavikamdi/Documents/InfraMind/infra-mind-dashboard-ui"
echo "  pnpm dev"
echo ""
echo "Then open http://localhost:3000 in your browser!"
echo ""
