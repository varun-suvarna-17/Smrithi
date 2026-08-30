# SMRITHI Full-Stack Development Guide

This guide explains how to develop and test the integrated Frontend & Backend.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              SMRITHI Frontend (React + Vite)             │
│  ✅ Caregiver Dashboard  ✅ Patient Games  ✅ Analytics  │
│          Port: 5173                                      │
└─────────────────────────────────────────────────────────┘
                           ↕️ 
                    HTTP/WebSocket
                  (Vite Proxy to /api)
                           ↕️
┌─────────────────────────────────────────────────────────┐
│           SMRITHI Backend (FastAPI + MongoDB)            │
│  ✅ REST APIs  ✅ Auth  ✅ Database  ✅ AI Engine        │
│          Port: 8000                                      │
│     Swagger UI: http://localhost:8000/docs              │
└─────────────────────────────────────────────────────────┘
                           ↕️
                       MongoDB
```

---

## 📋 Prerequisites

### Windows System
```powershell
# Check Node.js version (18+ required)
node --version

# Check Python version (3.10+ required)
python --version

# Check npm
npm --version
```

### macOS / Linux
```bash
# Same as above
node --version
python --version
npm --version
```

### MongoDB
- **Local:** Install from [mongodb.com](https://www.mongodb.com/try/download/community)
- **Cloud:** Use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (free tier available)

---

## 🚀 Development Workflow

### Option 1: Run Full Stack Together (Recommended)

```bash
# From root directory
npm install                    # Install root dependencies (concurrently)
npm run install:all           # Install backend & frontend dependencies
npm run dev                   # Start both frontend & backend
```

**This will:**
- ✅ Start Backend API on `http://localhost:8000`
- ✅ Start Frontend on `http://localhost:5173`
- ✅ Both will auto-reload on file changes

### Option 2: Run Backend & Frontend Separately

#### Terminal 1 - Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🔌 Testing API Endpoints

### Using Swagger UI (Easiest)
1. Start backend: `npm run backend:dev`
2. Open `http://localhost:8000/docs`
3. Use the interactive Swagger UI to test endpoints

### Using Postman
1. Import: `Smrithi_Backend.postman_collection.json`
2. Set base URL to `http://localhost:8000`
3. Tests will use demo data automatically seeded

### Using Frontend
1. Start full stack: `npm run dev`
2. Open `http://localhost:5173`
3. Login with demo credentials (set in backend seeding)

---

## 🛠️ Development Tips

### Hot Reload / Auto-Reload
- **Frontend:** Vite provides instant hot module reload (HMR)
- **Backend:** Uvicorn with `--reload` watches Python files

### Environment Variables
- Create `.env` in root directory
- Both frontend and backend will pick up configuration
- Restart servers after changing `.env`

### API Proxy (Development)
The frontend's Vite config automatically proxies API calls:
- Request to `http://localhost:5173/api/patients`
- Proxied to `http://localhost:8000/patients`
- No CORS issues in development!

### Database Fallback
- If MongoDB is unavailable, backend uses in-memory database
- Useful for quick testing without database setup
- Set `USE_IN_MEMORY_FALLBACK=true` in `.env`

---

## 📝 Common Development Tasks

### Add New Backend Endpoint

**File:** `backend/app/routes/new_feature.py`
```python
from fastapi import APIRouter, Depends
from app.middleware.auth_guard import require_auth

router = APIRouter(prefix="/new-feature", tags=["new-feature"])

@router.get("/status")
async def get_status():
    return {"status": "online"}

@router.post("/data")
async def create_data(payload: dict, user = Depends(require_auth)):
    # user contains authenticated caregiver info
    return {"created": True}
```

**Register in:** `backend/app/main.py`
```python
from app.routes import new_feature
app.include_router(new_feature.router)
```

### Add New Frontend Page

**File:** `frontend/src/pages/NewPage.jsx`
```jsx
import { useEffect, useState } from 'react';
import axios from 'axios';
import Layout from '../components/Layout';

export default function NewPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('/api/new-feature/data', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setData(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Layout>
      <div>
        <h1>New Page</h1>
        {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
      </div>
    </Layout>
  );
}
```

**Add route in:** `frontend/src/App.jsx`
```jsx
import NewPage from './pages/NewPage';

<Route path="/new-page" element={<NewPage />} />
```

---

## 🐛 Debugging

### Backend Debugging
```bash
# Check logs
python -m uvicorn app.main:app --reload --log-level debug

# Use Python debugger (pdb)
import pdb; pdb.set_trace()
```

### Frontend Debugging
- Open Chrome DevTools: `F12` or `Ctrl+Shift+I`
- Check Console tab for errors
- Use React DevTools browser extension

### Common Issues

#### "Connection refused" (Backend not running)
```bash
# Make sure backend is running
npm run backend:dev
# or
cd backend && python -m uvicorn app.main:app --reload
```

#### "CORS Error"
- Frontend sends requests to `/api/...`
- Vite proxy configuration in `vite.config.js` handles this
- If using different domain, backend must have CORS enabled

#### "MongoDB Connection Failed"
```bash
# Option 1: Start local MongoDB
# On Windows: open MongoDB Community (starts server)
# On Mac: brew services start mongodb-community

# Option 2: Use MongoDB Atlas (cloud)
# Update MONGODB_URI in .env
```

---

## 📦 Building for Production

### Frontend Build
```bash
cd frontend
npm run build
# Output: frontend/dist/
```

### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment for Production
Create `.env.production` with:
```
APP_ENV=production
DEBUG=false
MONGODB_URI=your-production-mongodb-uri
SECRET_KEY=your-strong-secret-key
VITE_API_BASE_URL=https://api.yourdomain.com
```

---

## ✅ Pre-Commit Checklist

Before committing changes:
- [ ] Backend tests pass: `pytest backend/tests/`
- [ ] Frontend builds: `npm run frontend:build`
- [ ] No console errors
- [ ] Code follows project style guidelines
- [ ] Updated `.env.example` if new config needed
- [ ] Updated README if architecture changed

---

## 📚 Additional Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **Vite Docs:** https://vitejs.dev/
- **MongoDB Docs:** https://docs.mongodb.com/
- **Axios Docs:** https://axios-http.com/

---

## 🤝 Need Help?

1. Check existing GitHub Issues
2. Review backend/README.md for API details
3. Review frontend/README.md for UI component docs
4. Ask in GitHub Discussions

---

**Happy Coding! 🚀**
