# 🎬 Shock Score - Cinema Emotion Analytics Platform

> Real-time facial emotion recognition system for analyzing audience reactions to horror and thriller films.

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start)

---

## 🌟 Features

- 🎥 **Live Webcam Analysis** - Real-time emotion detection using your camera
- 📊 **Shock Score Algorithm** - Proprietary metric combining fear, surprise, and tension
- 📈 **Analytics Dashboard** - Visualize audience emotional responses
- 🎬 **Video Processing** - Batch analyze entire films for peak scare moments
- 🔒 **Privacy-First** - GDPR/CCPA compliant, no facial data storage
- ⚡ **Serverless Architecture** - Deploy on Netlify with zero server management

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/shock-score.git
cd shock-score

# 2. Start backend (Terminal 1)
cd backend
npm install
npm start

# 3. Start frontend (Terminal 2)
cd frontend
npm install
npm start

# 4. Open browser
# Visit http://localhost:3000
```

### Deploy to Netlify

```bash
# 1. Push to GitHub
git add .
git commit -m "Initial commit"
git push origin main

# 2. Connect to Netlify
# Go to https://app.netlify.com
# Click "New site from Git"
# Select your repository
# Deploy!
```

See [NETLIFY_DEPLOYMENT.md](NETLIFY_DEPLOYMENT.md) for detailed instructions.

---

## 📁 Project Structure

```
ShockScore/
├── frontend/              # React web application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Dashboard, Upload, Report pages
│   │   └── App.js
│   ├── public/
│   │   └── _redirects    # Netlify routing
│   └── package.json
│
├── backend/              # Express API server (local dev)
│   ├── routes/           # API endpoints
│   ├── services/         # Python bridge
│   └── server.js
│
├── netlify/              # Serverless functions (production)
│   └── functions/
│       ├── analyze-frame.js
│       └── health.js
│
├── Python FER Engine/    # Facial emotion recognition
│   ├── shock_score_engine.py
│   ├── face_detector.py
│   ├── emotion_analyzer.py
│   └── anonymizer.py
│
└── netlify.toml          # Deployment configuration
```

---

## 🎯 Use Cases

### For Studios
- Test audience reactions during pre-screenings
- Identify which scenes generate the strongest emotional responses
- Optimize pacing and scare placement
- Compare different cuts of a film

### For Filmmakers
- Validate if horror/thriller scenes are effective
- Get objective metrics on emotional impact
- Benchmark against industry standards
- Prove ROI for distributors

### For Researchers
- Study emotional responses to media
- Analyze fear and tension patterns
- Build datasets for emotion AI research

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI framework
- **React Router** - Client-side routing
- **Recharts** - Data visualization
- **Axios** - HTTP client

### Backend
- **Node.js + Express** - API server (local dev)
- **Netlify Functions** - Serverless API (production)
- **Multer** - File upload handling

### Python FER Engine
- **DeepFace** - Facial emotion recognition
- **MTCNN** - Face detection
- **OpenCV** - Video processing
- **TensorFlow** - Deep learning models

### Deployment
- **Netlify** - Hosting and serverless functions
- **GitHub** - Version control and CI/CD

---

## 📊 Shock Score Algorithm

The Shock Score is calculated using a weighted combination of emotions:

```javascript
Shock Score = (
  Fear × 2.0 +
  Surprise × 1.5 +
  Disgust × 0.8 +
  Happy × 0.3 +
  Angry × 0.2 +
  Sad × 0.1
) / max_possible × 100
```

**Scale**: 0-100
- **0-20**: Calm/Neutral
- **20-40**: Mild tension
- **40-60**: Moderate scare
- **60-80**: High fear
- **80-100**: Extreme terror

---

## 🎥 Webcam Feature

Try the interactive demo to see your real-time Shock Score!

### How It Works

1. Click "Start Camera" on the dashboard
2. Allow camera permissions
3. Your webcam captures frames every 1.5 seconds
4. Facial emotions are analyzed in real-time
5. Shock Score updates instantly

### Privacy

- ✅ No frames stored
- ✅ No personal data collected
- ✅ All processing happens in real-time
- ✅ Instant deletion after analysis

---

## 🧪 Testing

### Test Build Process

```bash
./test-netlify-build.sh
```

This simulates the Netlify build and verifies:
- All required files exist
- Dependencies install successfully
- Frontend builds without errors
- Functions are ready to deploy

### Manual Testing

**Backend API:**
```bash
cd backend
npm start
node test-endpoint.js
```

**Frontend:**
```bash
cd frontend
npm start
# Open http://localhost:3000
```

---

## 📚 Documentation

- **[NETLIFY_DEPLOYMENT.md](NETLIFY_DEPLOYMENT.md)** - Complete deployment guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design
- **[INSTALLATION.md](INSTALLATION.md)** - Local setup instructions
- **[WEBCAM_FEATURE.md](WEBCAM_FEATURE.md)** - Webcam feature documentation

---

## 🔐 Environment Variables

### Local Development

Copy `.env.example` to `.env`:

```bash
# Backend
PORT=5000
NODE_ENV=development
PYTHON_PATH=../venv/bin/python

# Frontend
REACT_APP_API_URL=http://localhost:5000
```

### Production (Netlify)

Set in Netlify dashboard:
- `NODE_VERSION=18`
- `PYTHON_VERSION=3.11`

No API keys required for current mock data version.

---

## 🚦 Current Status

### ✅ Implemented
- Interactive webcam demo with real-time analysis
- React dashboard with analytics visualizations
- Serverless API functions for Netlify
- Mock emotion data generation
- Shock Score calculation algorithm
- Privacy-compliant architecture

### 🚧 In Progress
- Full Python FER engine integration
- Video upload and batch processing
- User authentication
- Database for historical data

### 📋 Planned
- Microsoft Azure Face API integration
- Multi-camera support for cinema screenings
- Real-time streaming analytics
- Advanced reporting and exports

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is proprietary and confidential.

© 2025 Shock Score. All rights reserved.

---

## 🆘 Support

### Issues?

- Check [NETLIFY_DEPLOYMENT.md](NETLIFY_DEPLOYMENT.md) troubleshooting section
- Review [INSTALLATION.md](INSTALLATION.md) for local setup help
- Open an issue on GitHub

### Common Problems

**Webcam not working?**
- Allow camera permissions in browser
- Check debug panel for error messages
- See [WEBCAM_FEATURE.md](WEBCAM_FEATURE.md)

**Build failing?**
- Run `./test-netlify-build.sh` locally
- Check Node.js version (18+)
- Verify all dependencies installed

**404 errors?**
- Check `netlify.toml` redirects
- Verify functions deployed
- Test health endpoint: `/api/health`

---

## 🎬 Demo

Try the live webcam feature at your deployed URL!

---

## 🙏 Acknowledgments

- **DeepFace** - Open-source facial recognition library
- **MTCNN** - Face detection model
- **Netlify** - Hosting and serverless platform
- **React** - Frontend framework

---

**Built with ❤️ for the film industry**
