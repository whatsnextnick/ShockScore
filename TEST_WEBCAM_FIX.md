# Testing the Simplified Webcam Feature

## What I Fixed

I've updated your application to use a **simplified version** of the webcam component that includes:

1. **Debug logging** - Shows exactly what's happening at each step
2. **Mock data** - Returns test emotion data to verify the pipeline works
3. **Better error handling** - Catches and displays any issues

## Files Changed

1. **frontend/src/pages/Dashboard.js** - Now imports `WebcamShockScoreSimple` instead of `WebcamShockScore`
2. **backend/server.js** - Already configured to use `analyze-simple.js` route
3. **backend/routes/analyze-simple.js** - Returns mock emotion data (no Python needed)
4. **frontend/src/components/WebcamShockScoreSimple.js** - New component with debug logging

## How to Test

### Step 1: Stop Any Running Servers

If you have servers running, press `Ctrl+C` in both terminal windows to stop them.

### Step 2: Start Backend

```bash
cd /home/nick_1804/CompouterVision/Module8/ShockScore/backend
npm start
```

You should see:
```
============================================================
🎬 SHOCK SCORE API SERVER
============================================================
Server running on port 5000
Environment: development
Frontend URL: http://localhost:3000
============================================================
```

### Step 3: Start Frontend (in a new terminal)

```bash
cd /home/nick_1804/CompouterVision/Module8/ShockScore/frontend
npm start
```

Browser should automatically open to `http://localhost:3000`

### Step 4: Test the Webcam Feature

1. **Scroll to the top** of the dashboard
2. **Click "🎥 Start Camera"**
3. **Allow camera permissions** when browser asks
4. **Look for the debug panel** - You should see a black box with green text showing:
   ```
   Debug Log:
   [timestamp]: Requesting camera access...
   [timestamp]: ✓ Camera started
   [timestamp]: Starting frame capture...
   [timestamp]: Capturing frame...
   [timestamp]: Sending frame (XX.XKB)...
   [timestamp]: Response: 200
   [timestamp]: ✓ Got data: Shock=XX.X
   Status: ✓ Ready
   ```

5. **Below the debug panel**, you should see:
   - Your live webcam feed
   - "✓ Active - Analyzing every 1.5s" indicator
   - **Large shock score** (0-100)
   - **Dominant emotion** with emoji
   - **Emotion bars** showing percentages

## What You Should See

### If Everything Works:

✅ Debug panel shows successful frame capture
✅ Response status is 200
✅ Shock score updates every 1.5 seconds
✅ Emotion bars animate with random values
✅ Dominant emotion changes

**Note**: The values will be **random mock data** since we're not using the Python engine yet. This is expected! We're testing the pipeline first.

### If It Doesn't Work:

Check the debug panel for errors:

**Error: "Cannot access webcam"**
- Click the camera icon in browser address bar
- Select "Allow" for camera permissions
- Refresh page and try again

**Error: Response status 404 or 500**
- Backend server not running
- Check backend terminal for errors
- Restart backend: `cd backend && npm start`

**No debug panel appears**
- Frontend not updated
- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Check browser console (F12) for errors

## What to Report Back

Once you've tested, let me know:

1. **Does the debug panel appear?** Yes/No
2. **What does the debug log show?** (copy the last 5 lines)
3. **Do you see the shock score updating?** Yes/No
4. **Any error messages?** (from debug panel or browser console)

## Next Steps After Testing

**If mock data works:**
- We'll connect the full Python FER engine
- Replace mock emotions with real face detection
- Test with actual facial expressions

**If mock data doesn't work:**
- We'll troubleshoot the React component
- Check API routing
- Verify CORS configuration

---

## Quick Troubleshooting

### Backend won't start
```bash
cd backend
npm install
npm start
```

### Frontend won't start
```bash
cd frontend
npm install
npm start
```

### Port already in use
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Hard reset
```bash
# Stop everything
pkill -f "node.*server.js"
pkill -f "react-scripts"

# Start fresh
cd backend && npm start
# In new terminal:
cd frontend && npm start
```

---

**The simplified version with mock data will help us identify exactly where the problem is occurring before we connect the full Python engine.**
