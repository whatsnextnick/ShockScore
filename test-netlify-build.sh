#!/bin/bash

# Test Netlify Build Process Locally
# This simulates what Netlify will do during deployment

set -e  # Exit on error

echo "🧪 Testing Netlify Build Process"
echo "================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "netlify.toml" ]; then
    echo -e "${RED}❌ Error: netlify.toml not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo "📁 Project Structure Check"
echo "-------------------------"

# Check required files
files=(
    "netlify.toml"
    "frontend/package.json"
    "frontend/public/_redirects"
    "frontend/.env.production"
    "netlify/functions/analyze-frame.js"
    "netlify/functions/health.js"
)

all_good=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file ${RED}(missing)${NC}"
        all_good=false
    fi
done

if [ "$all_good" = false ]; then
    echo ""
    echo -e "${RED}❌ Some required files are missing${NC}"
    exit 1
fi

echo ""
echo "📦 Installing Frontend Dependencies"
echo "-----------------------------------"
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Frontend npm install failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

echo ""
echo "🏗️  Building Frontend for Production"
echo "-----------------------------------"
npm run build
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Frontend build failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Frontend build successful${NC}"

echo ""
echo "📊 Build Output Statistics"
echo "-------------------------"
if [ -d "build" ]; then
    echo "Build directory size: $(du -sh build | cut -f1)"
    echo "Files created: $(find build -type f | wc -l)"
    echo ""
    echo "Main assets:"
    ls -lh build/static/js/*.js 2>/dev/null | awk '{print "  " $9, "-", $5}' || echo "  No JS files found"
    ls -lh build/static/css/*.css 2>/dev/null | awk '{print "  " $9, "-", $5}' || echo "  No CSS files found"
fi

cd ..

echo ""
echo "📦 Installing Function Dependencies"
echo "-----------------------------------"
cd netlify/functions
npm install
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Function dependencies install failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Function dependencies installed${NC}"

cd ../..

echo ""
echo "✅ Build Test Complete!"
echo "======================"
echo ""
echo -e "${GREEN}Your app is ready for Netlify deployment!${NC}"
echo ""
echo "Next steps:"
echo "  1. Push to GitHub: git push origin main"
echo "  2. Connect repository to Netlify"
echo "  3. Deploy!"
echo ""
echo "Or test with Netlify CLI:"
echo "  npm install -g netlify-cli"
echo "  netlify dev"
echo ""
