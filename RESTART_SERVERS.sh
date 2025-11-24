#!/bin/bash

echo "🔄 Restarting Shock Score Servers..."
echo ""

# Kill existing processes
echo "Stopping existing servers..."
pkill -f "node.*server.js" 2>/dev/null
pkill -f "react-scripts" 2>/dev/null
sleep 2

# Check if ports are free
if lsof -ti:5000 > /dev/null 2>&1; then
    echo "⚠️  Port 5000 still in use, forcing kill..."
    lsof -ti:5000 | xargs kill -9 2>/dev/null
    sleep 1
fi

if lsof -ti:3000 > /dev/null 2>&1; then
    echo "⚠️  Port 3000 still in use, forcing kill..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    sleep 1
fi

echo "✅ Servers stopped"
echo ""
echo "📝 To start the servers:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd /home/nick_1804/CompouterVision/Module8/ShockScore/backend"
echo "  npm start"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd /home/nick_1804/CompouterVision/Module8/ShockScore/frontend"
echo "  npm start"
echo ""
